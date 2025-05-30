import os
import subprocess
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich import box
from pyfiglet import Figlet
from pathlib import Path
import string
import psutil
import threading
from rich.prompt import Confirm
from file_operations import delete_file, setup_logging

# Initialize logging
logger = setup_logging()

# ASCII Art Banner
BANNER = """
[#003366]
▓█████▄▄▄█████▓ ▄▄▄       ▄████▄   ██░ ██ ▓█████  ██▀███  
▓█   ▀▓  ██▒ ▓▒▒████▄    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒
▒███  ▒ ▓██░ ▒░▒██  ▀█▄  ▒▓█    ▄ ▒██▀▀██░▒███   ▓██ ░▄█ ▒
▒▓█  ▄░ ▓██▓ ░ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  
░▒████▒ ▒██▒ ░  ▓█   ▓██▒▒ ▓███▀ ░░▓█▒░██▓░▒████▒░██▓ ▒██▒
░░ ▒░ ░ ▒ ░░    ▒▒   ▓▒█░░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ░  ░   ░      ▒   ▒▒ ░  ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░
   ░    ░        ░   ▒   ░         ░  ░░ ░   ░     ░░   ░ 
   ░  ░              ░  ░░ ░       ░  ░  ░   ░  ░   ░     
                         ░                                  
[/#003366]
[#1a478c]╔══════════════════════════════════════════════════════════╗
║             [#2c5aa0]FORENSIC FILE ELIMINATION SYSTEM[/#2c5aa0]             ║
║        [#4d4d4d]Secure • Fast • Professional • Untraceable[/#4d4d4d]        ║
║           [#2c5aa0]Developed by: Amh4ck3r [/#2c5aa0]                        ║
╚══════════════════════════════════════════════════════════╝[/#1a478c]
"""

console = Console()
console.print(BANNER)

# Setup EXIFTOOL path detection
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    # Set PERL5LIB environment variable to help ExifTool find its modules
    perl_lib = os.path.join(BASE_DIR, 'lib')
    os.environ['PERL5LIB'] = perl_lib
    if 'PATH' not in os.environ:
        os.environ['PATH'] = ''
    os.environ['PATH'] = BASE_DIR + os.pathsep + os.environ['PATH']
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # In development mode, use the exiftool_files lib directory
    perl_lib = os.path.join(BASE_DIR, 'exiftool_files', 'lib')
    os.environ['PERL5LIB'] = perl_lib

EXIFTOOL_PATH = os.path.join(BASE_DIR, "exiftool.exe")
if not os.path.exists(EXIFTOOL_PATH):
    EXIFTOOL_PATH = "exiftool"

