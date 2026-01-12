#!/usr/bin/env python3
import json
import os
import time
from typing import Optional
from pathlib import Path
import typer
import pyotp
import pyperclip
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Optional imports for QR and Image handling
try:
    from pyzbar.pyzbar import decode
    from PIL import Image, ImageGrab, ImageEnhance
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
except OSError:
    # This often happens if the zbar shared library is missing
    QR_AVAILABLE = False

app = typer.Typer(help="A terminal 2FA authenticator app.")
console = Console()

SECRETS_FILE = Path.home() / ".2fa_secrets.json"

def load_secrets():
    if not SECRETS_FILE.exists():
        return {"accounts": []}
    try:
        with open(SECRETS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"accounts": []}

def save_secrets(data):
    with open(SECRETS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def parse_otpauth_uri(uri: str):
    """Parse otpauth://totp/Label?secret=...&issuer=..."""
    try:
        parsed = pyotp.parse_uri(uri)
        return {
            "name": parsed.name,
            "secret": parsed.secret,
            "issuer": parsed.issuer
        }
    except Exception as e:
        return None

def extract_qr_from_image(image):
    if not QR_AVAILABLE:
        rprint("[red]Error: QR code libraries (pyzbar/zbar) not available.[/red]")
        rprint("Please install zbar (e.g., `brew install zbar` or `sudo apt-get install libzbar0`)")
        return None
    
    # List of transformations to try
    # 1. Original
    # 2. RGB (if RGBA)
    # 3. Grayscale
    # 4. High Contrast
    # 5. Binary
    
    candidates = [image]
    
    if image.mode == 'RGBA':
        candidates.append(image.convert('RGB'))
        
    gray = image.convert('L')
    candidates.append(gray)
    
    enhancer = ImageEnhance.Contrast(gray)
    candidates.append(enhancer.enhance(2.0))
    
    # Simple binarization
    candidates.append(gray.point(lambda p: 255 if p > 128 else 0))

    for img in candidates:
        try:
            decoded = decode(img)
            if decoded:
                return decoded[0].data.decode("utf-8")
        except Exception:
            continue
            
    return None

@app.command()
def add(
    name: str = typer.Option(None, "--name", "-n", help="Name for the account"),
    secret: str = typer.Option(None, "--secret", "-s", help="The secret key (base32)"),
    uri: str = typer.Option(None, "--uri", "-u", help="The otpauth URI"),
    image: str = typer.Option(None, "--image", "-i", help="Path to a QR code image file"),
    clipboard: bool = typer.Option(False, "--clipboard", "-c", help="Read from clipboard (URI, Secret, or QR Image)"),
):
    """Add a new 2FA account."""
    data = load_secrets()
    new_account = {}

    # 1. Try Clipboard
    if clipboard:
        # Check for image in clipboard first
        if QR_AVAILABLE:
            try:
                clip_img = ImageGrab.grabclipboard()
                if isinstance(clip_img, Image.Image):
                    decoded_uri = extract_qr_from_image(clip_img)
                    if decoded_uri:
                        rprint("[green]Found QR code in clipboard![/green]")
                        uri = decoded_uri
            except Exception:
                pass # Fallback to text
        
        # Check for text in clipboard if no image found or processed
        if not uri and not secret:
            clip_text = pyperclip.paste().strip()
            if clip_text:
                if clip_text.startswith("otpauth://"):
                    uri = clip_text
                    rprint("[green]Found otpauth URI in clipboard![/green]")
                else:
                    # Assume it might be a secret if it looks like one (simple heuristic)
                    if " " not in clip_text and len(clip_text) > 8: 
                        secret = clip_text
                        rprint("[green]Found potential secret in clipboard![/green]")

    # 2. Try Image File
    if image:
        if not os.path.exists(image):
            rprint(f"[red]File not found: {image}[/red]")
            return
        if QR_AVAILABLE:
            try:
                img = Image.open(image)
                decoded_uri = extract_qr_from_image(img)
                if decoded_uri:
                    uri = decoded_uri
                else:
                    rprint("[red]No QR code found in image.[/red]")
                    return
            except Exception as e:
                rprint(f"[red]Error reading image: {e}[/red]")
                return
        else:
             rprint("[red]QR scanning not available. Install zbar.[/red]")
             return

    # 3. Process URI or Secret
    if uri:
        parsed = parse_otpauth_uri(uri)
        if parsed:
            new_account = parsed
            # Allow overriding name
            if name:
                new_account["name"] = name
        else:
            rprint("[red]Invalid otpauth URI.[/red]")
            return
    elif secret:
        # Validate secret
        try:
            pyotp.TOTP(secret)
            new_account = {"secret": secret, "name": name or "Unknown", "issuer": None}
        except:
            rprint("[red]Invalid secret key.[/red]")
            return
    else:
        rprint("[red]No secret, URI, or image provided.[/red]")
        return

    # Finalize
    if not new_account.get("name"):
        new_account["name"] = typer.prompt("Enter a name for this account")

    # Check for duplicates
    for acc in data["accounts"]:
        if acc["name"] == new_account["name"]:
            if not typer.confirm(f"Account '{new_account['name']}' already exists. Overwrite?"):
                return
            data["accounts"].remove(acc)
            break
            
    data["accounts"].append(new_account)
    save_secrets(data)
    rprint(f"[bold green]Account '{new_account['name']}' added successfully![/bold green]")

@app.command("list")
def list_accounts(watch: bool = typer.Option(False, "--watch", "-w", help="Keep updating the codes every second")):
    """List all accounts and current codes."""
    data = load_secrets()
    if not data["accounts"]:
        rprint("No accounts found. Use `add` to create one.")
        return

    def display():
        table = Table(title="2FA Codes")
        table.add_column("Account", style="cyan")
        table.add_column("Code", style="bold green")
        table.add_column("TTL", style="yellow")
        
        for acc in data["accounts"]:
            try:
                totp = pyotp.TOTP(acc["secret"])
                time_remaining = totp.interval - (time.time() % totp.interval)
                table.add_row(acc["name"], totp.now(), f"{int(time_remaining)}s")
            except Exception:
                table.add_row(acc["name"], "ERROR", "N/A")
        
        console.clear()
        console.print(table)

    if watch:
        try:
            while True:
                display()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        display()

@app.command()
def get(
    name: str = typer.Argument(..., help="Name of the account (fuzzy match)"),
    copy: bool = typer.Option(True, "--copy/--no-copy", help="Copy code to clipboard automatically")
):
    """Get code for a specific account."""
    data = load_secrets()
    accounts = data["accounts"]
    
    # Exact match
    match = next((a for a in accounts if a["name"] == name), None)
    
    # Fuzzy match (case insensitive, substring)
    if not match:
        matches = [a for a in accounts if name.lower() in a["name"].lower()]
        if len(matches) == 1:
            match = matches[0]
        elif len(matches) > 1:
            rprint(f"[yellow]Multiple matches found for '{name}':[/yellow]")
            for m in matches:
                rprint(f" - {m['name']}")
            return
            
    if match:
        totp = pyotp.TOTP(match["secret"])
        code = totp.now()
        rprint(f"Account: [cyan]{match['name']}[/cyan]")
        rprint(f"Code: [bold green]{code}[/bold green]")
        
        if copy:
            pyperclip.copy(code)
            rprint("[dim]Copied to clipboard![/dim]")
    else:
        rprint(f"[red]Account '{name}' not found.[/red]")

@app.command()
def delete(name: str = typer.Argument(..., help="Name of the account to delete")):
    """Delete an account."""
    data = load_secrets()
    accounts = data["accounts"]
    
    # Exact match first
    match = next((a for a in accounts if a["name"] == name), None)
    
    if not match:
        rprint(f"[red]Account '{name}' not found.[/red]")
        return
        
    if typer.confirm(f"Are you sure you want to delete '{name}'?"):
        data["accounts"] = [a for a in accounts if a["name"] != name]
        save_secrets(data)
        rprint(f"[green]Account '{name}' deleted.[/green]")

if __name__ == "__main__":
    app()
