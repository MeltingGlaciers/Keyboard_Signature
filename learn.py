import keyboard
import time
import analyse

file = ''
entered = ""
events = []
password = ''


def setFile(path):
    global file
    file = open(path, "w")


def write_pressed_keys(e):
    global entered
    global events
    if (e.name == 'enter'):
        if (e.event_type == 'down'):
            string = next(keyboard.get_typed_strings(events))
            if (string != password):
                print("wrong")
            else:
                file.write(entered)
                file.write("\n")
        else:
            entered = ''
            events = []
    else:
        events.append(e)
        entered += (str(e.event_type) + " " +
                    str(e.name) + " " +
                    str(round(time.time() * 1000)) +
                    "\n")


def run():
    print("ready")
    keyboard.hook(write_pressed_keys)
    keyboard.wait('esc')
    file.close()
