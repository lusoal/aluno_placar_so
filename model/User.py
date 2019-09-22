
class User(object):

    def __init__(self, user, id = None):
        self.username = user
        self.id = id
        
    def __repr__(self):
        return f"{self.username}, {self.password}"
    