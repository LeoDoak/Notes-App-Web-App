class Groups:
    """A class represemtiomg groups created by user

    Parameters:

    Returns:
    str: group_name
    bool: is_private
    """
    def __init__(self, group_id: int, group_name: str, is_private: bool):

        self.group_id = group_id
        self.group_name = group_name
        self.is_private = is_private


SAMPLE_GROUP = [
    Groups(12, 'Mat 111', True),
    Groups(46, 'Oceanography', False),
    Groups(20, 'Programming Test', False),
    Groups(9, 'Group 11 files', True),
    Groups(7, 'Computer Graphics', False),
]
