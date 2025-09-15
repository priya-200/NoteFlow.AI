import pdfkit
import tempfile
from backend.app.utils.src.config import WKHTMLTOPDF_PATH

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def generate_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpf:
        pdf_path = tmpf.name
    pdfkit.from_string(html_content, pdf_path, configuration=PDFKIT_CONFIG)
    return pdf_path
