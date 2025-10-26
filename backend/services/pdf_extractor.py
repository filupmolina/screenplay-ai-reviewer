"""
PDF text extraction for screenplays
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class PDFExtractor:
    """
    Extract text from screenplay PDFs
    """

    def __init__(self):
        if not pypdf and not pdfplumber:
            raise ImportError("Need pypdf or pdfplumber installed: pip install pypdf pdfplumber")

    def extract_text_pypdf(self, pdf_path: str, max_pages: int = None) -> str:
        """
        Extract text using pypdf

        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum pages to extract (None = all)

        Returns:
            Extracted text
        """
        if not pypdf:
            raise ImportError("pypdf not installed")

        text_parts = []

        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            total_pages = len(reader.pages)

            pages_to_process = min(max_pages, total_pages) if max_pages else total_pages

            for page_num in range(pages_to_process):
                page = reader.pages[page_num]
                text = page.extract_text()
                text_parts.append(text)

        return '\n\n'.join(text_parts)

    def extract_text_pdfplumber(self, pdf_path: str, max_pages: int = None) -> str:
        """
        Extract text using pdfplumber (better for formatted text)

        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum pages to extract (None = all)

        Returns:
            Extracted text
        """
        if not pdfplumber:
            raise ImportError("pdfplumber not installed")

        text_parts = []

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(max_pages, total_pages) if max_pages else total_pages

            for page_num in range(pages_to_process):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        return '\n\n'.join(text_parts)

    def extract_text(self, pdf_path: str, max_pages: int = None, prefer_pdfplumber: bool = True) -> str:
        """
        Extract text from PDF using best available method

        Args:
            pdf_path: Path to PDF file
            max_pages: Maximum pages to extract (None = all)
            prefer_pdfplumber: Use pdfplumber if available (better formatting)

        Returns:
            Extracted text
        """
        if prefer_pdfplumber and pdfplumber:
            return self.extract_text_pdfplumber(pdf_path, max_pages)
        elif pypdf:
            return self.extract_text_pypdf(pdf_path, max_pages)
        else:
            raise ImportError("No PDF library available")

    def extract_with_metadata(self, pdf_path: str, max_pages: int = None) -> dict:
        """
        Extract text and metadata from PDF

        Returns:
            Dict with 'text', 'total_pages', 'extracted_pages'
        """
        text = self.extract_text(pdf_path, max_pages)

        # Get page count
        total_pages = 0
        if pdfplumber:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
        elif pypdf:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                total_pages = len(reader.pages)

        extracted_pages = min(max_pages, total_pages) if max_pages else total_pages

        return {
            'text': text,
            'total_pages': total_pages,
            'extracted_pages': extracted_pages
        }
