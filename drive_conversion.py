"""
This module provides functionality to convert audio files from the Google Drive to MP3 format.

It uses the Google Drive API to access and manipulate files in Google Drive. The module supports converting
M4A audio files to MP3 format and uploading the converted files back to Google Drive.

Usage:
    - Set the `raw_data_dir` and `processed_data_dir` arguments to specify the source and destination directories
      in Google Drive.
    - Run the script to convert the M4A files in the `raw_data_dir` to MP3 format and upload them to the
      `processed_data_dir`.

Dependencies:
    - google-api-python-client
    - google-auth-httplib2
    - google-auth-oauthlib
    - tqdm
    - dotenv

Note: Before running the script, make sure to set up the necessary credentials and environment variables
for accessing the Google Drive API.

Author: Arthur Zakirov
"""

import os
import argparse
import tqdm
import dotenv

from src.drive_io.drive_utils import (
    load_service,
    list_files_in_directory,
    get_folder_id_by_path,
)
from src.drive_io.drive_sync import download_file_from_gdrive, upload_file_to_gdrive
from src.audio_conversion.convert import convert_m4a_to_mp3

dotenv.load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--input_data_dir", default="/Learning/Voice Notes")
parser.add_argument("--output_data_dir", default="/Learning/Voice Notes mp3")
parser.add_argument("--input_format", default=".m4a")
parser.add_argument("--output_format", default=".mp3")
args = parser.parse_args()


def main():

    service = load_service()
    files_and_folders = list_files_in_directory(service, args.input_data_dir)

    for file in tqdm.tqdm(files_and_folders):
        if file["name"].endswith(args.input_format):

            input_file_io = download_file_from_gdrive(service, file["id"])
            output_file_io = convert_m4a_to_mp3(input_file_io)

            folder_id = get_folder_id_by_path(
                service=service, path=args.output_data_dir
            )
            output_file_name = file["name"].replace(
                args.input_format, args.output_format
            )

            upload_file_to_gdrive(
                service=service,
                file_name=output_file_name,
                output_file_io=output_file_io,
                folder_id=folder_id,
            )


if __name__ == "__main__":
    main()
