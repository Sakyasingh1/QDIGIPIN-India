"""
DIGIPIN Processing Provider
"""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
import os

from .encode_algorithm import EncodePointsAlgorithm
from .decode_algorithm import DecodeDigipinAlgorithm
from .generate_grid_algorithm import GenerateGridAlgorithm


class DigipinProvider(QgsProcessingProvider):
    """QGIS Processing provider for DIGIPIN tools"""
    
    def __init__(self):
        super().__init__()
        self.algs = []
    
    def id(self):
        """Unique provider id"""
        return 'digipin'
    
    def name(self):
        """Human readable name"""
        return 'DIGIPIN India'
    
    def icon(self):
        """Provider icon"""
        return QIcon()
    
    def loadAlgorithms(self):
        """Load all algorithms"""
        self.addAlgorithm(EncodePointsAlgorithm())
        self.addAlgorithm(DecodeDigipinAlgorithm())
        self.addAlgorithm(GenerateGridAlgorithm())
