from flask import Flask, render_template, request, send_file
import os
import zipfile
from io import BytesIO
from caf_to_mp3 import convert_caf_to_mp3
from werkzeug.utils import secure_filename
import logging
import shutil  # Add this import

# Create Flask app instance first
app = Flask(__name__)

# Then configure it
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size per file

# Configure upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = os.path.expanduser('~/Downloads')  # This resolves to the user's Downloads folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Add after app creation
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files[]' not in request.files:
        logging.error('No files in request')
        return 'No files uploaded', 400
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        logging.error('No files selected')
        return 'No files selected', 400

    # If only one file, convert and return directly
    if len(files) == 1:
        file = files[0]
        if not file.filename.endswith('.caf'):
            logging.error(f'Invalid file type: {file.filename}')
            return 'Please upload only .caf files', 400
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            logging.info(f'Saving file: {input_path}')
            file.save(input_path)
            
            # Create the output path directly in Downloads
            downloads_path = os.path.expanduser('~/Downloads')
            output_filename = os.path.splitext(filename)[0] + '.mp3'
            output_path = os.path.join(downloads_path, output_filename)
            
            logging.info(f'Converting file to: {output_path}')
            if convert_caf_to_mp3(input_path, output_path):
                logging.info(f'Conversion successful. File saved to: {output_path}')
                
                # Verify file exists
                if os.path.exists(output_path):
                    logging.info(f'Verified file exists at: {output_path}')
                    return send_file(output_path, 
                                   as_attachment=True,
                                   download_name=output_filename)
                else:
                    logging.error(f'File not found at expected location: {output_path}')
                    return 'Conversion failed - file not found', 500
            else:
                logging.error('Conversion failed')
                return 'Conversion failed', 500
        except Exception as e:
            logging.error(f'Error during conversion: {str(e)}')
            return f'Error: {str(e)}', 500
        finally:
            # Cleanup
            if os.path.exists(input_path):
                os.remove(input_path)

    # For multiple files, create a zip
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            if not file.filename.endswith('.caf'):
                continue
            
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], 
                                     os.path.splitext(filename)[0] + '.mp3')
            
            try:
                file.save(input_path)
                if convert_caf_to_mp3(input_path, output_path):
                    zf.write(output_path, os.path.basename(output_path))
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
    
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='converted_files.zip'
    )

if __name__ == '__main__':
    app.run(debug=True) 