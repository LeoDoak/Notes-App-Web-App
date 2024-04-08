"""
This module contains functions for interacting with Microsoft OneDrive.
It provides functionality to create new folders and move files within OneDrive.
"""


import requests, onedrive

# Import the 'onedrive' module's 'generate_access_token' function
# This assumes that the 'onedrive' module is correctly installed and available in the PYTHONPATH.
from onedrive import generate_access_token

# Constants should be in uppercase
APP_ID = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
SCOPES = ['Files.ReadWrite']

# Generating an access token and printing it
ACCESS_TOKEN = generate_access_token(APP_ID, SCOPES)['access_token']
print(ACCESS_TOKEN)


def create_folder(token, folder_name):
    """
    Creates a new folder on a user's OneDrive via the Microsoft Graph API,
    using an access token for authentication. Posts a request with the desired folder name,
    handles errors, and returns the API's response.

    Args:
        token: The access token for authentication.
        folder_name: The name of the folder to be created.

    Returns:
        The response from the OneDrive API as a JSON object.
    """
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    # Breaking down the request for readability
    response = requests.post(
        url,
        headers=headers,
        json={"name": folder_name, "folder": {}},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def move_file(token, file_id, target_id):
    """
    Moves a file identified by file_id within the user's OneDrive to a specified target folder id.

    Args:
        token: The access token for authentication.
        file_id: The unique identifier for the file to be moved.
        target_id: The target folder's unique identifier where the file should be moved.

    Returns:
        The response from the OneDrive API as a JSON object.
    """
    # Breaking down the URL for readability
    url = (
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/move"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    # Breaking down the request for readability
    response = requests.post(
        url,
        headers=headers,
        json={"parentReference": {"id": target_id}},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


# Example usage
# Use uppercase for constants
PARENT_FOLDER_ID = "root"
FOLDER_NAME = "Favorites"

# Create a folder
new_folder = create_folder(ACCESS_TOKEN, FOLDER_NAME)
print(new_folder["id"])