# Verify ExifTool is working
try:
    result = subprocess.run([EXIFTOOL_PATH, "-ver"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print("[red]ExifTool not properly configured. Error:[/red]")
        console.print(result.stderr)
        sys.exit(1)
except Exception as e:
    console.print(f"[red]Failed to run ExifTool: {e}[/red]")
    sys.exit(1)

EXCEL_EXTENSIONS = ['.xls', '.xlsx', '.xlsb', '.xlsm']

def show_startup_message():
    """Show initial startup message with security warning"""
    console.print(Panel.fit(
        "[#990000]⚠ SECURITY WARNING ⚠[/#990000]\n\n"
        "[#666666]This tool performs permanent file operations.[/#666666]\n"
        "[#666666]Files deleted cannot be recovered.[/#666666]\n"
        "[#4d4d4d]Make sure you have proper authorization.[/#4d4d4d]",
        title="[#990000]NOTICE[/#990000]",
        border_style="#990000"
    ))
    time.sleep(2)

def get_creator(filepath):
    """Get the creator of a file using exiftool with multiple fallback tags"""
    try:
        # List of metadata tags to check for creator information
        creator_tags = [
            "-Creator",           # Standard creator tag
            "-Author",           # Common in Office documents
            "-LastModifiedBy",   # Excel specific
            "-LastSavedBy",      # Another Excel specific tag
            "-Creator-Tool",     # Alternative creator tag
            "-Producer",         # PDF and some Office docs
            "-Company",          # Office documents
            "-Owner",           # Another common ownership tag
            "-MetadataDate",    # Date metadata was last modified
            "-Software",        # Software used to create the file
            "-OwnerName",       # Alternative owner name
            "-UserName",        # User name from some applications
            "-Contributors",    # Contributors list
            "-Manager",         # Manager field from Office docs
        ]
        
        # First try to get all metadata to see what's available
        debug_cmd = [EXIFTOOL_PATH, "-G", "-s", "-a", filepath]
        debug_result = subprocess.run(debug_cmd, capture_output=True, text=True)
        if debug_result.stdout:
            console.print(f"[dim]Debug metadata for {os.path.basename(filepath)}:[/dim]")
            console.print(f"[dim]{debug_result.stdout}[/dim]")
        
        # Try regular metadata extraction
        command = [EXIFTOOL_PATH] + creator_tags + ["-s3", filepath]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Get all non-empty lines from the output
        creators = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        # If no creators found and it's an Office document, try Office-specific approach
        if not creators and filepath.lower().endswith(('.xls', '.xlsx', '.xlsm', '.doc', '.docx')):
            office_cmd = [EXIFTOOL_PATH, "-Office:all", "-s3", filepath]
            office_result = subprocess.run(office_cmd, capture_output=True, text=True)
            if office_result.stdout:
                creators.extend([line.strip() for line in office_result.stdout.splitlines() if line.strip()])
        
        # Filter out generic system accounts and empty values
        filtered_creators = []
        for creator in creators:
            # Skip if creator is empty or None
            if not creator:
                continue
            # Skip generic system accounts
            if creator.lower() in ['system', 'administrator', 'unknown', 'user']:
                continue
            # Skip if creator is just spaces or special characters
            if not any(c.isalnum() for c in creator):
                continue
            filtered_creators.append(creator)
        
        return next((creator for creator in filtered_creators if creator), "Unknown")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]ExifTool error for {filepath}: {e.stderr}[/red]")
        return "Unknown"
    except Exception as e:
        console.print(f"[red]Error reading metadata for {filepath}: {e}[/red]")
        return "Unknown"

def scan_excel_files(directory):
    """Scan directory for files and collect their paths"""
    files = []
    try:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in EXCEL_EXTENSIONS):
                    try:
                        full_path = os.path.join(root, filename)
                        # Verify the file exists and is readable
                        if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
                            files.append(full_path)
                        else:
                            console.print(f"[yellow]Warning: Cannot access file: {full_path}[/yellow]")
                    except Exception as e:
                        console.print(f"[red]Error processing file {filename}: {e}[/red]")
                        continue
    except Exception as e:
        console.print(f"[red]Error scanning directory {directory}: {e}[/red]")
    
    return files

def display_creators(creator_files):
    table = Table(title="Excel Files by Creator", box=box.DOUBLE_EDGE, title_style="#2c5aa0", border_style="#1a478c")
    table.add_column("Creator", style="#FAE900", no_wrap=True)
    table.add_column("File Count", justify="right", style="#09ff00")
    for creator, files in creator_files.items():
        table.add_row(creator, str(len(files)))
    console.print(table)

def list_available_drives():
    drives = []
    for part in psutil.disk_partitions():
        if os.path.exists(part.device):
            drives.append(part.device)
    return drives

