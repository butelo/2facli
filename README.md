# 2FA CLI Tool

A simple terminal-based 2FA authenticator app (TOTP) that behaves like Google Authenticator or Authy, but in your terminal.

## Features

- **Generate Codes**: Generates time-based codes refreshing every 30 seconds.
- **Add Accounts**:
    - Scan QR code from a PNG image file.
    - Read QR code or Secret/URI from Clipboard.
    - Manually enter Secret or URI.
- **List Accounts**: View all codes in a real-time updating table.
- **Get Code**: Retrieve a specific code and automatically copy it to the clipboard.

## Installation

1.  **Dependencies**:
    This tool requires Python 3.
    It also relies on `zbar` for QR code decoding.

    **macOS**:
    ```bash
    brew install zbar
    ```

    **Linux (Ubuntu/Debian)**:
    ```bash
    sudo apt-get install libzbar0
    ```

2.  **Python Packages**:
    Install the required Python libraries:
    ```bash
    pip install typer pyotp pyperclip pyzbar pillow rich
    ```

## Usage

Run the script using python:

```bash
python 2fa.py --help
```

### Adding an Account

**From a QR Code Image:**
```bash
python 2fa.py add --image path/to/qr.png
```

**From Clipboard (QR Image or URI/Secret text):**
```bash
python 2fa.py add --clipboard
```

**From Manual Secret:**
```bash
python 2fa.py add --name "MyAccount" --secret "JBSWY3DPEHPK3PXP"
```

### Listing Codes

View all your codes (updates automatically with `--watch`):
```bash
python 2fa.py list --watch
```

### Getting a Code

Get a code for a specific account (fuzzy search) and copy to clipboard:
```bash
python 2fa.py get google
```

### Deleting an Account

```bash
python 2fa.py delete "MyAccount"
```

## Storage

Secrets are stored locally in `~/.2fa_secrets.json`.
**Warning**: This file is not encrypted by default. Ensure your computer is secure.
