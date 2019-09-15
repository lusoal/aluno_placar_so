
class User(object):

    def __init__(self, user, password, id = None):
        self.username = user
        self.password = password
        self.id = id
        
    def __repr__(self):
        return f"{self.username}, {self.password}"
    