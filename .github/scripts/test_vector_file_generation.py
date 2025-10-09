#!/usr/bin/env python3
"""
Test script to verify vector mode generates SVG files correctly
"""

import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from lang_stats.generator import generate_language_stats

# Sample language statistics
sample_data = [
    ('TypeScript', 34.3),
    ('Python', 33.6),
    ('C', 21.4),
    ('C++', 8.9),
    ('Svelte', 1.2)
]

print("Testing vector mode file generation...")
print("=" * 80)

# Generate light theme
print("\nGenerating light theme SVG...")
svg_light = generate_language_stats(
    sample_data,
    use_3d=True,
    output_mode='vector',
    use_graphical_bars=True,
    svg_theme='light'
)

# Generate dark theme
print("Generating dark theme SVG...")
svg_dark = generate_language_stats(
    sample_data,
    use_3d=True,
    output_mode='vector',
    use_graphical_bars=True,
    svg_theme='dark'
)

# Extract SVG content (remove wrapping div)
svg_light_content = svg_light.replace('<div align="center">\n', '').replace('\n</div>', '')
svg_dark_content = svg_dark.replace('<div align="center">\n', '').replace('\n</div>', '')

# Save to workspace root (simulating the actual workflow)
workspace_root = os.path.join(os.path.dirname(__file__), '..', '..')
light_path = os.path.join(workspace_root, 'langs-mono-light.svg')
dark_path = os.path.join(workspace_root, 'langs-mono-dark.svg')

with open(light_path, 'w', encoding='utf-8') as f:
    f.write(svg_light_content)
print(f"✓ Saved {light_path}")

with open(dark_path, 'w', encoding='utf-8') as f:
    f.write(svg_dark_content)
print(f"✓ Saved {dark_path}")

print("\n" + "=" * 80)
print("✓ Vector mode file generation successful!")
print("\nGenerated files:")
print(f"  - {light_path}")
print(f"  - {dark_path}")
print("\nTo use in README, add:")
print('<picture>')
print('  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">')
print('  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">')
print('  <img alt="Language Statistics" src="langs-mono-light.svg">')
print('</picture>')

