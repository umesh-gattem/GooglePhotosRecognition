import os
import pickle

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Setup the Photo v1 API
# SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly',
#           "https://www.googleapis.com/auth/photoslibrary.sharing"]

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.sharing"]
creds = None
if (os.path.exists("token.pickle")):
    with open("token.pickle", "rb") as tokenFile:
        creds = pickle.load(tokenFile)
if not creds or not creds.valid:
    if (creds and creds.expired and creds.refresh_token):
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '//samples/GooglePhotos.json', scopes=SCOPES)
        # flow = InstalledAppFlow.from_client_secrets_file('GooglePhotos.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as tokenFile:
        pickle.dump(creds, tokenFile)
service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# results = service.albums().list(pageSize=40).execute()
#
# items = results.get('albums', [])
# if not items:
#     print('No albums found.')
# else:
#     print('Albums:')
#     for item in items:
#         print(f'{item["title"]} , ({item["id"]})')

results = service.albums().list(pageSize=40).execute()

items = results.get('albums', [])
if not items:
    print('No albums found.')
else:
    print('Albums:')
    for item in items:
        media_files = service.mediaItems().search(body={"pageSize": 100, 'albumId': item['id']}).execute()['mediaItems']
        print(len(media_files))
        # print(item)
        print(f'{item["title"]} , ({item["id"]}), {len(media_files)}')
        # result = requests.get(item['productUrl']).content
        # print(result)
        # print(len(result))
        # plt.imread()
        # plt.show()

