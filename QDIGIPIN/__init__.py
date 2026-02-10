"""
Q-DIGIPIN India - QGIS Plugin
Professional geocoding plugin for India Post DIGIPIN system

Author: Sakyasingh Rout
License: GPL v3
"""

def classFactory(iface):
    """Load QDigipinIndia class from file qdigipin_india"""
    from .qdigipin_india import QDigipinIndia
    return QDigipinIndia(iface)
