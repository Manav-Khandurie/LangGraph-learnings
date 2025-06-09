from utils.pdf_utils import extract_text_from_pdf

def extractor_agent(file_path: str) -> str:
    """
    Agent to extract text from a PDF.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content.
    """
    return extract_text_from_pdf(file_path)
