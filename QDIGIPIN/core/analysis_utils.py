"""
Spatial analysis utilities for DIGIPIN data
"""

from qgis.core import (
    QgsVectorLayer, QgsFeature, QgsGeometry, QgsField,
    QgsPointXY, QgsProject, QgsDistanceArea
)
from qgis.PyQt.QtCore import QVariant
from ..core.digipin_engine import DigipinEncoder, DigipinDecoder
from collections import defaultdict
import math


class DigipinSpatialAnalysis:
    """Spatial analysis tools for DIGIPIN data"""
    
    @staticmethod
    def calculate_density(layer, digipin_field, precision):
        """
        Calculate point density per DIGIPIN cell
        
        Args:
            layer: Input point layer
            digipin_field: Name of DIGIPIN field
            precision: Grid precision for density calculation
            
        Returns:
            dict: DIGIPIN -> count mapping
        """
        density_map = defaultdict(int)
        
        field_idx = layer.fields().indexOf(digipin_field)
        if field_idx == -1:
            return {}
        
        for feature in layer.getFeatures():
            digipin = feature.attribute(digipin_field)
            if digipin:
                # Truncate to specified precision if needed
                digipin_clean = digipin.replace('-', '')[:precision]
                density_map[digipin_clean] += 1
        
        return dict(density_map)
    
    @staticmethod
    def find_neighbors(digipin, include_diagonals=True):
        """
        Find neighboring DIGIPIN cells
        
        Args:
            digipin: DIGIPIN code
            include_diagonals: Include diagonal neighbors
            
        Returns:
            list: List of neighboring DIGIPIN codes
        """
        try:
            result = DigipinDecoder.decode(digipin)
            center_lat = result['latitude']
            center_lon = result['longitude']
            bounds = result['bounds']
            
            # Calculate cell size
            lat_size = bounds['maxLat'] - bounds['minLat']
            lon_size = bounds['maxLon'] - bounds['minLon']
            
            precision = len(digipin.replace('-', ''))
            
            neighbors = []
            
            # Define offsets for neighbors
            if include_diagonals:
                offsets = [
                    (-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)
                ]
            else:
                offsets = [
                    (-1, 0),
                    (0, -1), (0, 1),
                    (1, 0)
                ]
            
            for lat_offset, lon_offset in offsets:
                neighbor_lat = center_lat + (lat_offset * lat_size)
                neighbor_lon = center_lon + (lon_offset * lon_size)
                
                try:
                    neighbor_digipin = DigipinEncoder.encode(neighbor_lat, neighbor_lon, precision)
                    if neighbor_digipin != digipin:
                        neighbors.append(neighbor_digipin)
                except ValueError:
                    pass
            
            return neighbors
            
        except ValueError:
            return []
    
    @staticmethod
    def calculate_coverage(layer, digipin_field, total_area_km2=None):
        """
        Calculate coverage statistics
        
        Args:
            layer: Input layer with DIGIPIN field
            digipin_field: Name of DIGIPIN field
            total_area_km2: Total area to calculate coverage percentage
            
        Returns:
            dict: Coverage statistics
        """
        field_idx = layer.fields().indexOf(digipin_field)
        if field_idx == -1:
            return {}
        
        unique_digipins = set()
        precision_counts = defaultdict(int)
        
        for feature in layer.getFeatures():
            digipin = feature.attribute(digipin_field)
            if digipin:
                digipin_clean = digipin.replace('-', '')
                unique_digipins.add(digipin_clean)
                precision = len(digipin_clean)
                precision_counts[precision] += 1
        
        stats = {
            'unique_cells': len(unique_digipins),
            'precision_distribution': dict(precision_counts),
            'total_features': layer.featureCount()
        }
        
        if total_area_km2:
            # Estimate covered area (approximate)
            # This is a rough estimate based on average cell size
            avg_precision = sum(p * c for p, c in precision_counts.items()) / sum(precision_counts.values()) if precision_counts else 0
            if avg_precision > 0:
                from ..core.constants import PRECISION_INFO
                avg_cell_size = PRECISION_INFO.get(int(avg_precision), {}).get('cell_size_km', 1)
                covered_area = len(unique_digipins) * avg_cell_size
                stats['covered_area_km2'] = covered_area
                stats['coverage_percentage'] = (covered_area / total_area_km2) * 100 if total_area_km2 > 0 else 0
        
        return stats
    
    @staticmethod
    def calculate_distance_matrix(layer, digipin_field, max_features=100):
        """
        Calculate distance matrix between DIGIPIN centers
        
        Args:
            layer: Input layer
            digipin_field: DIGIPIN field name
            max_features: Maximum features to process (to prevent memory issues)
            
        Returns:
            dict: Distance matrix
        """
        field_idx = layer.fields().indexOf(digipin_field)
        if field_idx == -1:
            return {}
        
        # Collect DIGIPIN codes and their centers
        digipins = []
        centers = []
        
        count = 0
        for feature in layer.getFeatures():
            if count >= max_features:
                break
                
            digipin = feature.attribute(digipin_field)
            if digipin:
                try:
                    result = DigipinDecoder.decode(digipin)
                    digipins.append(digipin)
                    centers.append((result['latitude'], result['longitude']))
                    count += 1
                except ValueError:
                    pass
        
        # Calculate distances
        distance_calc = QgsDistanceArea()
        distance_calc.setEllipsoid('WGS84')
        
        matrix = {}
        for i, (digipin1, center1) in enumerate(zip(digipins, centers)):
            matrix[digipin1] = {}
            for j, (digipin2, center2) in enumerate(zip(digipins, centers)):
                if i != j:
                    point1 = QgsPointXY(center1[1], center1[0])
                    point2 = QgsPointXY(center2[1], center2[0])
                    distance_m = distance_calc.measureLine(point1, point2)
                    matrix[digipin1][digipin2] = distance_m / 1000  # Convert to km
        
        return matrix
    
    @staticmethod
    def create_density_layer(density_map, layer_name='DIGIPIN_Density'):
        """
        Create a layer visualizing density
        
        Args:
            density_map: Dictionary of DIGIPIN -> count
            layer_name: Name for the output layer
            
        Returns:
            QgsVectorLayer: Density visualization layer
        """
        layer = QgsVectorLayer('Polygon?crs=EPSG:4326', layer_name, 'memory')
        provider = layer.dataProvider()
        
        provider.addAttributes([
            QgsField('DIGIPIN', QVariant.String),
            QgsField('Count', QVariant.Int),
            QgsField('Density_Class', QVariant.String)
        ])
        layer.updateFields()
        
        if not density_map:
            return layer
        
        # Calculate density classes
        counts = list(density_map.values())
        max_count = max(counts)
        min_count = min(counts)
        
        features = []
        for digipin, count in density_map.items():
            try:
                result = DigipinDecoder.decode(digipin)
                bounds = result['bounds']
                
                # Create polygon
                from qgis.core import QgsRectangle
                rect = QgsRectangle(
                    bounds['minLon'], bounds['minLat'],
                    bounds['maxLon'], bounds['maxLat']
                )
                polygon = QgsGeometry.fromRect(rect)
                
                # Classify density
                if max_count > min_count:
                    normalized = (count - min_count) / (max_count - min_count)
                    if normalized < 0.25:
                        density_class = 'Low'
                    elif normalized < 0.5:
                        density_class = 'Medium-Low'
                    elif normalized < 0.75:
                        density_class = 'Medium-High'
                    else:
                        density_class = 'High'
                else:
                    density_class = 'Uniform'
                
                feature = QgsFeature()
                feature.setGeometry(polygon)
                feature.setAttributes([digipin, count, density_class])
                features.append(feature)
                
            except ValueError:
                pass
        
        provider.addFeatures(features)
        layer.updateExtents()
        
        return layer
