class groups: 
# A class representing Groups created by user
    group_id: int
    group_name: str
    isPrivate: bool
    def __init__(self, id: int, group_name: str, isPrivate: bool):
        self.group_id = id
        self.group_name: group_name
        self.isPrivate: isPrivate


SAMPLE_GROUP = [
    groups(12,'Mat 111', True),
    groups(46,'Oceanography', False),
    groups(20,'Programming Test', False),
    groups(9,'Group 11 files', True),
    groups(7,'Computer Graphics', False),
]
