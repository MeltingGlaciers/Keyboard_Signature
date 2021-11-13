import keyboard
import time
import analyse
import learn

path = "Y:\\Keyboard\\"
key_events = []
entered = ""

print("Login:")
login = input()
print("Password")
password = input()
learn.password=password
learn.setFile(path+login)
learn.run()
analyse.password=password
analyse.make_sign(login)
