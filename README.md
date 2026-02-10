# Q-DIGIPIN India - QGIS Plugin

Professional geocoding plugin for India Post's DIGIPIN system.

## Overview

Q-DIGIPIN India is a comprehensive QGIS plugin that implements India Post's DIGIPIN geocoding system. DIGIPIN is a hierarchical geocoding system that converts any location in India into a 10-character alphanumeric code.

## Features

- **Encode Coordinates to DIGIPIN**: Convert latitude/longitude to DIGIPIN codes
- **Decode DIGIPIN to Coordinates**: Convert DIGIPIN codes back to coordinates
- **Batch Processing**: Process entire point layers at once
- **Grid Generation**: Create DIGIPIN grid polygons for any extent
- **Processing Algorithms**: Integrate with QGIS Processing Toolbox
- **Multiple Precision Levels**: Support for 1-10 precision levels (from ~900km to ~3.4m accuracy)

## Installation

### From QGIS Plugin Manager (Recommended)
1. Open QGIS
2. Go to `Plugins` → `Manage and Install Plugins`
3. Search for "Q-DIGIPIN India"
4. Click `Install Plugin`

### Manual Installation
1. Download the plugin ZIP file
2. Extract to your QGIS plugins directory:
   - Windows: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - Mac: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Restart QGIS
4. Enable the plugin in `Plugins` → `Manage and Install Plugins`

## Usage

### Encoding Coordinates

1. Open the plugin: `Vector` → `DIGIPIN India` → `Open DIGIPIN Tools`
2. Go to the **Encode** tab
3. Enter latitude and longitude
4. Select precision level (1-10)
5. Click **Encode to DIGIPIN**

### Decoding DIGIPIN

1. Open the plugin
2. Go to the **Decode** tab
3. Enter DIGIPIN code (with or without hyphens)
4. Click **Decode DIGIPIN**

### Batch Processing

1. Open the plugin
2. Go to the **Batch Process** tab
3. Select a point layer
4. Choose precision level
5. Enter output field name
6. Click **Encode Layer to DIGIPIN**

### Processing Algorithms

Access DIGIPIN tools from the Processing Toolbox:

- **DIGIPIN India** → **Encoding** → **Encode Points to DIGIPIN**
- **DIGIPIN India** → **Decoding** → **Decode DIGIPIN to Points**
- **DIGIPIN India** → **Grid Operations** → **Generate DIGIPIN Grid**

## Precision Levels

| Level | Accuracy | Use Case |
|-------|----------|----------|
| 1 | ~900 km | Country/State level |
| 3 | ~56 km | District level |
| 5 | ~3.5 km | City/Town level |
| 7 | ~219 m | Neighborhood level |
| 10 | ~3.4 m | Building/Address level |

## DIGIPIN Format

DIGIPIN codes are 10-character alphanumeric codes formatted as: `XXX-XXX-XXXX`

Example: `FCJ-3K4-LM9287`

Valid characters: F, C, J, 3, K, 4, L, M, 9, 2, 8, 7, P, 5, 6, T

## Requirements

- QGIS 3.0 or higher
- Python 3.6 or higher

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Credits

**DIGIPIN System**: Department of Posts, India Post, Government of India

**Plugin Development**: Sakyasingh Rout

## Support

- **Issues**: https://github.com/sakyasingh/Q-DIGIPIN-India/issues
- **Documentation**: See project wiki
- **Email**: sakyasingh@example.com

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Changelog

### Version 1.1.1 (2026-02-10)
- Initial release
- Core encoding/decoding functionality
- Batch processing support
- Processing algorithms
- Grid generation
- Modern tabbed interface
