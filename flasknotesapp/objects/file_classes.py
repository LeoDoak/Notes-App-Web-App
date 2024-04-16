""" Module containing methods related to files"""

import re 


class File:
    """A class representing a File.

    A file has a unique identifier, a title, a list of tags,
    and a list of entities with whom the file is shared.
    """
    file_id: int
    title: str
    tags: list[str]
    shared_with: list[int]

    # Assuming shared_with is a list of UserIDs or GroupIDs for simplicity

    def __init__(self, file_id: int, title: str, filetype:str,
                 fileicon: str):
        self.file_id = file_id
        self.title = title
        self.filetype = filetype
        self.fileicon = fileicon

    def get_file_id(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.file_id

    def get_title(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.title

    def set_filetype(self):
        '''Summary: Sets the filetype from the file name 

        Paramters: 

        Returns: Nothing, sets the filetype to the filetype
        '''
        type = re.findall(r'[.][a-z]{3}', self.title)
        if type is None:
            self.filetype = folder
        self.filetype = type

    def get_filetype(self):
        '''Summary: returns the filetype

        Paramters: 

        Returns: 
        '''
        return self.filetype



    def set_file_icont(self):
        '''Summary: Sets the file icon to the correct icon, the correct file image address

        Paramters:

        Returns:
        '''
        self.fileicon = none




