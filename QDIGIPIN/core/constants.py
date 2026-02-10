"""
Constants and configurations for DIGIPIN system
"""

# DIGIPIN Grid - 4x4 character grid
DIGIPIN_GRID = [
    ['F', 'C', '9', '8'],
    ['J', '3', '2', '7'],
    ['K', '4', '5', '6'],
    ['L', 'M', 'P', 'T']
]

# India geographical bounds
BOUNDS = {
    'minLat': 2.5,
    'maxLat': 38.5,
    'minLon': 63.5,
    'maxLon': 99.5
}

# Precision levels and their approximate cell sizes
PRECISION_INFO = {
    1: {'name': 'Level 1', 'cell_size_km': 900, 'accuracy': '~900 km'},
    2: {'name': 'Level 2', 'cell_size_km': 225, 'accuracy': '~225 km'},
    3: {'name': 'Level 3', 'cell_size_km': 56, 'accuracy': '~56 km'},
    4: {'name': 'Level 4', 'cell_size_km': 14, 'accuracy': '~14 km'},
    5: {'name': 'Level 5', 'cell_size_km': 3.5, 'accuracy': '~3.5 km'},
    6: {'name': 'Level 6', 'cell_size_km': 0.875, 'accuracy': '~875 m'},
    7: {'name': 'Level 7', 'cell_size_km': 0.219, 'accuracy': '~219 m'},
    8: {'name': 'Level 8', 'cell_size_km': 0.055, 'accuracy': '~55 m'},
    9: {'name': 'Level 9', 'cell_size_km': 0.014, 'accuracy': '~14 m'},
    10: {'name': 'Level 10', 'cell_size_km': 0.0034, 'accuracy': '~3.4 m'}
}

# Default settings
DEFAULT_PRECISION = 10
DEFAULT_CRS = 'EPSG:4326'

# Valid DIGIPIN characters
VALID_CHARS = set('FCJ3K4LM9287P56T')

# Plugin information
PLUGIN_NAME = 'Q-DIGIPIN India'
PLUGIN_VERSION = '1.0.0'
