from tinydb import TinyDB, Query

db_path = "Y:\\Keyboard\\db.json"
db = TinyDB(db_path)

class User:
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

def save(user: User):
    global db
    db.insert({'name': user.name, 'sign': user.sign})