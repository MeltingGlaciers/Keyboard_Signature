import keyboard
import time
import analyse
import learn
import database

path = "Y:\\Keyboard\\"
key_events = []
entered = ""

def log_in(login):
    print('Sign in')
    print("Password")
    password = input()
    if not database.password_equality(login, password):
        print('Invalid credentials')
        return -1

    learn.password = password
    learn.setFile(path + login)
    learn.run()
    analyse.password = password
    vector = analyse.make_sign(login)
    if database.sign_equality(login,vector):
        print('Success')
    else:
        print('Not Success(')

def sign_up(login):
    print('Sign up')
    print("Password")
    password = input()
    learn.password = password
    learn.setFile(path + login)
    learn.run()
    analyse.password = password
    analyse.save_sign(login,analyse.make_sign(login))

print("Login:")
login = input()
if database.isExist(login) :
    log_in(login)
else:
    sign_up(login)


