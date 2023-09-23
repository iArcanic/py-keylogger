# py-keylogger
![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Description
This `py-keylogger` is a Python application that functions as a keylogger, recording keystrokes made on a computer keyboard and saving them to log files. The script offers the choice to encrypt these log files to protect information that the user may deem sensitive.

## Features
- Records key presses and saves them to log files to a `keylogs` folder on the user's home directory.
- Each log file is uniquely named with a timestamp.
- Supports log file encryption via a specified passphrase for added security.
- Supports log file decryption via a specified passphrase (CURRENTLY UNDER DEVELOPMENT).
- Cross-platform compatibility (Windows, macOS, Linux)
- Automatic keyboard layout detection

## Prerequisites
Before running this script, make sure you have the following:

- Python 3.x installed on your system.
- Required Python packages: `cryptography`, `pynput`.

You can install the required packages using `pip`:

```bash
pip install cryptography pynput
```

## Usage
### Basic usage
To run the keylogger without encryption:
```bash
sudo python3 keylogger.py
```
NB: Make sure you run this script as root or give your terminal client the required priviledges for keyboard monitoring.

To run the keylogger with the log file encryption:
```bash
sudo python3 keylogger.py --encrypt --passphrase "YourSecretPassphrase"
```
### Options
- `--encrypt`: Enable log file encryption.
- `--passphrase`: Specify the encryption passphrase.

## Contribution
Feel free to contribute to this project by creating issues or submitting pull requests.

## Acknowledgements
Special thanks to the developers of these Python packages:
- [pynut](https://pypi.org/project/pynput/) – Allows to control and monitor input devices.
- [cryptography](https://pypi.org/project/cryptography/) – Provides common cryptographic algorithms such asymmetric ciphers, message digests, and key derivation functions for encryption purposes.