def select_scan_path():
    while True:
        console.print(Panel.fit(
            "[#2c5aa0]Select Scan Mode:[/#2c5aa0]\n"
            "1. Full Drive Scan\n"
            "2. Specific Folder (Manual Path)\n"
            "3. Browse for Folder\n"
            "4. Exit", 
            border_style="#1a478c"
        ))
        choice = console.input("[#003366]Enter choice (1-4): [/#003366]").strip()
        
        if choice == '1':
            drives = list_available_drives()
            console.print("\n[bold green]Available Drives:[/bold green]")
            for idx, d in enumerate(drives, 1):
                console.print(f"{idx}. {d}")
            drive_choice = console.input("Enter drive number or letter (e.g. C): ").strip().upper()
            if drive_choice.isdigit():
                idx = int(drive_choice) - 1
                if 0 <= idx < len(drives):
                    return drives[idx]
                else:
                    console.print("[red]Invalid drive number.[/red]")
            elif len(drive_choice) == 1 and drive_choice in string.ascii_uppercase:
                path = f"{drive_choice}:/"
                if os.path.exists(path):
                    return path
                else:
                    console.print(f"[red]Drive {drive_choice}: does not exist.[/red]")
            else:
                console.print("[red]Invalid input.[/red]")
        
        elif choice == '2':
            folder = console.input("Enter full folder path: ").strip()
            if os.path.isdir(folder):
                return folder
            console.print("[red]Invalid folder path.[/red]")
            
        elif choice == '3':
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                root.attributes('-topmost', True)  # Make dialog stay on top
                folder = filedialog.askdirectory(
                    title="Select Folder to Scan",
                    mustexist=True
                )
                root.destroy()
                if folder and os.path.exists(folder):
                    return folder
                else:
                    console.print("[red]No folder selected.[/red]")
            except Exception as e:
                console.print(f"[red]Error opening folder browser: {e}[/red]")
        
        elif choice == '4':
            console.print("[bold yellow]Exiting...[/bold yellow]")
            sys.exit(0)
        else:
            console.print("[red]Invalid choice.[/red]")

def select_file_type():
    console.print(Panel.fit("""[#2c5aa0]Choose File Category to Scan:[/#2c5aa0]

[1] 📄 Document Files       (.doc, .pdf, .txt, .odt)
[2] 📊 Spreadsheet Files    (.xls, .xlsx, .xlsb, .xlsm)
[3] 📈 Presentation Files   (.ppt, .pptx, .odp)
[4] 🖼️ Image Files          (.jpg, .png, .svg, .bmp, .tiff)
[5] 📹 Video/Audio Files    (.mp4, .mp3, .wav, .mov)
[6] 🗃️ Database Files       (.sql, .mdb, .db, .sqlite)
[7] 📦 Compressed Files     (.zip, .rar, .7z, .tar)
[8] ⚙️ Config/System Files  (.log, .ini, .json, .sh, .bat)
[9] 💻 Executable/Source Code (.exe, .py, .js, .html)

[0] Cancel
""", border_style="#ff0404"))

    choices = {
        '1': ['.doc', '.docx', '.pdf', '.txt', '.odt'],
        '2': ['.xls', '.xlsx', '.xlsb', '.xlsm'],
        '3': ['.ppt', '.pptx', '.odp'],
        '4': ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.tiff'],
        '5': ['.mp4', '.mov', '.mp3', '.wav'],
        '6': ['.sql', '.mdb', '.accdb', '.db', '.sqlite'],
        '7': ['.zip', '.rar', '.tar', '.gz', '.7z'],
        '8': ['.log', '.ini', '.conf', '.yaml', '.json', '.xml', '.bat', '.sh', '.ps1'],
        '9': ['.exe', '.msi', '.apk', '.ipa', '.py', '.java', '.js', '.html', '.css'],
    }

    while True:
        choice = console.input("Select category number: ").strip()
        if choice == '0':
            sys.exit(0)
        if choice in choices:
            return choices[choice]
        console.print("[red]Invalid selection. Try again.[/red]")


def ask_yes_no(prompt, default='n'):
    while True:
        val = console.input(f"{prompt} (y/N): ").strip().lower()
        if val == '' and default:
            val = default
        if val in ['y', 'n']:
            return val == 'y'
        console.print("[red]Enter 'y' or 'n'.[/red]")

def get_deletion_options():
    """Get user preferences for file deletion."""
    console.print(Panel.fit(
        "[#2c5aa0]Deletion Options[/#2c5aa0]\n"
        "1. Confirm deletion",
        border_style="#ca1d1d"
    ))
    
    secure = Confirm.ask("Confirm deletion?", default=False)
    backup = False
    preview = False
    
    return secure, backup, preview

