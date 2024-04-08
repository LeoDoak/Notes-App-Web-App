import requests
from onedrive import generate_access_token, GRAPH_API_ENDPOINT 
app_id = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
scopes = ['Files.ReadWrite']
access_token = generate_access_token(app_id, scopes)

resultant_token=access_token["access_token"]
print(resultant_token)
"""
The `create_folder` function is designed to create a new folder in the user's OneDrive by making a POST request to the Microsoft Graph API.
It takes an `access_token` for authentication, a `parent_id` parameter that is not utilized in its current implementation (implying the new folder is created at the root directory), and a `folder_name` for the name of the new folder.
The function sets up the necessary HTTP headers, including an incorrect reference to `resultant_token` instead of the provided `access_token` for authorization, and `Content-Type` set to `application/json`.
It constructs a JSON payload specifying the folder's name and indicating it's a folder by including an empty `folder` object. 
After making the API call, it checks for errors using `response.raise_for_status()` and returns the JSON response from the API, which contains details of the newly created folder." 
There's a noted mistake in the code where `resultant_token` should be replaced with `access_token` for proper authorization.
"""
def create_folder(access_token, parent_id, folder_name):
    url = f"https://graph.microsoft.com/v1.0/me/drive/root/children"
    headers = {
        "Authorization": "Bearer " + resultant_token,
        "Content-Type": "application/json",
    }
    data = {"name": folder_name, "folder": {}}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


"""
The `move_file` function facilitates moving a file within a user's OneDrive to a different folder by leveraging the Microsoft Graph API. 
It requires parameters including an `access_token` for authentication, the `file_id` of the file to be moved, and the `target_folder_id` where the file should be relocated. 
The function constructs a specific URL targeting the file to be moved, prepares the HTTP headers  and specifies the new parent folder's ID in the request body. 
After sending a POST request to the Graph API's move endpoint for the item, it checks for and raises any HTTP errors before returning the API's JSON response, which typically includes details of the moved file. 

"""

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


