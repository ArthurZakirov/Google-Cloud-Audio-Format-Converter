from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload
from pydub import AudioSegment
from googleapiclient.http import MediaIoBaseUpload



def download_file_from_gdrive(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_io = BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    file_io.seek(0)
    return file_io


def convert_m4a_to_mp3(m4a_io):
    # Load M4A file from BytesIO
    audio = AudioSegment.from_file(m4a_io, format='m4a')
    
    # Convert to MP3 and store in a BytesIO object
    mp3_io = BytesIO()
    audio.export(mp3_io, format='mp3')
    mp3_io.seek(0)
    
    return mp3_io


def upload_file_to_gdrive(service, file_name, mp3_io, folder_id='root'):
    file_metadata = {
        'name': file_name,
        'mimeType': 'audio/mpeg',
        'parents': [folder_id]
    }
    
    media = MediaIoBaseUpload(mp3_io, mimetype='audio/mpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    