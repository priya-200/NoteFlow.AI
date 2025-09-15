import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("YT_TRANSCRIPT_API_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

if not API_TOKEN:
    raise ValueError("Missing YT_TRANSCRIPT_API_TOKEN in .env file")
if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")