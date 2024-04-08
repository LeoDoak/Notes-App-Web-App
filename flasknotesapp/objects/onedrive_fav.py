import requests
from onedrive import generate_access_token
app_id = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
scopes = ['Files.ReadWrite']
access_token = generate_access_token(app_id, scopes)
resultant_token = access_token["access_token"]
print(resultant_token)


def create_folder(access_token, parent_id, folder_name):
    """The `create_folder` function creates a new folder on a user's OneDrive via the Microsoft Graph API, 
       
        using an `access_token` for authentication. It posts a request with the desired `folder_name`, 
        handles any errors, and returns the API's response. 
    """
    url = f"https://graph.microsoft.com/v1.0/me/drive/root/children"
    headers = {
        "Authorization": "Bearer " + resultant_token,
        "Content-Type": "application/json",
    }
    data = {"name": folder_name, "folder": {}}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def move_file(access_token, file_id, target_folder_id):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/move"
    headers = {
        "Authorization": "Bearer " + resultant_token,
        "Content-Type": "application/json",
    }
    data = {"parentReference": {"id": target_folder_id}}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


# Example usage
access_token = generate_access_token(app_id, scopes)
parent_folder_id = "root"  # ID of the parent folder where you want to create the favorite folder
favorite_folder_name = "Favorites"


# Create a favorite folder
favorite_folder = create_folder(access_token, parent_folder_id, favorite_folder_name)
favorite_folder_id = favorite_folder["id"]
