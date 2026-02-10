"""
Decode DIGIPIN to Points Algorithm
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem
)
from qgis.PyQt.QtCore import QVariant

from ..core.digipin_engine import DigipinDecoder


class DecodeDigipinAlgorithm(QgsProcessingAlgorithm):
    """Decode DIGIPIN codes to point features"""
    
    INPUT = 'INPUT'
    DIGIPIN_FIELD = 'DIGIPIN_FIELD'
    OUTPUT = 'OUTPUT'
    
    def tr(self, string):
        return string
    
    def createInstance(self):
        return DecodeDigipinAlgorithm()
    
    def name(self):
        return 'decode_digipin'
    
    def displayName(self):
        return self.tr('Decode DIGIPIN to Points')
    
    def group(self):
        return self.tr('Decoding')
    
    def groupId(self):
        return 'decoding'
    
    def shortHelpString(self):
        return self.tr('Decode DIGIPIN codes to point features. '
                      'Creates point layer from DIGIPIN field.')
    
    def initAlgorithm(self, config=None):
        """Define algorithm parameters"""
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer with DIGIPIN codes'),
                [QgsProcessing.TypeVector]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterField(
                self.DIGIPIN_FIELD,
                self.tr('DIGIPIN field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output points')
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        """Process the algorithm"""
        
        # Get parameters
        source = self.parameterAsSource(parameters, self.INPUT, context)
        digipin_field = self.parameterAsString(parameters, self.DIGIPIN_FIELD, context)
        
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        
        # Prepare output fields
        fields = QgsFields()
        fields.append(QgsField('DIGIPIN', QVariant.String))
        fields.append(QgsField('Latitude', QVariant.Double))
        fields.append(QgsField('Longitude', QVariant.Double))
        fields.append(QgsField('MinLat', QVariant.Double))
        fields.append(QgsField('MaxLat', QVariant.Double))
        fields.append(QgsField('MinLon', QVariant.Double))
        fields.append(QgsField('MaxLon', QVariant.Double))
        
        # Create output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Point,
            QgsCoordinateReferenceSystem('EPSG:4326')
        )
        
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        
        # Get field index
        field_idx = source.fields().indexOf(digipin_field)
        if field_idx == -1:
            raise QgsProcessingException(f'Field {digipin_field} not found')
        
        # Process features
        total = source.featureCount()
        if total == 0:
            return {self.OUTPUT: dest_id}
        
        for current, feature in enumerate(source.getFeatures()):
            if feedback.isCanceled():
                break
            
            digipin = feature.attribute(digipin_field)
            
            if digipin:
                try:
                    # Decode DIGIPIN
                    result = DigipinDecoder.decode(str(digipin))
                    
                    # Create point feature
                    out_feature = QgsFeature(fields)
                    point = QgsPointXY(result['longitude'], result['latitude'])
                    out_feature.setGeometry(QgsGeometry.fromPointXY(point))
                    
                    # Set attributes
                    out_feature.setAttributes([
                        digipin,
                        result['latitude'],
                        result['longitude'],
                        result['bounds']['minLat'],
                        result['bounds']['maxLat'],
                        result['bounds']['minLon'],
                        result['bounds']['maxLon']
                    ])
                    
                    sink.addFeature(out_feature)
                    
                except ValueError as e:
                    feedback.reportError(f'Error decoding DIGIPIN {digipin}: {str(e)}')
            
            feedback.setProgress(int(current * 100 / total))
        
        return {self.OUTPUT: dest_id}
