import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Setup the Photo v1 API

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.sharing"]
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
# # Call the Photo v1 API
# print(service.mediaItems().search().__dict__)
results = service.mediaItems().search(body={"pageSize": 10, "pageToken": '',
                                            "filters": {"contentFilter":
                                                            {"includedContentCategories": ["PEOPLE"]}}}).execute()
print(results['mediaItems'])
# items = results.get('mediaItems', [])
# for item in items:
#     # if item["mimeType"] == 'image/jpeg':
#     #     image = Image.open(BytesIO(requests.get(item['baseUrl']).content))
#     #     image.show()
#     with open("Photos/" + item['filename'], 'wb') as f:
#         f.write(requests.get(item['baseUrl']).content)
#         if item["mimeType"] == 'image/jpeg':
#             image = Image.open("Photos/" + item['filename'])
#             image.show()
