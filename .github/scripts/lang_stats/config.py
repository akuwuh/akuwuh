"""
Configuration constants for box drawing and formatting
"""

# ============================================================================
# BOX DRAWING CONFIGURATION
# ============================================================================

# Padding inside the box
LEFT_PADDING = 2   # Spaces to the left of content inside box
RIGHT_PADDING = 3  # Spaces to the right of content inside box

# Extrusion spacing (3D effect)
EXTRUSION_INDENT_LEVEL_1 = 2  # Spaces before content lines and first bottom line
EXTRUSION_INDENT_LEVEL_2 = 3  # Spaces before second bottom line (depth effect)

# ============================================================================
# PROGRESS BAR CONFIGURATION
# ============================================================================

PROGRESS_BAR_BLOCKS = 25  # Total number of blocks in progress bar
FILLED_BLOCK = '█'        # Character for filled portion
EMPTY_BLOCK = '░'         # Character for empty portion

# ============================================================================
# CONTENT FORMATTING
# ============================================================================

LANG_NAME_WIDTH = 14      # Fixed width for language names
MAX_LANGUAGES = 6         # Maximum number of languages to display

# ============================================================================
# LANGUAGE FILTERING
# ============================================================================

EXCLUDED_LANGUAGES = [
    'JavaScript',
    'HTML',
    'CSS'
]  # Languages to exclude from statistics

# ============================================================================
# README MARKERS
# ============================================================================

START_MARKER = '<!--START_SECTION:languages-->'
END_MARKER = '<!--END_SECTION:languages-->'
