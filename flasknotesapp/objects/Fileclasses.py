""" Module containing methods related to files"""



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

    def __init__(self, file_id: int, title: str, tags: list[str],
                 shared_with: list[int]):
        self.file_id = file_id
        self.title = title
        self.tags = tags
        self.shared_with = shared_with

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

    def get_tags(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.tags

    def get_shared_with(self):
        """Summary or Description of the function

        Parameters:

        Returns:
        """
        return self.shared_with


# A sample list of files to play with.
SAMPLE_FILES = [
    File(1, 'Report.pdf', ['report', 'pdf', 'finance'], [123456789]),
    File(2, 'Presentation.pptx', ['slides', 'meeting'], [222222222]),
    File(3, 'Image.png', ['picture', 'sample'], [186918691]),
]
