import PyPDF2
import io

def extract_text_from_pdf(pdf_file_stream):
    """
    Extracts text from a PDF file stream (e.g., from Streamlit file_uploader).

    Args:
        pdf_file_stream: A file-like object (e.g., from st.file_uploader).

    Returns:
        str: Extracted text from the PDF, or an empty string if error.
    """
    text = ""
    try:
        # PyPDF2.PdfReader expects a binary file stream
        reader = PyPDF2.PdfReader(pdf_file_stream)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or "" # Use .extract_text() and handle None
    except PyPDF2.errors.PdfReadError:
        print("Error: Could not read PDF file. It might be encrypted or corrupted.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during PDF parsing: {e}")
        return ""
    return text.strip()