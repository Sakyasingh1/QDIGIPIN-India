"""
Generate DIGIPIN Grid Algorithm
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsRectangle,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem
)
from qgis.PyQt.QtCore import QVariant

from ..core.digipin_engine import DigipinEncoder, DigipinDecoder
from ..core.constants import BOUNDS


class GenerateGridAlgorithm(QgsProcessingAlgorithm):
    """Generate DIGIPIN grid for a given extent"""
    
    EXTENT = 'EXTENT'
    PRECISION = 'PRECISION'
    OUTPUT = 'OUTPUT'
    
    def tr(self, string):
        return string
    
    def createInstance(self):
        return GenerateGridAlgorithm()
    
    def name(self):
        return 'generate_grid'
    
    def displayName(self):
        return self.tr('Generate DIGIPIN Grid')
    
    def group(self):
        return self.tr('Grid Operations')
    
    def groupId(self):
        return 'grid'
    
    def shortHelpString(self):
        return self.tr('Generate a DIGIPIN grid for the specified extent. '
                      'Creates polygon features for each DIGIPIN cell.')
    
    def initAlgorithm(self, config=None):
        """Define algorithm parameters"""
        
        self.addParameter(
            QgsProcessingParameterExtent(
                self.EXTENT,
                self.tr('Grid extent')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PRECISION,
                self.tr('Precision level (1-10)'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=5,
                minValue=1,
                maxValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output grid')
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        """Process the algorithm"""
        
        # Get parameters
        extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        precision = self.parameterAsInt(parameters, self.PRECISION, context)
        
        # Prepare output fields
        fields = QgsFields()
        fields.append(QgsField('DIGIPIN', QVariant.String))
        fields.append(QgsField('CenterLat', QVariant.Double))
        fields.append(QgsField('CenterLon', QVariant.Double))
        fields.append(QgsField('Precision', QVariant.Int))
        
        # Create output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            QgsCoordinateReferenceSystem('EPSG:4326')
        )
        
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        
        # Constrain extent to India bounds
        min_lat = max(extent.yMinimum(), BOUNDS['minLat'])
        max_lat = min(extent.yMaximum(), BOUNDS['maxLat'])
        min_lon = max(extent.xMinimum(), BOUNDS['minLon'])
        max_lon = min(extent.xMaximum(), BOUNDS['maxLon'])
        
        # Generate grid
        feedback.pushInfo(f'Generating grid at precision level {precision}...')
        
        # Calculate step size based on precision
        # This is approximate - we'll generate points and get their DIGIPINs
        lat_step = (max_lat - min_lat) / 20  # Adjust density as needed
        lon_step = (max_lon - min_lon) / 20
        
        digipins_set = set()
        
        # Sample points to find unique DIGIPINs in extent
        lat = min_lat
        while lat <= max_lat:
            lon = min_lon
            while lon <= max_lon:
                try:
                    digipin = DigipinEncoder.encode(lat, lon, precision)
                    digipins_set.add(digipin)
                except ValueError:
                    pass
                lon += lon_step
            lat += lat_step
        
        # Create polygon for each unique DIGIPIN
        total = len(digipins_set)
        for current, digipin in enumerate(digipins_set):
            if feedback.isCanceled():
                break
            
            try:
                # Decode to get bounds
                result = DigipinDecoder.decode(digipin)
                bounds = result['bounds']
                
                # Create polygon
                rect = QgsRectangle(
                    bounds['minLon'], bounds['minLat'],
                    bounds['maxLon'], bounds['maxLat']
                )
                
                polygon = QgsGeometry.fromRect(rect)
                
                # Create feature
                feature = QgsFeature(fields)
                feature.setGeometry(polygon)
                feature.setAttributes([
                    digipin,
                    result['latitude'],
                    result['longitude'],
                    precision
                ])
                
                sink.addFeature(feature)
                
            except ValueError as e:
                feedback.reportError(f'Error processing DIGIPIN {digipin}: {str(e)}')
            
            feedback.setProgress(int(current * 100 / total))
        
        feedback.pushInfo(f'Generated {total} grid cells')
        
        return {self.OUTPUT: dest_id}
