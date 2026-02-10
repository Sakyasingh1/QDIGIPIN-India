"""
Grid generation utilities with optimized approach for high precision levels
"""

from qgis.core import (
    QgsVectorLayer, QgsFeature, QgsGeometry, QgsField,
    QgsRectangle, QgsPointXY, QgsProject
)
from qgis.PyQt.QtCore import QVariant
from ..core.digipin_engine import DigipinEncoder, DigipinDecoder
from ..core.constants import BOUNDS
import math


class OptimizedGridGenerator:
    """Optimized grid generator that prevents freezing for high precision levels"""
    
    @staticmethod
    def estimate_cell_count(extent, precision):
        """Estimate number of cells for given extent and precision"""
        lat_range = extent.yMaximum() - extent.yMinimum()
        lon_range = extent.xMaximum() - extent.xMinimum()
        
        # Approximate cells per degree at each precision level
        cells_per_degree = 4 ** precision / 36  # Rough estimate
        
        estimated_cells = lat_range * lon_range * cells_per_degree
        return int(estimated_cells)
    
    @staticmethod
    def generate_grid_chunked(extent, precision, progress_callback=None, max_cells=10000):
        """
        Generate grid with chunking to prevent freezing
        
        Args:
            extent: QgsRectangle defining the area
            precision: Precision level (1-10)
            progress_callback: Function to call with progress updates
            max_cells: Maximum cells to generate (safety limit)
        
        Returns:
            QgsVectorLayer: Generated grid layer
        """
        # Constrain to India bounds
        min_lat = max(extent.yMinimum(), BOUNDS['minLat'])
        max_lat = min(extent.yMaximum(), BOUNDS['maxLat'])
        min_lon = max(extent.xMinimum(), BOUNDS['minLon'])
        max_lon = min(extent.xMaximum(), BOUNDS['maxLon'])
        
        # Create layer
        layer = QgsVectorLayer('Polygon?crs=EPSG:4326', f'DIGIPIN_Grid_L{precision}', 'memory')
        provider = layer.dataProvider()
        
        # Add fields
        provider.addAttributes([
            QgsField('DIGIPIN', QVariant.String),
            QgsField('CenterLat', QVariant.Double),
            QgsField('CenterLon', QVariant.Double),
            QgsField('Precision', QVariant.Int),
            QgsField('Area_km2', QVariant.Double)
        ])
        layer.updateFields()
        
        # Use adaptive sampling based on precision
        if precision <= 5:
            # For low precision, sample more densely
            sample_points = 50
        elif precision <= 7:
            # Medium precision
            sample_points = 100
        else:
            # High precision - use intelligent sampling
            sample_points = 200
        
        lat_step = (max_lat - min_lat) / sample_points
        lon_step = (max_lon - min_lon) / sample_points
        
        # Collect unique DIGIPINs
        digipins_dict = {}
        total_samples = sample_points * sample_points
        processed = 0
        
        lat = min_lat
        while lat <= max_lat:
            lon = min_lon
            while lon <= max_lon:
                try:
                    digipin = DigipinEncoder.encode(lat, lon, precision)
                    if digipin not in digipins_dict:
                        digipins_dict[digipin] = True
                        
                        # Safety check
                        if len(digipins_dict) >= max_cells:
                            break
                            
                except ValueError:
                    pass
                
                lon += lon_step
                processed += 1
                
                if progress_callback and processed % 100 == 0:
                    progress = int((processed / total_samples) * 50)  # First 50% for sampling
                    progress_callback(progress)
            
            if len(digipins_dict) >= max_cells:
                break
            lat += lat_step
        
        # Create features in chunks
        features = []
        chunk_size = 100
        total_cells = len(digipins_dict)
        
        for idx, digipin in enumerate(digipins_dict.keys()):
            try:
                result = DigipinDecoder.decode(digipin)
                bounds = result['bounds']
                
                # Create polygon
                rect = QgsRectangle(
                    bounds['minLon'], bounds['minLat'],
                    bounds['maxLon'], bounds['maxLat']
                )
                
                polygon = QgsGeometry.fromRect(rect)
                
                # Calculate area in km²
                area_km2 = OptimizedGridGenerator.calculate_area_km2(
                    bounds['minLat'], bounds['maxLat'],
                    bounds['minLon'], bounds['maxLon']
                )
                
                # Create feature
                feature = QgsFeature()
                feature.setGeometry(polygon)
                feature.setAttributes([
                    digipin,
                    result['latitude'],
                    result['longitude'],
                    precision,
                    area_km2
                ])
                
                features.append(feature)
                
                # Add features in chunks
                if len(features) >= chunk_size:
                    provider.addFeatures(features)
                    features = []
                    
                    if progress_callback:
                        progress = 50 + int((idx / total_cells) * 50)  # Second 50% for feature creation
                        progress_callback(progress)
                        
            except ValueError:
                pass
        
        # Add remaining features
        if features:
            provider.addFeatures(features)
        
        layer.updateExtents()
        
        if progress_callback:
            progress_callback(100)
        
        return layer
    
    @staticmethod
    def calculate_area_km2(min_lat, max_lat, min_lon, max_lon):
        """Calculate approximate area in km²"""
        # Approximate using Haversine formula
        lat_diff = max_lat - min_lat
        lon_diff = max_lon - min_lon
        
        avg_lat = (min_lat + max_lat) / 2
        
        # 1 degree latitude ≈ 111 km
        # 1 degree longitude ≈ 111 * cos(latitude) km
        lat_km = lat_diff * 111
        lon_km = lon_diff * 111 * math.cos(math.radians(avg_lat))
        
        return lat_km * lon_km
