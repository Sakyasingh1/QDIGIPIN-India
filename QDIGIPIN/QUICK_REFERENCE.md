# Q-DIGIPIN India - Quick Reference

## Quick Start

### Opening the Plugin
- **Toolbar**: Click DIGIPIN icon
- **Menu**: Vector → DIGIPIN India → Open DIGIPIN Tools
- **Shortcut**: (Can be configured in QGIS settings)

## Common Tasks

### 1. Encode a Single Location

```
Tab: Encode
Latitude: 28.6139
Longitude: 77.2090
Precision: 10
→ Click "Encode to DIGIPIN"
Result: FCJ-3K4-XXXX (example)
```

### 2. Decode a DIGIPIN

```
Tab: Decode
DIGIPIN: FCJ-3K4-LM92
→ Click "Decode DIGIPIN"
Result: Lat/Lon + Bounds
```

### 3. Batch Encode a Layer

```
Tab: Batch Process
1. Select point layer
2. Choose precision (1-10)
3. Enter field name (default: DIGIPIN)
4. Click "Encode Layer to DIGIPIN"
```

## Precision Levels Quick Reference

| Level | Accuracy | Use Case |
|-------|----------|----------|
| 1 | ~900 km | Country/Region |
| 2 | ~225 km | State |
| 3 | ~56 km | District |
| 4 | ~14 km | Taluk |
| 5 | ~3.5 km | City/Town |
| 6 | ~875 m | Locality |
| 7 | ~219 m | Neighborhood |
| 8 | ~55 m | Street |
| 9 | ~14 m | Building |
| 10 | ~3.4 m | Address |

## DIGIPIN Format

- **Characters**: F, C, J, 3, K, 4, L, M, 9, 2, 8, 7, P, 5, 6, T
- **Format**: XXX-XXX-XXXX (hyphens optional)
- **Length**: 1-10 characters
- **Example**: FCJ-3K4-LM9287

## Processing Algorithms

Access from: **Processing Toolbox** → **DIGIPIN India**

### Encode Points to DIGIPIN
```
Input: Point layer
Precision: 1-10
Field name: DIGIPIN
→ Output: Layer with DIGIPIN field
```

### Decode DIGIPIN to Points
```
Input: Layer with DIGIPIN field
Field: Select DIGIPIN field
→ Output: Point layer with coordinates
```

### Generate DIGIPIN Grid
```
Extent: Map canvas / Layer / Custom
Precision: 1-10
→ Output: Polygon grid layer
```

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open Plugin | (Configure in QGIS) |
| Copy Result | Ctrl+C (after selecting) |
| Close Dialog | Esc |

## Common Errors

### "Coordinates out of range"
- **Cause**: Location outside India
- **Fix**: Check lat/lon values
- **Valid Range**: 
  - Lat: 2.5° to 38.5° N
  - Lon: 63.5° to 99.5° E

### "Invalid DIGIPIN"
- **Cause**: Wrong characters or format
- **Fix**: Use only valid characters
- **Valid**: F,C,J,3,K,4,L,M,9,2,8,7,P,5,6,T

### "No point layers available"
- **Cause**: No point layers in project
- **Fix**: Load a point layer first

## Tips & Tricks

### 1. Quick Copy
- After encoding/decoding, use "Copy" buttons
- Paste directly into other applications

### 2. Create Layers
- Use "Create Point Layer" to visualize results
- Layers are added to current project

### 3. Zoom to Location
- After decoding, use "Zoom to Location"
- Map centers on DIGIPIN cell

### 4. Batch Processing
- Process thousands of points at once
- Progress bar shows status
- Can cancel anytime

### 5. Field Names
- Use descriptive field names
- Example: DIGIPIN_L10, DIGIPIN_L5
- Helps identify precision level

## Example Coordinates

### Major Indian Cities

| City | Latitude | Longitude |
|------|----------|-----------|
| New Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Kolkata | 22.5726 | 88.3639 |
| Chennai | 13.0827 | 80.2707 |
| Bangalore | 12.9716 | 77.5946 |
| Hyderabad | 17.3850 | 78.4867 |

## Workflow Examples

### Workflow 1: Geocode Addresses
1. Import CSV with lat/lon
2. Use Batch Process tab
3. Select precision 10
4. Export with DIGIPIN codes

### Workflow 2: Create Service Areas
1. Decode DIGIPIN codes
2. Use Generate Grid algorithm
3. Style by attributes
4. Create service area map

### Workflow 3: Analyze Coverage
1. Encode point layer
2. Generate grid at same precision
3. Join points to grid
4. Analyze distribution

## Support Resources

- **User Guide**: docs/user_guide.md
- **Installation**: docs/installation.md
- **GitHub**: github.com/sakyasingh/Q-DIGIPIN-India
- **Issues**: Report bugs on GitHub
- **Email**: sakyasingh@example.com

## Version Info

- **Current Version**: 1.0.0
- **QGIS Version**: 3.0+
- **License**: GPL v3

---

**Last Updated**: February 2026
