# User Guide - Q-DIGIPIN India

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [Usage Examples](#usage-examples)
6. [Processing Algorithms](#processing-algorithms)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Introduction

Q-DIGIPIN India is a QGIS plugin that implements India Post's DIGIPIN geocoding system. DIGIPIN converts any location in India into a unique 10-character alphanumeric code.

### What is DIGIPIN?

DIGIPIN is a hierarchical geocoding system where:
- Each character represents a subdivision of the previous level
- The system uses a 4x4 grid at each level
- 10 levels provide accuracy from ~900 km down to ~3.4 meters

### Valid Characters

DIGIPIN uses 16 characters: **F, C, J, 3, K, 4, L, M, 9, 2, 8, 7, P, 5, 6, T**

### Format

DIGIPINs are formatted as: `XXX-XXX-XXXX` (e.g., `FCJ-3K4-LM92`)

## Installation

### Method 1: QGIS Plugin Manager (Recommended)

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Search for "Q-DIGIPIN India"
4. Click **Install Plugin**
5. Enable the plugin if not automatically enabled

### Method 2: Manual Installation

1. Download the plugin ZIP file
2. Extract to your QGIS plugins directory:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Restart QGIS
4. Enable in **Plugins** → **Manage and Install Plugins**

## Getting Started

### Opening the Plugin

1. Click the DIGIPIN icon in the toolbar, OR
2. Go to **Vector** → **DIGIPIN India** → **Open DIGIPIN Tools**

### Interface Overview

The plugin has four main tabs:

1. **Encode**: Convert coordinates to DIGIPIN
2. **Decode**: Convert DIGIPIN to coordinates
3. **Batch Process**: Process entire layers
4. **About**: Plugin information

## Features

### 1. Single Point Encoding

Convert a single coordinate pair to DIGIPIN:

1. Open the **Encode** tab
2. Enter **Latitude** (e.g., 28.6139)
3. Enter **Longitude** (e.g., 77.2090)
4. Select **Precision Level** (1-10)
5. Click **Encode to DIGIPIN**

**Actions:**
- **Copy DIGIPIN**: Copy result to clipboard
- **Create Point Layer**: Add point to map

### 2. Single DIGIPIN Decoding

Convert a DIGIPIN code to coordinates:

1. Open the **Decode** tab
2. Enter **DIGIPIN Code** (with or without hyphens)
3. Click **Decode DIGIPIN**

**Actions:**
- **Copy Coordinates**: Copy lat/lon to clipboard
- **Create Point Layer**: Add point to map
- **Zoom to Location**: Navigate to location

### 3. Batch Layer Encoding

Encode all points in a layer:

1. Open the **Batch Process** tab
2. Select a **Point Layer**
3. Choose **Precision Level**
4. Enter **Output Field Name** (default: DIGIPIN)
5. Click **Encode Layer to DIGIPIN**

The plugin will add a new field with DIGIPIN codes to your layer.

## Usage Examples

### Example 1: Encode New Delhi Coordinates

```
Latitude: 28.6139
Longitude: 77.2090
Precision: 10

Result: FCJ-3K4-LM92 (or similar)
```

### Example 2: Decode a DIGIPIN

```
DIGIPIN: FCJ-3K4-LM9

Result:
Latitude: 28.xxxxx
Longitude: 77.xxxxx
Bounds: [min/max lat/lon]
```

### Example 3: Batch Encode Cities

1. Load a point layer with Indian cities
2. Use Batch Process tab
3. Select precision level 7 (neighborhood level)
4. Process layer
5. New DIGIPIN field added to attribute table

## Processing Algorithms

Access from **Processing Toolbox** → **DIGIPIN India**

### 1. Encode Points to DIGIPIN

**Location**: DIGIPIN India → Encoding → Encode Points to DIGIPIN

**Inputs:**
- Input point layer
- Precision level (1-10)
- Output field name

**Output:**
- Point layer with DIGIPIN field

### 2. Decode DIGIPIN to Points

**Location**: DIGIPIN India → Decoding → Decode DIGIPIN to Points

**Inputs:**
- Input layer with DIGIPIN field
- DIGIPIN field name

**Output:**
- Point layer with decoded coordinates

### 3. Generate DIGIPIN Grid

**Location**: DIGIPIN India → Grid Operations → Generate DIGIPIN Grid

**Inputs:**
- Grid extent
- Precision level

**Output:**
- Polygon layer with DIGIPIN cells

## Troubleshooting

### Plugin doesn't appear in menu

1. Check if plugin is enabled: **Plugins** → **Manage and Install Plugins**
2. Look for Q-DIGIPIN India in the list
3. Ensure checkbox is checked

### "Coordinates out of range" error

DIGIPIN only works within India's geographical bounds:
- Latitude: 2.5° to 38.5° N
- Longitude: 63.5° to 99.5° E

### Batch processing is slow

- Large layers may take time
- Progress bar shows current status
- You can cancel operation if needed

### Invalid DIGIPIN error

Check that:
- Only valid characters are used (F,C,J,3,K,4,L,M,9,2,8,7,P,5,6,T)
- Length is between 1-10 characters
- Format is correct

## FAQ

### Q: What precision level should I use?

**A:** It depends on your use case:
- **Level 1-3**: Regional/district level mapping
- **Level 5-7**: City/neighborhood level
- **Level 8-10**: Building/address level (most precise)

### Q: Can I use DIGIPIN outside India?

**A:** No, DIGIPIN is specifically designed for India's geographical bounds.

### Q: How accurate is DIGIPIN?

**A:** Accuracy depends on precision level:
- Level 10: ~3.4 meters
- Level 7: ~219 meters
- Level 5: ~3.5 kilometers

### Q: Can I export DIGIPIN data?

**A:** Yes, use QGIS's standard export functions:
- Right-click layer → Export → Save Features As
- Choose format (CSV, GeoJSON, Shapefile, etc.)

### Q: Is the plugin free?

**A:** Yes, Q-DIGIPIN India is open source (GPL v3 license).

### Q: How do I report bugs?

**A:** Report issues on GitHub: https://github.com/sakyasingh/Q-DIGIPIN-India/issues

### Q: Can I contribute to the plugin?

**A:** Yes! Contributions are welcome. See CONTRIBUTING.md for guidelines.

## Support

- **Email**: sakyasingh@example.com
- **GitHub**: https://github.com/sakyasingh/Q-DIGIPIN-India
- **Documentation**: Project wiki on GitHub

---

**Version**: 1.0.0  
**Last Updated**: February 2026
