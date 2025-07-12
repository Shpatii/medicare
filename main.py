# from flask import Flask, request, render_template, make_response
# from flask_cors import CORS
# import os
# from logic.extract import extract_text_from_pdf, generate_medical_chronology

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/", methods=["GET"])
# def upload_form():
#     return render_template("upload.html")

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     try:
#         file = request.files.get("pdf")
#         if not file:
#             return "No file uploaded", 400

#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         text = extract_text_from_pdf(file_path)
#         chronology = generate_medical_chronology(text)

#         return render_template("result.html", summary=chronology)

#     except Exception as e:
#         return f"Server Error: {str(e)}", 500

# @app.route("/download/json", methods=["POST"])
# def download_json():
#     summary = request.form["summary"]
#     response = make_response(summary)
#     response.headers["Content-Disposition"] = "attachment; filename=summary.json"
#     response.mimetype = "application/json"
#     return response

# if __name__ == "__main__":
#     app.run(debug=True)
