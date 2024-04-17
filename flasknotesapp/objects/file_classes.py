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
        if '.' not in self.title:
            self.filetype = ['folder']
        else:
            type = re.findall(r'[.][a-z]{3}', self.title)
            self.filetype = type

    def get_filetype(self):
        '''Summary: returns the filetype

        Paramters:

        Returns:
        '''
        return str(self.filetype)

    def set_file_icon(self):
        '''Summary: Sets the file icon to the correct icon, the correct file image address

        Paramters:

        Returns:
        '''
        if self.filetype == ['.doc']:
            self.fileicon = "static/file_icons/docx_file_icon.png"
        if self.filetype == ['.jpg']:
            self.fileicon = "static/file_icons/jpeg_icon.png"
        if self.filetype == ['.pdf']:
            self.fileicon = "static/file_icons/pdf_icon.png"
        if self.filetype == ['folder']:
            self.fileicon = "static/file_icons/folder_icon.png"
        if self.filetype == ['.sas']:
            self.fileicon = "static/file_icons/sas_icon.png"
        if self.filetype == ['.csv']:
            self.fileicon = "static/file_icons/csv_icon.png"









