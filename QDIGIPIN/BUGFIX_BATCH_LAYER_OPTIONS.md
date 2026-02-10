# Bug Fix Report - Batch Processing Layer Options

## Issue: Create New Layer and Save Output Not Working

### Problem Description
When using the batch processing tab with an existing layer:
- **Create new layer** checkbox was being ignored
- **Save output to file** checkbox was being ignored
- The original layer was always modified in place
- No new layer was created even when the option was checked

### Root Cause
The `batch_encode_layer()` method was not checking the state of the `create_new_layer_check` and `save_to_file_check` checkboxes. It always modified the original layer directly without considering user preferences.

### Solution Implemented

#### 1. Check User Options
```python
create_new = self.create_new_layer_check.isChecked()
save_to_file = self.save_to_file_check.isChecked()
```

#### 2. Create Layer Copy if Requested
```python
if create_new:
    # Create a copy of the layer
    target_layer = self.create_layer_copy(layer, f'{layer.name()}_DIGIPIN')
else:
    # Work with the original layer
    target_layer = layer
```

#### 3. Add New Layer to Project
```python
if create_new:
    QgsProject.instance().addMapLayer(target_layer)
    self.status_label.setText(f'Created new layer: {target_layer.name()}')
```

#### 4. Save to File if Requested
```python
if save_to_file:
    self.save_layer_to_file(target_layer, field_name)
```

### New Helper Methods Added

#### `create_layer_copy(source_layer, new_name)`
- Creates a memory layer copy with the same:
  - Geometry type
  - CRS (Coordinate Reference System)
  - Fields
  - Features
- Returns the new layer (not added to project yet)

#### `save_layer_to_file(layer, field_name)`
- Prompts user to select file location and format
- Supports:
  - CSV files (with lat/lon columns)
  - GeoJSON files
- Shows success/error messages

#### `save_layer_as_csv(layer, file_path)`
- Writes layer to CSV format
- Includes all attributes
- Adds latitude and longitude columns
- UTF-8 encoding

### Files Modified
- `gui/main_dialog.py`
  - Modified `batch_encode_layer()` method (lines 733-820)
  - Added `create_layer_copy()` method
  - Added `save_layer_to_file()` method
  - Added `save_layer_as_csv()` method

### Behavior After Fix

#### Scenario 1: Both Options Unchecked
- ✅ Original layer is modified in place
- ✅ DIGIPIN field added to original layer
- ✅ No new layer created
- ✅ No file saved

#### Scenario 2: Create New Layer Checked
- ✅ Original layer remains unchanged
- ✅ New layer created with "_DIGIPIN" suffix
- ✅ New layer added to QGIS project
- ✅ DIGIPIN field added to new layer

#### Scenario 3: Save Output Checked
- ✅ Layer processed (original or new based on other option)
- ✅ File save dialog appears
- ✅ User can choose CSV or GeoJSON format
- ✅ File saved to selected location

#### Scenario 4: Both Options Checked
- ✅ New layer created
- ✅ New layer added to project
- ✅ File save dialog appears
- ✅ New layer saved to file
- ✅ Original layer unchanged

### Testing Checklist
- [x] Create new layer option works
- [x] Save to file option works
- [x] Both options together work
- [x] Neither option works (modifies original)
- [x] CSV export includes lat/lon
- [x] GeoJSON export works
- [x] Layer naming is correct
- [x] Progress bar updates
- [x] Status messages are accurate
- [x] Error handling works

### Version Update
- Current: 1.1.1 → 1.1.2 (bug fix)

---

**Status**: ✅ FIXED  
**Date**: February 10, 2026  
**Severity**: High (core feature not working)  
**Impact**: Users wanting to preserve original layers or export results
