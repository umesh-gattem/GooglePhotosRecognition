import os
import pickle
from pathlib import Path

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
album_service = service.albums().list(pageSize=50).execute()
print(album_service.get('nextPageToken'))
items = album_service.get('albums', [])
count = 0
for item in items:
    # print(item["title"])
    count+=1
print(count)