def process_deletions(files, preview=False, secure=False, backup=True):
    """Process file deletions with the specified options."""
    deleted, failed, skipped = 0, 0, 0
    
    for file in track(files, description="[#2c5aa0]Processing files[/#2c5aa0]"):
        try:
            if preview:
                console.print(f"[#666666]Would delete: {file}[/#666666]")
                skipped += 1
                continue
                
            success = delete_file(file, secure=secure, backup=backup)
            if success:
                deleted += 1
            else:
                failed += 1
                
        except Exception as e:
            logger.error(f"Error processing {file}: {str(e)}")
            failed += 1
            
    return deleted, failed, skipped

def main():
    try:
        while True:
            selected_extensions = select_file_type()
            global EXCEL_EXTENSIONS
            EXCEL_EXTENSIONS = selected_extensions
            scan_path = select_scan_path()
            console.print(f"\n[yellow]Scanning: {scan_path}[/yellow]\n")

            # Show analyzing UI immediately after scan path selection
            console.print(Panel.fit(
                "[#003366]\n⏳ [bold cyan]Please wait...[/bold cyan]\n\n[white]Analyzing files and extracting metadata.\nThis may take several minutes for large drives![/white]\n[#1a478c]══════════════════════════════════════════════[/#1a478c]",
                title="[bold #2c5aa0]File Analysis In Progress[/bold #2c5aa0]",
                border_style="#1a478c",
                box=box.DOUBLE
            ))

            files = scan_excel_files(scan_path)
            if not files:
                console.print("[bold red]No matching files found.[/bold red]")
                continue
            creator_files = {}
            with console.status("[green]Analyzing metadata...[/green]"):
                for filepath in track(files, description="Analyzing files"):
                    creator = get_creator(filepath)
                    creator_files.setdefault(creator, []).append(filepath)
            display_creators(creator_files)
            
            while creator_files:
                console.print("\n[bold blue]Available Creators:[/bold blue]")
                for i, creator in enumerate(creator_files, 1):
                    console.print(f"{i}. {creator}")
                selection = console.input("\nSelect creator name or number to delete (or 'exit', 'back'): ").strip()
                
                if selection.lower() in ('exit', 'quit'):
                    console.print("[bold yellow]Exiting...[/bold yellow]")
                    sys.exit(0)
                if selection.lower() == 'back':
                    break
                    
                selected_creator = None
                if selection.isdigit() and 1 <= int(selection) <= len(creator_files):
                    selected_creator = list(creator_files)[int(selection) - 1]
                else:
                    for c in creator_files:
                        if c.lower() == selection.lower():
                            selected_creator = c
                            break
                            
                if not selected_creator:
                    console.print("[red]Invalid selection.[/red]")
                    continue
                    
                console.print(Panel.fit(f"[bold cyan]Files by {selected_creator}[/bold cyan]", border_style="cyan"))
                for i, f in enumerate(creator_files[selected_creator], 1):
                    console.print(f"[green]{i}.[/green] {f}")
                    
                if ask_yes_no(f"\nProcess files by '{selected_creator}'?"):
                    secure, backup, preview = get_deletion_options()
                    
                    deleted, failed, skipped = process_deletions(
                        creator_files[selected_creator],
                        preview=preview,
                        secure=secure,
                        backup=backup
                    )
                    
                    if not preview:
                        del creator_files[selected_creator]
                        
                    console.print(f"\n[bold]Results:[/bold]")
                    console.print(f"[green]Successfully deleted: {deleted}[/green]")
                    console.print(f"[red]Failed: {failed}[/red]")
                    if preview:
                        console.print(f"[yellow]Skipped (preview mode): {skipped}[/yellow]")
                        
                    if not creator_files:
                        console.print("[bold yellow]No more files left.[/bold yellow]")
                        break
                        
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted by user.[/red]")
        if ask_yes_no("Exit anyway?", default='y'):
            sys.exit(0)
        else:
            main()
            
# Add the startup message call before the main menu
if __name__ == '__main__':
    show_startup_message()
    main()



