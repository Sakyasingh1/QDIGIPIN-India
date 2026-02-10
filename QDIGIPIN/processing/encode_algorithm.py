"""
Encode Points to DIGIPIN Algorithm
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QVariant

from ..core.digipin_engine import DigipinEncoder


class EncodePointsAlgorithm(QgsProcessingAlgorithm):
    """Encode point layer to DIGIPIN codes"""
    
    INPUT = 'INPUT'
    PRECISION = 'PRECISION'
    FIELD_NAME = 'FIELD_NAME'
    OUTPUT = 'OUTPUT'
    
    def tr(self, string):
        return string
    
    def createInstance(self):
        return EncodePointsAlgorithm()
    
    def name(self):
        return 'encode_points'
    
    def displayName(self):
        return self.tr('Encode Points to DIGIPIN')
    
    def group(self):
        return self.tr('Encoding')
    
    def groupId(self):
        return 'encoding'
    
    def shortHelpString(self):
        return self.tr('Encode point features to DIGIPIN codes. '
                      'Adds a new field with DIGIPIN codes for each point.')
    
    def initAlgorithm(self, config=None):
        """Define algorithm parameters"""
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input point layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PRECISION,
                self.tr('Precision level (1-10)'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=10,
                minValue=1,
                maxValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.FIELD_NAME,
                self.tr('Output field name'),
                defaultValue='DIGIPIN'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        """Process the algorithm"""
        
        # Get parameters
        source = self.parameterAsSource(parameters, self.INPUT, context)
        precision = self.parameterAsInt(parameters, self.PRECISION, context)
        field_name = self.parameterAsString(parameters, self.FIELD_NAME, context)
        
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        
        # Prepare output fields
        fields = source.fields()
        fields.append(QgsField(field_name, QVariant.String))
        
        # Create output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs()
        )
        
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
        
        # Process features
        total = source.featureCount()
        if total == 0:
            return {self.OUTPUT: dest_id}
        
        for current, feature in enumerate(source.getFeatures()):
            if feedback.isCanceled():
                break
            
            # Get point coordinates
            geom = feature.geometry()
            if geom and not geom.isNull():
                point = geom.asPoint()
                
                try:
                    # Encode to DIGIPIN
                    digipin = DigipinEncoder.encode(point.y(), point.x(), precision)
                    
                    # Create output feature
                    out_feature = QgsFeature(fields)
                    out_feature.setGeometry(geom)
                    
                    # Copy attributes
                    for i, attr in enumerate(feature.attributes()):
                        out_feature.setAttribute(i, attr)
                    
                    # Add DIGIPIN
                    out_feature.setAttribute(field_name, digipin)
                    
                    sink.addFeature(out_feature)
                    
                except ValueError as e:
                    feedback.reportError(f'Error encoding feature {feature.id()}: {str(e)}')
            
            feedback.setProgress(int(current * 100 / total))
        
        return {self.OUTPUT: dest_id}
