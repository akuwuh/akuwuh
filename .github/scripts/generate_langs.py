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
    
    # Get output mode configuration from environment (defaults to config values)
    output_mode = os.environ.get('OUTPUT_MODE', None)  # 'text' or 'vector'
    use_graphical_bars = os.environ.get('USE_GRAPHICAL_BARS', None)
    svg_theme = os.environ.get('SVG_THEME', None)  # 'light' or 'dark'
    
    # Convert string to boolean for use_graphical_bars
    if use_graphical_bars is not None:
        use_graphical_bars = use_graphical_bars.lower() in ('true', '1', 'yes')
    
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    
    print(f"Fetching language stats for {username}...")
    if output_mode:
        print(f"Output mode: {output_mode}")
    
    # Step 2: Fetch language statistics from GitHub API
    lang_stats = fetch_language_stats(username, token)
    
    if not lang_stats:
        print("No language data found")
        sys.exit(1)
    
    print(f"Found {len(lang_stats)} languages:")
    for lang, pct in lang_stats:
        print(f"  {lang}: {pct:.1f}%")
    
    # Step 3: Generate formatted stats with 3D box
    mode_str = output_mode if output_mode else "default (text)"
    print(f"\nGenerating language stats with 3D box (mode: {mode_str})...")
    
    # Vector mode: Save SVG files instead of updating README
    if output_mode == 'vector':
        print("Vector mode: Generating both light and dark theme SVGs...")
        
        # Generate light theme
        svg_light = generate_language_stats(
            lang_stats,
            use_3d=True,
            output_mode='vector',
            use_graphical_bars=True if use_graphical_bars is None else use_graphical_bars,
            svg_theme='light'
        )
        
        # Generate dark theme
        svg_dark = generate_language_stats(
            lang_stats,
            use_3d=True,
            output_mode='vector',
            use_graphical_bars=True if use_graphical_bars is None else use_graphical_bars,
            svg_theme='dark'
        )
        
        # Extract SVG content (remove wrapping div)
        svg_light_content = svg_light.replace('<div align="center">\n', '').replace('\n</div>', '')
        svg_dark_content = svg_dark.replace('<div align="center">\n', '').replace('\n</div>', '')
        
        # Save to files
        with open('langs-mono-light.svg', 'w', encoding='utf-8') as f:
            f.write(svg_light_content)
        print("✓ Saved langs-mono-light.svg")
        
        with open('langs-mono-dark.svg', 'w', encoding='utf-8') as f:
            f.write(svg_dark_content)
        print("✓ Saved langs-mono-dark.svg")
        
        print("\n✓ Done! SVG files generated successfully.")
        print("\nTo use in README, add:")
        print('<picture>')
        print('  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">')
        print('  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">')
        print('  <img alt="Language Statistics" src="langs-mono-light.svg">')
        print('</picture>')
    else:
        # Text mode: Update README as usual
        stats_text = generate_language_stats(
            lang_stats, 
            use_3d=True,
            output_mode=output_mode,
            use_graphical_bars=use_graphical_bars,
            svg_theme=svg_theme
        )
        
        print("\nGenerated output preview:")
        print(stats_text[:200] + "...")
        
        # Update README.md
        print("\nUpdating README.md...")
        update_readme(stats_text)
        
        print("\n✓ Done! Language stats updated successfully.")


if __name__ == '__main__':
    main()