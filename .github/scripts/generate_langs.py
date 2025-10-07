#!/usr/bin/env python3
import os
import sys
import re
import requests
from collections import defaultdict

def fetch_language_stats(username, token):
    """Fetch language statistics from GitHub API"""
    headers = {'Authorization': f'token {token}'}
    
    # Get all repos
    repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
    repos = requests.get(repos_url, headers=headers).json()
    
    # Aggregate language bytes across all repos
    lang_bytes = defaultdict(int)
    
    for repo in repos:
        if isinstance(repo, dict) and not repo.get('fork', False):
            lang_url = repo.get('languages_url')
            if lang_url:
                languages = requests.get(lang_url, headers=headers).json()
                if isinstance(languages, dict):
                    for lang, bytes_count in languages.items():
                        lang_bytes[lang] += bytes_count
    
    # Calculate percentages
    total_bytes = sum(lang_bytes.values())
    if total_bytes == 0:
        return []
    
    lang_stats = []
    for lang, bytes_count in lang_bytes.items():
        percentage = (bytes_count / total_bytes) * 100
        lang_stats.append((lang, percentage))
    
    # Sort by percentage descending
    lang_stats.sort(key=lambda x: x[1], reverse=True)
    
    return lang_stats[:8]  # Top 8 languages

def generate_progress_bar(percentage, total_blocks=25):
    """Generate filled and empty blocks based on percentage"""
    filled_blocks = round((percentage / 100) * total_blocks)
    empty_blocks = total_blocks - filled_blocks
    return '█' * filled_blocks + '░' * empty_blocks

def generate_language_stats(lang_stats):
    """Generate WakaTime-style language stats as HTML samp"""
    lines = []
    
    for lang_name, percentage in lang_stats:
        # Pad language name to fixed width (14 chars)
        lang_display = lang_name.ljust(14)
        
        # Generate progress bar
        bar_string = generate_progress_bar(percentage)
        
        # Format percentage with padding
        percent_str = f'{percentage:5.1f} %'
        
        # Combine: "TypeScript    ████████████░░░░░░░░░░░░░  29.5 %"
        line = f'{lang_display} {bar_string}  {percent_str}'
        
        # Replace spaces with &nbsp; to preserve alignment in HTML
        line = line.replace(' ', '&nbsp;')
        
        lines.append(line)
    
    # Wrap in centered div with samp tag
    stats_html = '<br>\n'.join(lines)
    return f'<div align="center">\n<samp>\n{stats_html}\n</samp>\n</div>'

def update_readme(stats_text):
    """Update README.md with language stats between markers"""
    readme_path = 'README.md'
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found")
        sys.exit(1)
    
    # Markers for the stats section
    start_marker = '<!--START_SECTION:languages-->'
    end_marker = '<!--END_SECTION:languages-->'
    
    # Check if markers exist
    if start_marker not in content or end_marker not in content:
        print(f"Error: Markers not found in {readme_path}")
        print(f"Please add these markers to your README:")
        print(f"  {start_marker}")
        print(f"  {end_marker}")
        sys.exit(1)
    
    # Replace content between markers
    pattern = f'{re.escape(start_marker)}.*?{re.escape(end_marker)}'
    new_section = f'{start_marker}\n{stats_text}\n{end_marker}'
    
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    # Write back to README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Successfully updated {readme_path}")

def main():
    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_ACTOR', 'akuwuh')
    
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    
    print(f"Fetching language stats for {username}...")
    lang_stats = fetch_language_stats(username, token)
    
    if not lang_stats:
        print("No language data found")
        sys.exit(1)
    
    print(f"Found {len(lang_stats)} languages")
    for lang, pct in lang_stats:
        print(f"  {lang}: {pct:.1f}%")
    
    # Generate stats text
    print("\nGenerating language stats...")
    stats_text = generate_language_stats(lang_stats)
    
    print("\nGenerated stats:")
    print(stats_text)
    
    # Update README
    print("\nUpdating README.md...")
    update_readme(stats_text)
    
    print("Done!")

if __name__ == '__main__':
    main()

