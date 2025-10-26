"""
Screenplay parser - supports Fountain format
"""
import re
from typing import List, Tuple, Optional
import sys
from pathlib import Path

# Add backend to path if needed
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from models.screenplay import Screenplay, Scene, SceneElement


class FountainParser:
    """
    Parse Fountain format screenplays and PDF screenplays

    Fountain spec: https://fountain.io/syntax
    Also supports PDF extraction
    """

    # Scene heading pattern (must start with INT, EXT, EST, I/E, INT./EXT.)
    SCENE_HEADING_PATTERN = re.compile(
        r'^(INT|EXT|EST|INT\./EXT\.|I/E)[\.\s]+(.+?)(?:\s+-\s+(.+?))?$',
        re.IGNORECASE
    )

    # Character name pattern (all caps, optionally with parenthetical)
    CHARACTER_PATTERN = re.compile(r'^([A-Z][A-Z\s\-\.]+?)(\s*\(.*\))?$')

    # Transition pattern (ends with TO:)
    TRANSITION_PATTERN = re.compile(r'^([A-Z\s]+TO:)\s*$')

    # Title page keys
    TITLE_PAGE_KEYS = [
        'title', 'credit', 'author', 'authors', 'source', 'draft date',
        'date', 'contact', 'copyright'
    ]

    def __init__(self):
        self.in_title_page = True
        self.title_page_data = {}

    def parse_file(self, filepath: str, max_pages: int = None) -> Screenplay:
        """
        Parse a screenplay file into a Screenplay object

        Supports:
        - .fountain files (text)
        - .pdf files (extracts text first)
        - .txt files (text)

        Args:
            filepath: Path to file
            max_pages: For PDFs, max pages to extract (None = all)

        Returns:
            Screenplay object
        """
        filepath_lower = filepath.lower()

        if filepath_lower.endswith('.pdf'):
            # Extract text from PDF
            from services.pdf_extractor import PDFExtractor
            extractor = PDFExtractor()
            result = extractor.extract_with_metadata(filepath, max_pages=max_pages)
            content = result['text']

            # Store PDF metadata
            self.pdf_metadata = {
                'total_pages': result['total_pages'],
                'extracted_pages': result['extracted_pages']
            }
        else:
            # Read as text file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.pdf_metadata = None

        return self.parse(content)

    def parse(self, content: str) -> Screenplay:
        """Parse Fountain content into a Screenplay object"""
        lines = content.split('\n')

        # Reset state
        self.in_title_page = True
        self.title_page_data = {}

        # Parse title page and get screenplay lines
        screenplay_lines = self._parse_title_page(lines)

        # Split into scenes
        scenes = self._split_into_scenes(screenplay_lines)

        # Parse each scene
        parsed_scenes = []
        for i, scene_lines in enumerate(scenes):
            scene = self._parse_scene(i + 1, scene_lines)
            if scene:
                parsed_scenes.append(scene)

        # Extract all unique characters
        all_characters = set()
        total_words = 0
        for scene in parsed_scenes:
            all_characters.update(scene.characters_present)
            total_words += scene.word_count

        # Build screenplay object
        screenplay = Screenplay(
            title=self.title_page_data.get('title'),
            author=self.title_page_data.get('author') or self.title_page_data.get('authors'),
            draft_date=self.title_page_data.get('draft date') or self.title_page_data.get('date'),
            scenes=parsed_scenes,
            total_scenes=len(parsed_scenes),
            characters=sorted(list(all_characters)),
            word_count=total_words,
            metadata=self.title_page_data
        )

        return screenplay

    def _parse_title_page(self, lines: List[str]) -> List[str]:
        """
        Parse title page metadata, return remaining screenplay lines

        Title page ends with first blank line followed by content
        """
        screenplay_start_idx = 0

        for i, line in enumerate(lines):
            # Check for title page key: value format
            if ':' in line and not line.strip().startswith('==='):
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip().lower()
                    value = key_value[1].strip()

                    if key in self.TITLE_PAGE_KEYS:
                        self.title_page_data[key] = value
                        continue

            # Check for title page end marker (===)
            if line.strip() == '===' or line.strip().startswith('==='):
                screenplay_start_idx = i + 1
                self.in_title_page = False
                break

            # Empty line might signal end of title page
            if not line.strip() and self.title_page_data:
                # Check if next non-empty line is a scene heading
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip():
                        if self.SCENE_HEADING_PATTERN.match(lines[j].strip()):
                            screenplay_start_idx = i + 1
                            self.in_title_page = False
                            break
                        break
                if not self.in_title_page:
                    break

        return lines[screenplay_start_idx:]

    def _split_into_scenes(self, lines: List[str]) -> List[List[str]]:
        """Split screenplay into scenes based on scene headings"""
        scenes = []
        current_scene = []

        for line in lines:
            stripped = line.strip()

            # Check if this is a scene heading
            if self.SCENE_HEADING_PATTERN.match(stripped):
                # Save previous scene if it exists
                if current_scene:
                    scenes.append(current_scene)
                # Start new scene with this heading
                current_scene = [line]
            else:
                # Add to current scene
                if current_scene or stripped:  # Don't start with empty lines
                    current_scene.append(line)

        # Add the last scene
        if current_scene:
            scenes.append(current_scene)

        return scenes

    def _parse_scene(self, scene_number: int, lines: List[str]) -> Optional[Scene]:
        """Parse a single scene"""
        if not lines:
            return None

        # First line should be scene heading
        heading = lines[0].strip()
        match = self.SCENE_HEADING_PATTERN.match(heading)

        if not match:
            # Not a valid scene heading, skip
            return None

        int_ext = match.group(1).upper()
        location = match.group(2).strip() if match.group(2) else ""
        time_of_day = match.group(3).strip().upper() if match.group(3) else None

        # Parse scene elements
        elements = []
        characters_present = set()
        characters_speaking = set()
        full_text_parts = [heading]

        i = 1  # Start after heading
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                # Empty line
                i += 1
                continue

            # Check for character name
            if self._is_character_line(stripped):
                char_name = self._extract_character_name(stripped)
                elements.append(SceneElement(
                    type="character",
                    text=char_name,
                    line_number=i
                ))
                characters_present.add(char_name)
                characters_speaking.add(char_name)
                full_text_parts.append(stripped)

                # Next line(s) might be parenthetical and/or dialogue
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        i += 1
                        break

                    # Check for parenthetical
                    if next_line.startswith('(') and next_line.endswith(')'):
                        elements.append(SceneElement(
                            type="parenthetical",
                            text=next_line,
                            line_number=i
                        ))
                        full_text_parts.append(next_line)
                        i += 1
                        continue

                    # Check if it's dialogue (indented or just follows character)
                    if not self._is_character_line(next_line) and not self.SCENE_HEADING_PATTERN.match(next_line):
                        elements.append(SceneElement(
                            type="dialogue",
                            text=next_line,
                            line_number=i
                        ))
                        full_text_parts.append(next_line)
                        i += 1
                    else:
                        # Not dialogue, break out
                        break

            # Check for transition
            elif self.TRANSITION_PATTERN.match(stripped):
                elements.append(SceneElement(
                    type="transition",
                    text=stripped,
                    line_number=i
                ))
                full_text_parts.append(stripped)
                i += 1

            # Otherwise it's action/description
            else:
                elements.append(SceneElement(
                    type="action",
                    text=stripped,
                    line_number=i
                ))
                full_text_parts.append(stripped)

                # Check for character names in action lines (e.g., "JOHN enters")
                action_characters = self._extract_characters_from_action(stripped)
                characters_present.update(action_characters)

                i += 1

        # Build full text
        full_text = '\n'.join(full_text_parts)
        word_count = len(full_text.split())

        scene = Scene(
            scene_number=scene_number,
            scene_id=f"SCENE_{scene_number:03d}",
            heading=heading,
            location=location,
            time_of_day=time_of_day,
            interior_exterior=int_ext,
            elements=elements,
            full_text=full_text,
            characters_present=sorted(list(characters_present)),
            characters_speaking=sorted(list(characters_speaking)),
            word_count=word_count
        )

        return scene

    def _is_character_line(self, line: str) -> bool:
        """Check if a line is a character name"""
        # Must be all caps (with spaces, hyphens, dots allowed)
        # Must not be a scene heading
        # Must not be a transition
        if self.SCENE_HEADING_PATTERN.match(line):
            return False
        if self.TRANSITION_PATTERN.match(line):
            return False

        return bool(self.CHARACTER_PATTERN.match(line))

    def _extract_character_name(self, line: str) -> str:
        """Extract clean character name from character line"""
        match = self.CHARACTER_PATTERN.match(line)
        if match:
            name = match.group(1).strip()
            # Remove common suffixes like (V.O.), (O.S.), (CONT'D)
            name = re.sub(r'\s*\((V\.O\.|O\.S\.|CONT\'D)\)\s*$', '', name, flags=re.IGNORECASE)
            return name
        return line.strip()

    def _extract_characters_from_action(self, action: str) -> List[str]:
        """Extract character names mentioned in action lines"""
        characters = []

        # Look for names in ALL CAPS (likely character names)
        # Must be 2+ letters, can include spaces/hyphens
        pattern = r'\b([A-Z][A-Z\-]+(?:\s+[A-Z][A-Z\-]+)*)\b'
        matches = re.findall(pattern, action)

        for match in matches:
            # Filter out common non-character all-caps words
            if match not in ['INT', 'EXT', 'DAY', 'NIGHT', 'CONTINUOUS', 'LATER', 'THE', 'A', 'AN']:
                # Clean up
                match = match.strip()
                if len(match) >= 2:
                    characters.append(match)

        return characters
