from flask import Flask, render_template, request, redirect, url_for
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

app = Flask(__name__)

# Replace 'credentials.json' with the path to your Google service account credentials file
SERVICE_ACCOUNT_FILE = '/workspaces/drive_upload/instant-edudoc.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Function to upload file to Google Drive
def upload_to_drive(file_path, folder_id):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID:', file.get('id'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join('uploads', file.filename))
            folder_id = '1e62wkTIGOtBT5fmlbnaLIAomVQwjc73X'  # Replace with the actual folder ID of your "Edudocs" folder
            upload_to_drive(os.path.join('uploads', file.filename), folder_id)
            return 'File uploaded successfully!'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
