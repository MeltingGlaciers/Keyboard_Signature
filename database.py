from tinydb import TinyDB, Query

db_path = "Y:\\Keyboard\\db.json"
db = TinyDB(db_path)

class User:
    def __init__(self, name, sign, password):
        self.name = name
        self.sign = sign
        self.password = password

def save(user: User):
    global db
    db.insert({'name': user.name, 'sign': user.sign, 'password': user.password})

def isExist(login):
    global db
    result = db.search(Query()['name']==login)
    return False if len(result)==0 else result

def password_equality(login,password):
    global db
    result = db.search(Query()['name'] == login)[0]
    return result['password'] == password

def sign_equality(login,vector):
    global db
    result = db.search(Query()['name'] == login)[0]
    user_vector = result['sign']
    for i in range(len(user_vector)):
        print(vector[i], user_vector[i])
        if (abs(vector[i] - user_vector[i]) > 0.3):
            return False
    return True

