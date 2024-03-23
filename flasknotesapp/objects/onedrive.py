#pip install msal
#video https://www.youtube.com/watch?v=1Jyd7SA-0kI&t=141s
#possible https://www.youtube.com/watch?v=oW1SJxGiaZA
import webbrowser
import requests
from msal import PublicClientApplication

APPLICATION_ID = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
CLIENT_SECRET = 'ZyD8Q~cyR5CAFFQat2ZvtTcnUJB3BJmCPj2FbdoR'
authority_url = 'https://login.microsoftonline.com/consumers/'

base_url = 'https://graph.microsoft.com/v1.0/'
endpoint = base_url + 'me'

SCOPES = ['User.Read']

app = PublicClientApplication(
    APPLICATION_ID,
    authority=authority_url
)

# accounts = app.get_accounts()
# if accounts:
#     app.acquire_token_silent(scopes=SCOPES, account=accounts[0])

flow = app.initiate_device_flow(scopes=SCOPES)
print(flow)
print(flow['message'])
webbrowser.open(flow['verification_uri'])

result = app.acquire_token_by_device_flow(flow)
access_token_id = result['access_token']
headers = {'Authorization': 'Bearer ' + access_token_id}

endpoint = base_url + 'me'
response = requests.get(endpoint, headers=headers)
print(response)
print(response.json())