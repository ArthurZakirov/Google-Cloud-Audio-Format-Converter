from pydub import AudioSegment
import os
import argparse
import tqdm
import dotenv

from src.data.google_drive_utils import list_files_in_directory, get_folder_id_by_path
from src.data.audio_processor import download_file_from_gdrive, convert_m4a_to_mp3, upload_file_to_gdrive

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

parser = argparse.ArgumentParser()
parser.add_argument("--raw_data_dir", default='/Learning/Voice Notes')
parser.add_argument("--processed_data_dir", default='/Learning/Voice Notes mp3')

args = parser.parse_args()

def main(args):

    dotenv.load_dotenv()
    token_path = os.getenv("GOOGLE_TOKEN_PATH")
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    service = build("drive", "v3", credentials=creds)

    files_and_folders = list_files_in_directory(service, args.raw_data_dir)

    for file in tqdm.tqdm(files_and_folders):
        if file["name"].endswith('.m4a'):

            m4a_io = download_file_from_gdrive(service, file["id"])
            mp3_io = convert_m4a_to_mp3(m4a_io)

            folder_id = get_folder_id_by_path(service=service, path=args.processed_data_dir)
            mp3_file_name = file["name"].replace(".m4a", ".mp3")

            upload_file_to_gdrive(
                service=service, 
                file_name=mp3_file_name, 
                mp3_io=mp3_io, 
                folder_id=folder_id
            )
            # Export as MP3

if __name__ == "__main__":
    main(args)
