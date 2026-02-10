# Installation Guide - Q-DIGIPIN India

## System Requirements

- **QGIS Version**: 3.0 or higher
- **Python**: 3.6+ (included with QGIS)
- **Operating System**: Windows, Linux, or macOS
- **Disk Space**: ~5 MB

## Installation Methods

### Method 1: QGIS Plugin Repository (Recommended)

This is the easiest method once the plugin is published.

1. **Open QGIS**

2. **Open Plugin Manager**
   - Go to `Plugins` → `Manage and Install Plugins`
   - Or press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)

3. **Search for Plugin**
   - Click on the `All` tab
   - Type "Q-DIGIPIN India" in the search box

4. **Install**
   - Click on the plugin name
   - Click `Install Plugin` button
   - Wait for installation to complete

5. **Verify Installation**
   - Check `Installed` tab to see Q-DIGIPIN India
   - The plugin should be automatically enabled

### Method 2: Manual Installation from ZIP

Use this method for development or if installing from a downloaded ZIP file.

#### Windows

1. **Download Plugin**
   - Download the `Q-DIGIPIN-India.zip` file

2. **Locate Plugins Directory**
   ```
   C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
   ```
   
   **Quick Access:**
   - Press `Win+R`
   - Type: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins`
   - Press Enter

3. **Extract Plugin**
   - Extract the ZIP file to the plugins directory
   - The folder should be named `QDIGIPIN`
   - Final path: `.../plugins/QDIGIPIN/`

4. **Restart QGIS**

5. **Enable Plugin**
   - Go to `Plugins` → `Manage and Install Plugins`
   - Click `Installed` tab
   - Check the box next to "Q-DIGIPIN India"

#### Linux

1. **Download Plugin**
   - Download the `Q-DIGIPIN-India.zip` file

2. **Locate Plugins Directory**
   ```bash
   ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
   ```

3. **Extract Plugin**
   ```bash
   cd ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
   unzip /path/to/Q-DIGIPIN-India.zip
   ```

4. **Restart QGIS**

5. **Enable Plugin**
   - Go to `Plugins` → `Manage and Install Plugins`
   - Click `Installed` tab
   - Check the box next to "Q-DIGIPIN India"

#### macOS

1. **Download Plugin**
   - Download the `Q-DIGIPIN-India.zip` file

2. **Locate Plugins Directory**
   ```
   ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
   ```

3. **Extract Plugin**
   - Extract the ZIP file to the plugins directory
   - The folder should be named `QDIGIPIN`

4. **Restart QGIS**

5. **Enable Plugin**
   - Go to `Plugins` → `Manage and Install Plugins`
   - Click `Installed` tab
   - Check the box next to "Q-DIGIPIN India"

### Method 3: Install from Source (Development)

For developers who want to contribute or test the latest version.

1. **Clone Repository**
   ```bash
   git clone https://github.com/sakyasingh/Q-DIGIPIN-India.git
   ```

2. **Create Symbolic Link** (Linux/Mac)
   ```bash
   ln -s /path/to/Q-DIGIPIN-India ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QDIGIPIN
   ```

3. **Or Copy Files** (Windows)
   - Copy the entire folder to the plugins directory
   - Rename to `QDIGIPIN` if needed

4. **Restart QGIS**

5. **Enable Plugin**

## Verifying Installation

After installation, verify the plugin is working:

1. **Check Menu**
   - Look for `Vector` → `DIGIPIN India` in the menu bar

2. **Check Toolbar**
   - Look for the DIGIPIN icon in the toolbar

3. **Check Processing**
   - Open Processing Toolbox (`Ctrl+Alt+T`)
   - Look for "DIGIPIN India" provider

4. **Test Plugin**
   - Click the DIGIPIN icon or menu item
   - The main dialog should open
   - Try encoding a coordinate (e.g., 28.6139, 77.2090)

## Troubleshooting Installation

### Plugin doesn't appear

**Solution:**
1. Check that files are in correct directory
2. Folder must be named `QDIGIPIN` (not `Q-DIGIPIN-India` or similar)
3. Restart QGIS completely
4. Enable in Plugin Manager

### "Plugin is broken" error

**Possible causes:**
- Missing dependencies
- Incorrect Python version
- Corrupted files

**Solution:**
1. Reinstall the plugin
2. Check QGIS version (must be 3.0+)
3. Check error log: `Plugins` → `Python Console` → `Show Editor`

### Permission errors (Linux/Mac)

**Solution:**
```bash
chmod -R 755 ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QDIGIPIN
```

### Plugin loads but doesn't work

**Solution:**
1. Check Python console for errors
2. Verify all files are present
3. Try reinstalling
4. Report issue on GitHub

## Updating the Plugin

### From Plugin Repository

1. Go to `Plugins` → `Manage and Install Plugins`
2. Click `Upgradeable` tab
3. If Q-DIGIPIN India appears, click `Upgrade Plugin`

### Manual Update

1. Uninstall current version
2. Follow installation steps for new version

## Uninstalling

### From Plugin Manager

1. Go to `Plugins` → `Manage and Install Plugins`
2. Click `Installed` tab
3. Select "Q-DIGIPIN India"
4. Click `Uninstall Plugin`

### Manual Uninstall

1. Close QGIS
2. Delete the `QDIGIPIN` folder from plugins directory
3. Restart QGIS

## Getting Help

If you encounter issues:

1. **Check Documentation**
   - Read the User Guide
   - Check FAQ section

2. **Search Existing Issues**
   - Visit: https://github.com/sakyasingh/Q-DIGIPIN-India/issues

3. **Report New Issue**
   - Create a new issue with details
   - Include QGIS version and error messages

4. **Contact Support**
   - Email: sakyasingh@example.com

## Next Steps

After successful installation:

1. Read the [User Guide](user_guide.md)
2. Try the example workflows
3. Explore Processing algorithms
4. Join the community!

---

**Version**: 1.0.0  
**Last Updated**: February 2026
