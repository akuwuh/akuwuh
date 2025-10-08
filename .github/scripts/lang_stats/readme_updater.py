"""
README.md file updater
"""

import re
import sys
from .config import START_MARKER, END_MARKER


def update_readme(stats_text, readme_path='README.md'):
    """
    Update README.md with language stats between markers
    
    Args:
        stats_text: HTML string to insert
        readme_path: Path to README.md file
    """
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found")
        sys.exit(1)
    
    # Check if markers exist
    if START_MARKER not in content or END_MARKER not in content:
        print(f"Error: Markers not found in {readme_path}")
        print(f"Please add these markers to your README:")
        print(f"  {START_MARKER}")
        print(f"  {END_MARKER}")
        sys.exit(1)
    
    # Replace content between markers
    pattern = f'{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}'
    new_section = f'{START_MARKER}\n{stats_text}\n{END_MARKER}'
    
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    # Write back to README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Successfully updated {readme_path}")
