import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.API import credential_managing

def download_file(real_file_id):

    creds = credential_managing.creds
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_id = real_file_id
        # pylint: disable=maybe-no-member
    request = service.files().export_media(fileId=file_id, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return file.getvalue()
