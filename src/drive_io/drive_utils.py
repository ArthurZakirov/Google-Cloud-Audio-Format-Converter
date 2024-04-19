import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


def load_service():
    """
    Load the Google Drive service using the provided credentials.

    Returns:
        service (googleapiclient.discovery.Resource): The Google Drive service object.
    """
    token_path = os.getenv("GOOGLE_TOKEN_PATH")
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    service = build("drive", "v3", credentials=creds)
    return service


def list_files_in_directory(service, path):
    """
    Lists all files and folders in a given directory.

    Args:
        service: The Google Drive service object.
        path: The path of the directory to list files from.

    Returns:
        A list of dictionaries, where each dictionary represents a file or folder.
        Each dictionary contains the following keys:
        - 'name': The name of the file or folder.
        - 'id': The ID of the file or folder.
        - 'mimeType': The MIME type of the file or folder.
    """
    folder_id = get_folder_id_by_path(service, path)
    query = f"'{folder_id}' in parents and trashed=false"
    response = (
        service.files()
        .list(q=query, fields="nextPageToken, files(id, name, mimeType)")
        .execute()
    )

    items = response.get("files", [])
    files_and_folders = [
        {"name": item["name"], "id": item["id"], "mimeType": item["mimeType"]}
        for item in items
    ]

    return files_and_folders


def get_folder_id_by_path(service, path):
    """
    Retrieves the folder ID of a given path in Google Drive.

    Args:
        service: The Google Drive service object.
        path (str): The path of the folder in Google Drive.

    Returns:
        str: The folder ID of the specified path.

    Raises:
        ValueError: If the path does not start with '/' or if no folder with the specified name is found.

    """
    if path == "/":
        return "root"
    elif not path.startswith("/"):
        raise ValueError("Path must start with '/'.")

    folder_id = "root"
    parts = path.strip("/").split("/")

    for part in parts:
        response = (
            service.files()
            .list(
                q=f"mimeType='application/vnd.google-apps.folder' and name='{part}' and '{folder_id}' in parents and trashed=false",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        files = response.get("files", [])

        if not files:
            raise ValueError(f"No folder with name '{part}'")
        folder_id = files[0]["id"]

    return folder_id
