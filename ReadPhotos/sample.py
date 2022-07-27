"""
Shows basic usage of the Photos v1 API.
Creates a Photos v1 API service and prints the names and ids of the last 10 albums
the user has access to.
"""
from __future__ import print_function
import os
import pickle
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_httplib2  # This gotta be installed for build() to work



from oauth2client import client # Added
from oauth2client import tools # Added
from oauth2client.file import Storage # Added

def get_authenticated_service(): # Modified
    credential_path = os.path.join('./', 'credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)

# Setup the Photo v1 API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']
creds = None
if(os.path.exists("token.pickle")):
    with open("token.pickle", "rb") as tokenFile:
        creds = pickle.load(tokenFile)
if not creds or not creds.valid:
    if (creds and creds.expired and creds.refresh_token):
        creds.refresh(Request())
    else:
        credential_path = os.path.join('./', 'credential_sample.json')
        store = Storage(credential_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("GooglePhotos.json", SCOPES)
            creds = tools.run_flow(flow, store)
        # Using a JSON string
        with open('credential_sample.json', 'w') as outfile:
            outfile.write(creds)
        # flow = InstalledAppFlow.from_client_secrets_file('GooglePhotos.json', SCOPES)
        # creds = flow.run_console(host="localhost", port = 0, open_browser=True)
    # with open("credential_sample.json", "wb") as tokenFile:
    #     pickle.dump(creds, tokenFile)
print(creds)
service = build('photoslibrary', 'v1', credentials = creds)

# Call the Photo v1 API
results = service.albums().list(
    pageSize=10, fields="nextPageToken,albums(id,title)").execute()
items = results.get('albums', [])
if not items:
    print('No albums found.')
else:
    print('Albums:')
    for item in items:
        print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))