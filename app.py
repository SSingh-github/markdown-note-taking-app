from flask import Flask, request, jsonify
import markdown
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
        # Get the uploads folder
        uploads_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(uploads_folder, exist_ok=True)  # Ensure the uploads folder exists

        # Extract file extension
        file_extension = file.filename.rsplit('.', 1)[1].lower()

        # Count existing files in the folder
        file_count = len([f for f in os.listdir(uploads_folder) if os.path.isfile(os.path.join(uploads_folder, f))])

        # Generate new filename
        new_filename = f"example_{file_count + 1}.{file_extension}"
        file_path = os.path.join(uploads_folder, new_filename)

        # Save the file
        file.save(file_path)

        return jsonify({
            "message": "File uploaded successfully",
            "original_name": file.filename,
            "stored_name": new_filename,
            "path": file_path
        }), 201

    return jsonify({"error": "Invalid file type. Only Markdown files are allowed."}), 400

# Define the uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Function to find file based on ID
def find_markdown_file_by_id(file_id):
    # Loop through files in the uploads folder
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(f"_{file_id}.md"):
            return os.path.join(UPLOAD_FOLDER, filename)
    return None

@app.route('/api/convert/<int:file_id>', methods=['GET'])
def convert_markdown_to_html(file_id):
    # Check if the file exists based on the given ID
    markdown_file_path = find_markdown_file_by_id(file_id)

    if not markdown_file_path:
        return jsonify({"error": "Markdown file not found for the given ID."}), 404

    # Read the content of the markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Convert the markdown content to HTML
    html_content = markdown.markdown(markdown_content)

    return jsonify({
        "html": html_content
    })