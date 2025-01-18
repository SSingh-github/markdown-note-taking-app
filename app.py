from flask import Flask, request, jsonify

app = Flask(__name__)

import os


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'md'}

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Save the file directly in the uploads folder
        file_path = os.path.join(os.path.join(os.getcwd(), 'uploads'), file.filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            return jsonify({"error": f"A file named '{file.filename}' already exists."}), 409

        # Save the file
        file.save(file_path)

        return jsonify({"message": "File uploaded successfully", "path": file_path}), 201

    return jsonify({"error": "Invalid file type. Only Markdown files are allowed."}), 400

