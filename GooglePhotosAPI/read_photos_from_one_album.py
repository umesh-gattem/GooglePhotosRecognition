import os
import pickle

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly',
          "https://www.googleapis.com/auth/photoslibrary.sharing"]
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as tokenFile:
        creds = pickle.load(tokenFile)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('GooglePhotos.json', scopes=SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as tokenFile:
        pickle.dump(creds, tokenFile)
service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# album_service = service.albums().list(pageSize=1).execute()
#
# items = album_service.get('albums', [])
# for item in items:
next_page_token = 'Start'
total_media_file = 0
total_image_files = 0
album_id = 'AOzt70o5wzJ46rL0iUSNYFacybvN4uSN9OKACcfyyJyEtvV2YFMQ6QMQefiMVQumbq_A-64zj4q9'
while next_page_token:
    next_page_token = '' if next_page_token == 'Start' else next_page_token
    media_service = service.mediaItems().search(body={"pageSize": 50,
                                                      'albumId': album_id,
                                                      "pageToken": next_page_token}).execute()
    media_files = media_service['mediaItems']
    for media_item in media_files:
        if media_item["mimeType"] == 'image/jpeg':
            filename = f"AlbumPhotos/Santhosh/{media_item['filename']}"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as f:
                f.write(requests.get(media_item['baseUrl']).content)
            total_image_files += 1
    total_media_file += len(media_files)
    next_page_token = media_service.get('nextPageToken', '')
    print(f"Loaded {total_media_file} files")
# print(f'Album : {item["title"]} , contains {total_media_file} media '
#       f'files which has {total_image_files} image files')
