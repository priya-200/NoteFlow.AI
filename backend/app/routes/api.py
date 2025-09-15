from flask import Blueprint, request, jsonify, send_file, Flask
from backend.app.services.transcript_service import fetch_transcript
from backend.app.services.gemini_service import build_prompt, call_gemini
from backend.app.services.pdf_service import generate_pdf
from backend.app.utils.src.helper import extract_video_id

api_bp = Blueprint('api', __name__)
app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

@api_bp.route("/get-transcript", methods=["POST"])
def get_transcript():
    try:
        data = request.json
        youtube_url = data.get("url")
        preference = data.get("preference", "short-headings")
        if not youtube_url:
            return jsonify({"error": "YouTube URL is required"}), 400
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        transcript_data = fetch_transcript(video_id)
        prompt = build_prompt(transcript_data, preference)
        html_output = call_gemini(prompt)
        pdf_path = generate_pdf(html_output)

        return jsonify({
            "message": "Success",
            "video_id": video_id,
            "html_notes": html_output,
            "pdf_file": f"/download-pdf?path={pdf_path}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/download-pdf")
def download_pdf():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "PDF not found"}), 404
    return send_file(path, as_attachment=True, download_name="notes.pdf")
