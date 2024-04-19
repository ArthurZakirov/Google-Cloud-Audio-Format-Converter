"""
This module provides functions for downloading and uploading files to Google Drive.

The main functions in this module are:
- download_file_from_gdrive: Downloads a file from Google Drive and returns a file-like object containing the downloaded file data.
- upload_file_to_gdrive: Uploads a file to Google Drive and returns the ID of the uploaded file.

These functions rely on the Google Drive API and require a valid Google Drive service object to be passed as an argument.

Example usage:
service = create_drive_service()  # Create a Google Drive service object
file_id = "abc123"  # ID of the file to be downloaded/uploaded
file_io = download_file_from_gdrive(service, file_id)  # Download the file
upload_file_to_gdrive(service, "new_file.mp3", file_io)  # Upload the file

Note: The Google Drive API credentials and authentication process are not covered in this module and should be handled separately.
"""

from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload


def download_file_from_gdrive(service, file_id):
    """
    Downloads a file from Google Drive.

    Args:
        service: The Google Drive service object.
        file_id (str): The ID of the file to be downloaded.

    Returns:
        io.BytesIO: The file-like object containing the downloaded file data.
    """
    request = service.files().get_media(fileId=file_id)
    file_io = BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)

    done = False
    while done is False:
        _, done = downloader.next_chunk()

    file_io.seek(0)
    return file_io


def upload_file_to_gdrive(service, file_name, output_file_io, folder_id="root"):
    """
    Uploads a file to Google Drive.

    Args:
        service: The Google Drive service object.
        file_name (str): The name of the file to be uploaded.
        mp3_io: The file-like object containing the MP3 data to be uploaded.
        folder_id (str, optional): The ID of the folder in Google Drive where the file should be uploaded.
            Defaults to "root".

    Returns:
        str: The ID of the uploaded file in Google Drive.
    """
    file_metadata = {
        "name": file_name,
        "mimeType": "audio/mpeg",
        "parents": [folder_id],
    }

    media = MediaIoBaseUpload(output_file_io, mimetype="audio/mpeg", resumable=True)
    uploaded_file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return uploaded_file.get("id")
