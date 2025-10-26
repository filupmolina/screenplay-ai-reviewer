"""
Test PDF extraction - SAFE (only first 2 pages)
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.pdf_extractor import PDFExtractor


def test_pdf_extraction():
    """Test extracting first 2 pages from PDF"""

    print("=" * 60)
    print("PDF EXTRACTION TEST (First 2 pages only)")
    print("=" * 60)

    # Path to PDF
    pdf_path = Path(__file__).parent.parent.parent / "Bad Hombres by Filup Molina.pdf"

    if not pdf_path.exists():
        print(f"\n✗ PDF not found at: {pdf_path}")
        return

    print(f"\nPDF found: {pdf_path.name}")
    print(f"Size: {pdf_path.stat().st_size / 1024:.1f} KB")

    # Extract first 2 pages only (safe)
    extractor = PDFExtractor()

    try:
        result = extractor.extract_with_metadata(str(pdf_path), max_pages=2)

        print(f"\nTotal pages in PDF: {result['total_pages']}")
        print(f"Extracted pages: {result['extracted_pages']}")
        print(f"Extracted text length: {len(result['text'])} characters")

        # Show first 1000 characters to see format
        print("\n" + "=" * 60)
        print("FIRST 1000 CHARACTERS (to see format)")
        print("=" * 60)
        print(result['text'][:1000])
        print("...")

        # Save to file for inspection
        output_file = Path(__file__).parent / "pdf_sample.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"\nFull extracted text saved to: {output_file}")

    except ImportError as e:
        print(f"\n✗ Error: {e}")
        print("\nInstall dependencies: pip install pypdf pdfplumber")
    except Exception as e:
        print(f"\n✗ Error extracting PDF: {e}")


if __name__ == "__main__":
    test_pdf_extraction()
