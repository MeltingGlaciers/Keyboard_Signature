import keyboard
import time
import analyse

password = "privet"
key_events = []
entered = ""

def record(e):
    global entered, key_events
    if (e.name!='enter'):
        key_events.append(e)
        entered += (str(e.event_type) + " " +
                    str(e.name) + " " +
                    str(round(time.time() * 1000)) +
                    "\n")

# while(True):
#     print("ready")
#     keyboard.hook(record)
#     keyboard.wait('enter')
#     string = next(keyboard.get_typed_strings(key_events))
#     if (string==password):
#         break
#     else:
#         print("wrong")
# entered = entered[:-1]
# print(analyse.analyse(entered))
