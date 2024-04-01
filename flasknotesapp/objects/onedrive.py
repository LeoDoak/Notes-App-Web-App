import webbrowser
from datetime import datetime
import json
import os
import msal

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

user_code = "placement_code"

def generate_access_token(app_id, scopes):
    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists('ms_graph_api_token.json'):
        access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
        token_detail = json.load(open('ms_graph_api_token.json',))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if datetime.now() > token_expiration:
            os.remove('ms_graph_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authetnicate your accoutn as usual
        flow = client.initiate_device_flow(scopes=scopes)
        user_code = flow['user_code']
        print('user_code: ' + user_code)
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

if __name__ == '__main__':
    ...


def get_user_code():
    return user_code

# #pip install msal
# #video https://www.youtube.com/watch?v=1Jyd7SA-0kI&t=141s
# #possible https://www.youtube.com/watch?v=oW1SJxGiaZA
# import webbrowser
# import requests
# from msal import PublicClientApplication

# APPLICATION_ID = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
# CLIENT_SECRET = 'ZyD8Q~cyR5CAFFQat2ZvtTcnUJB3BJmCPj2FbdoR'
# authority_url = 'https://login.microsoftonline.com/consumers/'

# base_url = 'https://graph.microsoft.com/v1.0/'
# endpoint = base_url + 'me'

# SCOPES = ['User.Read']

# app = PublicClientApplication(
#     APPLICATION_ID,
#     authority=authority_url
# )

# # accounts = app.get_accounts()
# # if accounts:
# #     app.acquire_token_silent(scopes=SCOPES, account=accounts[0])

# flow = app.initiate_device_flow(scopes=SCOPES)
# print(flow)
# print(flow['message'])
# webbrowser.open(flow['verification_uri'])

# result = app.acquire_token_by_device_flow(flow)
# access_token_id = result['access_token']
# headers = {'Authorization': 'Bearer ' + access_token_id}

# endpoint = base_url + 'me'
# response = requests.get(endpoint, headers=headers)
# print(response)
# print(response.json())