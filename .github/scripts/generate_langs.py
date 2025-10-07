#!/usr/bin/env python3
import os
import sys
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

def generate_progress_bar(percentage, total_blocks=20):
    """Generate filled and empty blocks based on percentage"""
    filled_blocks = round((percentage / 100) * total_blocks)
    return filled_blocks, total_blocks - filled_blocks

def generate_svg(lang_stats, theme='light'):
    """Generate SVG with text-based progress bars (WakaTime style)"""
    
    if theme == 'light':
        title_color = '#4A5568'
        lang_color = '#2D3748'
        percent_color = '#4A5568'
        bar_color = '#6B7280'
    else:  # dark
        title_color = '#A0AEC0'
        lang_color = '#E2E8F0'
        percent_color = '#CBD5E0'
        bar_color = '#D1D5DB'
    
    height = 40 + len(lang_stats) * 24
    svg = f'''<svg width="480" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ 
      fill: {title_color}; 
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Droid Sans Mono', 'Source Code Pro', monospace;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
    }}
    .lang-name {{ 
      fill: {lang_color}; 
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Droid Sans Mono', 'Source Code Pro', monospace;
      font-size: 14px;
      font-weight: 400;
    }}
    .bar-text {{ 
      fill: {bar_color}; 
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Droid Sans Mono', 'Source Code Pro', monospace;
      font-size: 14px;
      font-weight: 400;
    }}
    .percent {{ 
      fill: {percent_color}; 
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Droid Sans Mono', 'Source Code Pro', monospace;
      font-size: 14px;
      font-weight: 400;
    }}
  </style>
  
  <rect width="480" height="{height}" fill="transparent"/>
  
  <!-- Title -->
  <text x="20" y="25" class="title">MOST USED LANGUAGES</text>
'''
    
    y_offset = 54
    for lang_name, percentage in lang_stats:
        filled_blocks, empty_blocks = generate_progress_bar(percentage, total_blocks=25)
        
        # Pad language name to fixed width
        lang_display = lang_name.ljust(14)[:14]
        
        # Generate bar string
        bar_string = '█' * filled_blocks + '░' * empty_blocks
        
        # Add comment
        svg += f'\n  <!-- {lang_name} - {percentage:.1f}% -->\n'
        
        # Add language name
        svg += f'  <text x="20" y="{y_offset}" class="lang-name">{lang_display}</text>\n'
        
        # Add progress bar
        svg += f'  <text x="160" y="{y_offset}" class="bar-text">{bar_string}</text>\n'
        
        # Add percentage
        percent_str = f'{percentage:5.1f}%'
        svg += f'  <text x="415" y="{y_offset}" class="percent">{percent_str}</text>\n'
        
        y_offset += 24
    
    svg += '</svg>'
    return svg

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
    
    # Generate light theme
    print("\nGenerating langs-mono-light.svg...")
    light_svg = generate_svg(lang_stats, theme='light')
    with open('langs-mono-light.svg', 'w') as f:
        f.write(light_svg)
    
    # Generate dark theme
    print("Generating langs-mono-dark.svg...")
    dark_svg = generate_svg(lang_stats, theme='dark')
    with open('langs-mono-dark.svg', 'w') as f:
        f.write(dark_svg)
    
    print("Done!")

if __name__ == '__main__':
    main()

