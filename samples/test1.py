from google_auth_oauthlib.flow import InstalledAppFlow

# scopes =['https://www.googleapis.com/auth/photoslibrary']
# scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
scopes = ['https://www.googleapis.com/auth/userinfo.profile']
# scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
flow = InstalledAppFlow.from_client_secrets_file(
    '../ReadPhotos/GooglePhotos.json',
    scopes=scopes)

flow.run_local_server(port=0)

session = flow.authorized_session()

profile_info = session.get(
    'https://www.googleapis.com/userinfo/v2/me').json()

print(profile_info)
