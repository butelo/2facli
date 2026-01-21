[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/butelo/2facli)
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

### License

MIT

## Storage

Secrets are stored locally in `~/.2fa_secrets.json`.
**Warning**: This file is not encrypted by default. Ensure your computer is secure.
