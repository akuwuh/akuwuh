#!/usr/bin/env python3
"""
GitHub Language Statistics Generator
Fetches language statistics from GitHub and updates README.md with a 3D box visualization
"""

import os
import sys

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from lang_stats.fetcher import fetch_language_stats
from lang_stats.generator import generate_language_stats
from lang_stats.readme_updater import update_readme


def main():
    """Main workflow: fetch stats, generate box, update README"""
    
    # Step 1: Get environment variables
    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_ACTOR', 'akuwuh')
    
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    
    print(f"Fetching language stats for {username}...")
    
    # Step 2: Fetch language statistics from GitHub API
    lang_stats = fetch_language_stats(username, token)
    
    if not lang_stats:
        print("No language data found")
        sys.exit(1)
    
    print(f"Found {len(lang_stats)} languages:")
    for lang, pct in lang_stats:
        print(f"  {lang}: {pct:.1f}%")
    
    # Step 3: Generate formatted stats with 3D box
    print("\nGenerating language stats with 3D box...")
    stats_text = generate_language_stats(lang_stats, use_3d=True)
    
    print("\nGenerated HTML preview:")
    print(stats_text[:200] + "...")
    
    # Step 4: Update README.md
    print("\nUpdating README.md...")
    update_readme(stats_text)
    
    print("\n✓ Done! Language stats updated successfully.")


if __name__ == '__main__':
    main()