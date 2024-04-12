import os.path
import urllib
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
#SCOPES_ROOT = "https://www.googleapis.com"

parser = argparse.ArgumentParser()
parser.add_argument("--token_path", default="config/mensmaxxing_gdrive_config.json")
parser.add_argument("--credentials_path", default="config/mensmaxxing_gdrive_credentials.json")
parser.add_argument("--scopes", nargs="+", default=["https://www.googleapis.com/auth/drive"])
args = parser.parse_args()



def main(args):
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  token_path = args.token_path
  credentials_path = args.credentials_path
  SCOPES = args.scopes
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, "w") as token:
      token.write(creds.to_json())


if __name__ == "__main__":
  main(args)