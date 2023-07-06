import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes required for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Set up the authentication flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
credentials = flow.run_local_server(port=0)

# Build the Google Drive service
service = build('drive', 'v3', credentials=credentials)

# Define the folder ID of the folder in your Google Drive
folder_id = '1d_xVnygdkZUvn5lvOSO9IqdUCGAH2SA-lVBz1QERhKUTryVaM9g7Ss-sB9VS5W8auF1KLaWy'

# Retrieve the list of files in the folder
results = service.files().list(q=f"'{folder_id}' in parents",
                               orderBy='modifiedTime desc',
                               pageSize=1,
                               fields='files(name, id)').execute()
files = results.get('files', [])

if len(files) > 0:
    file = files[0]
    file_name = file['name']
    file_id = file['id']

    # Download the file
    request = service.files().get_media(fileId=file_id)
    response = request.execute()

    # Save the file to the local directory
    with open(file_name, 'wb') as f:
        f.write(response)
    print(f'Newest file "{file_name}" downloaded successfully.')
else:
    print('No files found in the specified folder.')
