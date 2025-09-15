from flask import Flask
from flask_cors import CORS
from backend.app.routes.api import api_bp
from backend.app.routes.web import web_bp
import os

frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

app = Flask(
    __name__,
    template_folder=os.path.join(frontend_path, "templates"),
    static_folder=os.path.join(frontend_path, "static")
)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
