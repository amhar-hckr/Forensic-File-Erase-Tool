import os
from delete_excel_by_author import get_creator
from rich.console import Console

console = Console()

def test_metadata_extraction():
    """Test metadata extraction from various file types"""
    test_dir = "."  # Change this to your test files directory
    
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.lower().endswith(('.xls', '.xlsx', '.xlsm', '.doc', '.docx', '.pdf')):
                filepath = os.path.join(root, file)
                console.print(f"\n[bold]Testing {file}:[/bold]")
                creator = get_creator(filepath)
                console.print(f"Creator: {creator}")

if __name__ == "__main__":
    test_metadata_extraction()
