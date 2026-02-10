<div align="center">

# 📍 Q-DIGIPIN India

### Professional Geocoding Plugin for QGIS

[![QGIS Version](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)
[![Python Version](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-1.1.1-orange.svg)](https://github.com/Sakyasingh1/Q-DIGIPIN-India/releases)

*Transform any location in India into a precise 10-character alphanumeric code*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## 🌟 Overview

**Q-DIGIPIN India** is a comprehensive QGIS plugin that seamlessly integrates India Post's revolutionary DIGIPIN geocoding system into your GIS workflow. DIGIPIN is a hierarchical geocoding system that converts any location in India into a unique, memorable 10-character alphanumeric code.

### 🎯 What is DIGIPIN?

DIGIPIN (Digital India Geographic Pin) is an innovative address system developed by India Post that provides:
- **Universal Coverage**: Every location in India gets a unique code
- **Hierarchical Structure**: From country-level to building-level precision
- **Easy to Remember**: Alphanumeric codes that are human-friendly
- **Precision Scalable**: 10 levels of accuracy from ~900km to ~3.4m

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔢 Encoding & Decoding
- Convert coordinates to DIGIPIN codes
- Reverse geocode DIGIPIN to coordinates
- Support for all 10 precision levels
- Flexible input formats (with/without hyphens)

</td>
<td width="50%">

### ⚡ Batch Processing
- Process entire point layers at once
- High-performance bulk operations
- Custom field naming
- Progress tracking

</td>
</tr>
<tr>
<td width="50%">

### 🗺️ Grid Generation
- Create DIGIPIN grid polygons
- Customizable extent and precision
- Perfect for spatial analysis
- Export to any vector format

</td>
<td width="50%">

### 🔧 QGIS Integration
- Native Processing Toolbox algorithms
- Modern tabbed interface
- Seamless layer integration
- Built-in validation

</td>
</tr>
</table>

---

## 📦 Installation

### Option 1: QGIS Plugin Manager (Recommended)

```bash
1. Open QGIS
2. Navigate to: Plugins → Manage and Install Plugins
3. Search for "Q-DIGIPIN India"
4. Click Install Plugin
```

### Option 2: Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

#### Windows
```powershell
# Extract plugin to:
C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

#### Linux
```bash
# Extract plugin to:
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

#### macOS
```bash
# Extract plugin to:
~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
```

**After extraction:**
1. Restart QGIS
2. Enable the plugin: `Plugins` → `Manage and Install Plugins`

</details>

---

## 🚀 Usage

### Quick Start Guide

#### 1️⃣ Encoding Coordinates to DIGIPIN

```
Vector → DIGIPIN India → Open DIGIPIN Tools → Encode Tab
```

1. Enter **latitude** and **longitude**
2. Select **precision level** (1-10)
3. Click **Encode to DIGIPIN**

**Example:**
```
Input:  Lat: 28.6139, Lon: 77.2090 (India Gate, Delhi)
Output: FCJ-3K4-LM9287 (Precision Level 10)
```

#### 2️⃣ Decoding DIGIPIN to Coordinates

```
Vector → DIGIPIN India → Open DIGIPIN Tools → Decode Tab
```

1. Enter **DIGIPIN code** (with or without hyphens)
2. Click **Decode DIGIPIN**

**Example:**
```
Input:  FCJ-3K4-LM9287
Output: Lat: 28.6139, Lon: 77.2090
```

#### 3️⃣ Batch Processing Layers

```
Vector → DIGIPIN India → Open DIGIPIN Tools → Batch Process Tab
```

1. Select a **point layer**
2. Choose **precision level**
3. Enter **output field name**
4. Click **Encode Layer to DIGIPIN**

### Processing Toolbox Algorithms

Access advanced tools from the **Processing Toolbox**:

```
Processing Toolbox → DIGIPIN India
├── Encoding
│   └── Encode Points to DIGIPIN
├── Decoding
│   └── Decode DIGIPIN to Points
└── Grid Operations
    └── Generate DIGIPIN Grid
```

---

## 📊 Precision Levels

<div align="center">

| Level | Accuracy | Grid Size | Typical Use Case | Example |
|:-----:|:--------:|:---------:|:-----------------|:--------|
| **1** | ~900 km | 900 × 900 km | Country/State level | `F--` |
| **2** | ~563 km | 563 × 563 km | Multi-state regions | `FC-` |
| **3** | ~56 km | 56 × 56 km | District level | `FCJ` |
| **4** | ~35 km | 35 × 35 km | Multiple cities | `FCJ-3` |
| **5** | ~3.5 km | 3.5 × 3.5 km | City/Town level | `FCJ-3K` |
| **6** | ~2.2 km | 2.2 × 2.2 km | Large neighborhoods | `FCJ-3K4` |
| **7** | ~219 m | 219 × 219 m | Neighborhood level | `FCJ-3K4-L` |
| **8** | ~137 m | 137 × 137 m | Street blocks | `FCJ-3K4-LM` |
| **9** | ~13.7 m | 13.7 × 13.7 m | Individual buildings | `FCJ-3K4-LM9` |
| **10** | ~3.4 m | 3.4 × 3.4 m | Precise address/door | `FCJ-3K4-LM9287` |

</div>

---

## 🔤 DIGIPIN Format

### Structure

DIGIPIN codes follow a standardized 10-character format:

```
XXX-XXX-XXXX

Example: FCJ-3K4-LM9287
         │   │   └─ Sub-location (4 chars)
         │   └───── Area code (3 chars)
         └───────── Region code (3 chars)
```

### Valid Characters

```
F C J 3 K 4 L M 9 2 8 7 P 5 6 T
```

> **Note:** Hyphens are optional but recommended for readability

---

## 🛠️ Requirements

- ![QGIS](https://img.shields.io/badge/QGIS-3.0+-green?style=flat-square) **QGIS 3.0 or higher**
- ![Python](https://img.shields.io/badge/Python-3.6+-blue?style=flat-square) **Python 3.6 or higher**
- Standard QGIS Python libraries (included)

---

## 📚 Documentation

### Resources

- 📖 **[Wiki](https://github.com/Sakyasingh1/Q-DIGIPIN-India/wiki)** - Comprehensive documentation
- 🎓 **[Tutorials](https://github.com/Sakyasingh1/Q-DIGIPIN-India/wiki/Tutorials)** - Step-by-step guides
- ❓ **[FAQ](https://github.com/Sakyasingh1/Q-DIGIPIN-India/wiki/FAQ)** - Common questions
- 🐛 **[Issue Tracker](https://github.com/Sakyasingh1/Q-DIGIPIN-India/issues)** - Report bugs

### API Reference

For developers integrating DIGIPIN into custom scripts, see the [API Documentation](https://github.com/Sakyasingh1/Q-DIGIPIN-India/wiki/API).

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Submit issues with detailed descriptions
- 💡 **Suggest Features**: Share your ideas for improvements
- 📝 **Improve Documentation**: Help make docs clearer
- 💻 **Submit Pull Requests**: Contribute code improvements

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright (C) 2026 Sakyasingh Rout

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

---

## 🙏 Credits

### DIGIPIN System
**Department of Posts, India Post, Government of India**

### Plugin Development
**Sakyasingh Rout** - *Initial work* - [@Sakyasingh1](https://github.com/Sakyasingh1)

---

## 📞 Support

<div align="center">

### Need Help?

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](https://github.com/Sakyasingh1/Q-DIGIPIN-India/issues)
[![Email](https://img.shields.io/badge/Email-Contact-blue?style=for-the-badge&logo=gmail)](mailto:routsakyasingh@gmail.com)

**Email:** routsakyasingh@gmail.com  
**Issues:** [GitHub Issue Tracker](https://github.com/Sakyasingh1/Q-DIGIPIN-India/issues)

</div>

---

## 📈 Changelog

### Version 1.1.1 (2026-02-10)

#### 🎉 Initial Release
- ✅ Core encoding/decoding functionality
- ✅ Batch processing support for point layers
- ✅ QGIS Processing Toolbox algorithms
- ✅ DIGIPIN grid generation
- ✅ Modern tabbed user interface
- ✅ Full support for precision levels 1-10
- ✅ Input validation and error handling

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## ⭐ Show Your Support

If you find this plugin useful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs and suggesting features
- 📢 Sharing with colleagues and the GIS community
- ☕ [Supporting the developer](https://github.com/sponsors/Sakyasingh1)

---

<div align="center">

**Made with ❤️ for the Indian GIS Community**

[![GitHub stars](https://img.shields.io/github/stars/Sakyasingh1/Q-DIGIPIN-India?style=social)](https://github.com/Sakyasingh1/Q-DIGIPIN-India/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Sakyasingh1/Q-DIGIPIN-India?style=social)](https://github.com/Sakyasingh1/Q-DIGIPIN-India/network/members)

</div>
