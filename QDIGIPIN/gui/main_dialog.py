"""
Main Dialog for Q-DIGIPIN India Plugin
"""

from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QPushButton, QLabel, QProgressBar, QMessageBox,
    QWidget, QGroupBox, QFormLayout, QLineEdit,
    QSpinBox, QComboBox, QTextEdit, QCheckBox,
    QFileDialog, QTableWidget, QTableWidgetItem
)
from qgis.PyQt.QtGui import QFont
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry,
    QgsPointXY, QgsField, QgsFields, QgsCoordinateReferenceSystem,
    QgsVectorFileWriter, QgsWkbTypes
)
from qgis.PyQt.QtCore import QVariant

from ..core.digipin_engine import DigipinEncoder, DigipinDecoder, DigipinValidator
from ..core.constants import PRECISION_INFO, DEFAULT_PRECISION


class QDigipinMainDialog(QDialog):
    """Main dialog for DIGIPIN tools"""
    
    def __init__(self, iface, plugin_dir, parent=None):
        """Constructor"""
        super(QDigipinMainDialog, self).__init__(parent)
        self.iface = iface
        self.plugin_dir = plugin_dir
        
        self.setWindowTitle('Q-DIGIPIN India - Geocoding Tools')
        self.setMinimumSize(800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('<h2>Q-DIGIPIN India</h2>')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Professional Geocoding Plugin for India Post DIGIPIN System')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.encode_tab = self.create_encode_tab()
        self.decode_tab = self.create_decode_tab()
        self.batch_tab = self.create_batch_tab()
        self.grid_tab = self.create_grid_tab()
        self.analysis_tab = self.create_analysis_tab()
        self.about_tab = self.create_about_tab()
        
        self.tabs.addTab(self.encode_tab, '📤 Encode')
        self.tabs.addTab(self.decode_tab, '📥 Decode')
        self.tabs.addTab(self.batch_tab, '⚙️ Batch Process')
        self.tabs.addTab(self.grid_tab, '🔲 Grid Visualization')
        self.tabs.addTab(self.analysis_tab, '📊 Spatial Analysis')
        self.tabs.addTab(self.about_tab, 'ℹ️ About')
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.status_label = QLabel('Ready')
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Close button
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def create_encode_tab(self):
        """Create the encoding tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Input group
        input_group = QGroupBox('Input Coordinates')
        input_layout = QFormLayout()
        
        self.encode_lat_input = QLineEdit()
        self.encode_lat_input.setPlaceholderText('e.g., 28.6139')
        input_layout.addRow('Latitude:', self.encode_lat_input)
        
        self.encode_lon_input = QLineEdit()
        self.encode_lon_input.setPlaceholderText('e.g., 77.2090')
        input_layout.addRow('Longitude:', self.encode_lon_input)
        
        self.encode_precision = QSpinBox()
        self.encode_precision.setMinimum(1)
        self.encode_precision.setMaximum(10)
        self.encode_precision.setValue(DEFAULT_PRECISION)
        self.encode_precision.valueChanged.connect(self.update_precision_info)
        input_layout.addRow('Precision Level:', self.encode_precision)
        
        self.precision_info_label = QLabel()
        self.update_precision_info()
        input_layout.addRow('Accuracy:', self.precision_info_label)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Encode button
        encode_btn = QPushButton('Encode to DIGIPIN')
        encode_btn.clicked.connect(self.encode_coordinates)
        layout.addWidget(encode_btn)
        
        # Result group
        result_group = QGroupBox('Result')
        result_layout = QVBoxLayout()
        
        self.encode_result = QTextEdit()
        self.encode_result.setReadOnly(True)
        self.encode_result.setMaximumHeight(150)
        result_layout.addWidget(self.encode_result)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        copy_btn = QPushButton('Copy DIGIPIN')
        copy_btn.clicked.connect(self.copy_encoded_result)
        btn_layout.addWidget(copy_btn)
        
        create_layer_btn = QPushButton('Create Point Layer')
        create_layer_btn.clicked.connect(self.create_point_from_encode)
        btn_layout.addWidget(create_layer_btn)
        
        result_layout.addLayout(btn_layout)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_decode_tab(self):
        """Create the decoding tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Input group
        input_group = QGroupBox('Input DIGIPIN')
        input_layout = QFormLayout()
        
        self.decode_input = QLineEdit()
        self.decode_input.setPlaceholderText('e.g., FCJ-3K4-LM9')
        input_layout.addRow('DIGIPIN Code:', self.decode_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Decode button
        decode_btn = QPushButton('Decode DIGIPIN')
        decode_btn.clicked.connect(self.decode_digipin)
        layout.addWidget(decode_btn)
        
        # Result group
        result_group = QGroupBox('Result')
        result_layout = QVBoxLayout()
        
        self.decode_result = QTextEdit()
        self.decode_result.setReadOnly(True)
        self.decode_result.setMaximumHeight(200)
        result_layout.addWidget(self.decode_result)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        copy_coords_btn = QPushButton('Copy Coordinates')
        copy_coords_btn.clicked.connect(self.copy_decoded_coords)
        btn_layout.addWidget(copy_coords_btn)
        
        create_point_btn = QPushButton('Create Point Layer')
        create_point_btn.clicked.connect(self.create_point_from_decode)
        btn_layout.addWidget(create_point_btn)
        
        zoom_btn = QPushButton('Zoom to Location')
        zoom_btn.clicked.connect(self.zoom_to_decoded)
        btn_layout.addWidget(zoom_btn)
        
        result_layout.addLayout(btn_layout)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_batch_tab(self):
        """Create the batch processing tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Input source selection
        source_group = QGroupBox('Input Source')
        source_layout = QVBoxLayout()
        
        # Radio buttons for source type
        from qgis.PyQt.QtWidgets import QRadioButton, QButtonGroup
        self.batch_source_group = QButtonGroup()
        
        self.batch_layer_radio = QRadioButton('Existing Layer')
        self.batch_layer_radio.setChecked(True)
        self.batch_layer_radio.toggled.connect(self.toggle_batch_source)
        self.batch_source_group.addButton(self.batch_layer_radio, 0)
        source_layout.addWidget(self.batch_layer_radio)
        
        self.batch_file_radio = QRadioButton('Import from File (CSV/GeoJSON)')
        self.batch_file_radio.toggled.connect(self.toggle_batch_source)
        self.batch_source_group.addButton(self.batch_file_radio, 1)
        source_layout.addWidget(self.batch_file_radio)
        
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)
        
        # Layer selection group
        self.layer_group = QGroupBox('Select Existing Layer')
        layer_layout = QFormLayout()
        
        self.layer_combo = QComboBox()
        self.refresh_layers()
        layer_layout.addRow('Select Layer:', self.layer_combo)
        
        refresh_btn = QPushButton('Refresh Layers')
        refresh_btn.clicked.connect(self.refresh_layers)
        layer_layout.addRow('', refresh_btn)
        
        self.layer_group.setLayout(layer_layout)
        layout.addWidget(self.layer_group)
        
        # File import group
        self.file_group = QGroupBox('Import from File')
        file_layout = QFormLayout()
        
        file_select_layout = QHBoxLayout()
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText('Select CSV or GeoJSON file...')
        self.file_path_input.setReadOnly(True)
        file_select_layout.addWidget(self.file_path_input)
        
        browse_btn = QPushButton('Browse...')
        browse_btn.clicked.connect(self.browse_input_file)
        file_select_layout.addWidget(browse_btn)
        
        file_layout.addRow('Input File:', file_select_layout)
        
        # CSV field mapping (only for CSV files)
        self.csv_lat_combo = QComboBox()
        self.csv_lon_combo = QComboBox()
        file_layout.addRow('Latitude Field:', self.csv_lat_combo)
        file_layout.addRow('Longitude Field:', self.csv_lon_combo)
        
        self.file_group.setLayout(file_layout)
        self.file_group.setVisible(False)
        layout.addWidget(self.file_group)
        
        # Common settings
        settings_group = QGroupBox('Processing Settings')
        settings_layout = QFormLayout()
        
        self.batch_precision = QSpinBox()
        self.batch_precision.setMinimum(1)
        self.batch_precision.setMaximum(10)
        self.batch_precision.setValue(DEFAULT_PRECISION)
        settings_layout.addRow('Precision Level:', self.batch_precision)
        
        self.output_field_name = QLineEdit('DIGIPIN')
        settings_layout.addRow('Output Field Name:', self.output_field_name)
        
        # Output options
        self.create_new_layer_check = QCheckBox('Create new layer with results')
        self.create_new_layer_check.setChecked(True)
        settings_layout.addRow('', self.create_new_layer_check)
        
        self.save_to_file_check = QCheckBox('Save output to file')
        settings_layout.addRow('', self.save_to_file_check)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Process button
        process_btn = QPushButton('Process and Encode to DIGIPIN')
        process_btn.setStyleSheet('QPushButton { font-weight: bold; padding: 8px; }')
        process_btn.clicked.connect(self.batch_process)
        layout.addWidget(process_btn)
        
        # Results
        self.batch_result = QTextEdit()
        self.batch_result.setReadOnly(True)
        self.batch_result.setMaximumHeight(150)
        layout.addWidget(self.batch_result)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_grid_tab(self):
        """Create the grid visualization tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Grid settings
        settings_group = QGroupBox('Grid Settings')
        settings_layout = QFormLayout()
        
        # Extent selection
        self.grid_extent_combo = QComboBox()
        self.grid_extent_combo.addItems(['Current Map Extent', 'Layer Extent', 'Custom Extent'])
        self.grid_extent_combo.currentIndexChanged.connect(self.toggle_grid_extent_options)
        settings_layout.addRow('Extent Source:', self.grid_extent_combo)
        
        # Layer selection for extent
        self.grid_layer_combo = QComboBox()
        self.grid_layer_combo.setVisible(False)
        settings_layout.addRow('Select Layer:', self.grid_layer_combo)
        
        # Precision with warning
        precision_layout = QHBoxLayout()
        self.grid_precision = QSpinBox()
        self.grid_precision.setMinimum(1)
        self.grid_precision.setMaximum(10)
        self.grid_precision.setValue(5)
        self.grid_precision.valueChanged.connect(self.update_grid_warning)
        precision_layout.addWidget(self.grid_precision)
        
        self.grid_warning_label = QLabel()
        self.grid_warning_label.setStyleSheet('color: #dc3545; font-weight: bold;')
        precision_layout.addWidget(self.grid_warning_label)
        settings_layout.addRow('Precision Level:', precision_layout)
        
        # Grid options
        self.grid_labels_check = QCheckBox('Add DIGIPIN labels')
        self.grid_labels_check.setChecked(True)
        settings_layout.addRow('', self.grid_labels_check)
        
        self.grid_style_combo = QComboBox()
        self.grid_style_combo.addItems(['Simple', 'Colored by Precision', 'Gradient'])
        settings_layout.addRow('Grid Style:', self.grid_style_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Generate button
        generate_btn = QPushButton('🔲 Generate DIGIPIN Grid')
        generate_btn.setStyleSheet('QPushButton { font-weight: bold; padding: 10px; background-color: #007bff; color: white; } QPushButton:hover { background-color: #0056b3; }')
        generate_btn.clicked.connect(self.generate_grid)
        layout.addWidget(generate_btn)
        
        # Info/Results
        self.grid_result = QTextEdit()
        self.grid_result.setReadOnly(True)
        self.grid_result.setMaximumHeight(150)
        layout.addWidget(self.grid_result)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_analysis_tab(self):
        """Create the spatial analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Analysis type selection
        analysis_group = QGroupBox('Analysis Type')
        analysis_layout = QVBoxLayout()
        
        from qgis.PyQt.QtWidgets import QRadioButton, QButtonGroup
        self.analysis_type_group = QButtonGroup()
        
        self.analysis_density_radio = QRadioButton('Point Density Analysis')
        self.analysis_density_radio.setChecked(True)
        self.analysis_type_group.addButton(self.analysis_density_radio, 0)
        analysis_layout.addWidget(self.analysis_density_radio)
        
        self.analysis_coverage_radio = QRadioButton('Coverage Analysis')
        self.analysis_type_group.addButton(self.analysis_coverage_radio, 1)
        analysis_layout.addWidget(self.analysis_coverage_radio)
        
        self.analysis_neighbors_radio = QRadioButton('Find Neighboring DIGIPINs')
        self.analysis_type_group.addButton(self.analysis_neighbors_radio, 2)
        analysis_layout.addWidget(self.analysis_neighbors_radio)
        
        self.analysis_distance_radio = QRadioButton('Distance Matrix')
        self.analysis_type_group.addButton(self.analysis_distance_radio, 3)
        analysis_layout.addWidget(self.analysis_distance_radio)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # Input layer selection
        input_group = QGroupBox('Input Data')
        input_layout = QFormLayout()
        
        self.analysis_layer_combo = QComboBox()
        input_layout.addRow('Select Layer:', self.analysis_layer_combo)
        
        refresh_analysis_btn = QPushButton('Refresh Layers')
        refresh_analysis_btn.clicked.connect(self.refresh_analysis_layers)
        input_layout.addRow('', refresh_analysis_btn)
        
        # Create the field combo BEFORE calling refresh (important!)
        self.analysis_digipin_field = QComboBox()
        input_layout.addRow('DIGIPIN Field:', self.analysis_digipin_field)
        
        # Now it's safe to call refresh
        self.refresh_analysis_layers()
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Analysis parameters
        params_group = QGroupBox('Parameters')
        params_layout = QFormLayout()
        
        self.analysis_precision = QSpinBox()
        self.analysis_precision.setMinimum(1)
        self.analysis_precision.setMaximum(10)
        self.analysis_precision.setValue(7)
        params_layout.addRow('Grid Precision:', self.analysis_precision)
        
        self.analysis_include_diagonals = QCheckBox('Include diagonal neighbors')
        self.analysis_include_diagonals.setChecked(True)
        params_layout.addRow('', self.analysis_include_diagonals)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Run analysis button
        run_btn = QPushButton('📊 Run Analysis')
        run_btn.setStyleSheet('QPushButton { font-weight: bold; padding: 10px; background-color: #28a745; color: white; } QPushButton:hover { background-color: #218838; }')
        run_btn.clicked.connect(self.run_spatial_analysis)
        layout.addWidget(run_btn)
        
        # Results
        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        self.analysis_result.setMaximumHeight(200)
        layout.addWidget(self.analysis_result)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_about_tab(self):
        """Create the about tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml('''
            <h2>Q-DIGIPIN India</h2>
            <p><b>Version:</b> 1.0.0</p>
            <p><b>Author:</b> Sakyasingh Rout</p>
            <p><b>License:</b> GPL v3</p>
            
            <h3>About DIGIPIN</h3>
            <p>DIGIPIN is a hierarchical geocoding system developed by India Post, 
            Department of Posts. It converts any location in India into a 10-character 
            alphanumeric code.</p>
            
            <h3>Features</h3>
            <ul>
                <li>Encode coordinates to DIGIPIN codes</li>
                <li>Decode DIGIPIN codes to coordinates</li>
                <li>Batch process entire point layers</li>
                <li>Support for 1-10 precision levels</li>
                <li>Create point and polygon layers</li>
                <li>Export to multiple formats</li>
            </ul>
            
            <h3>Precision Levels</h3>
            <ul>
                <li>Level 1: ~900 km accuracy</li>
                <li>Level 5: ~3.5 km accuracy</li>
                <li>Level 10: ~3.4 m accuracy</li>
            </ul>
            
            <h3>Credits</h3>
            <p>DIGIPIN System: Department of Posts, India Post, Government of India</p>
            
            <p><i>This plugin is open source and released under GPL v3 license.</i></p>
        ''')
        layout.addWidget(about_text)
        
        widget.setLayout(layout)
        return widget
    
    def update_precision_info(self):
        """Update precision information label"""
        precision = self.encode_precision.value()
        info = PRECISION_INFO.get(precision, {})
        self.precision_info_label.setText(info.get('accuracy', 'N/A'))
    
    def encode_coordinates(self):
        """Encode coordinates to DIGIPIN"""
        try:
            lat = float(self.encode_lat_input.text())
            lon = float(self.encode_lon_input.text())
            precision = self.encode_precision.value()
            
            # Validate
            is_valid, error_msg = DigipinValidator.validate_coordinates(lat, lon)
            if not is_valid:
                QMessageBox.warning(self, 'Validation Error', error_msg)
                return
            
            # Encode
            digipin = DigipinEncoder.encode(lat, lon, precision)
            
            # Display result with enhanced styling
            result_text = f'''
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Encoding Successful</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📍 Input Coordinates:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Latitude: <span style="color: #007bff; font-weight: bold;">{lat}°</span></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Longitude: <span style="color: #007bff; font-weight: bold;">{lon}°</span></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Precision: <span style="color: #28a745; font-weight: bold;">Level {precision}</span></p>
</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; margin-top: 15px; text-align: center;">
    <p style="margin: 0 0 8px 0; color: #fff; font-size: 14px; font-weight: 600;">🔐 DIGIPIN CODE</p>
    <p style="margin: 0; font-size: 32px; font-weight: bold; color: #fff; letter-spacing: 3px; font-family: 'Courier New', monospace; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{digipin}</p>
</div>

<div style="background: #e7f3ff; padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 4px solid #007bff;">
    <p style="margin: 0; color: #004085;"><b>📏 Accuracy:</b> <span style="color: #0056b3;">{PRECISION_INFO[precision]['accuracy']}</span></p>
    <p style="margin: 5px 0 0 0; color: #004085; font-size: 12px;"><i>Cell size: ~{PRECISION_INFO[precision]['cell_size_km']} km</i></p>
</div>
            '''
            
            self.encode_result.setHtml(result_text)
            self.status_label.setText(f'✓ Successfully encoded to: {digipin}')
            
            # Store for later use
            self.last_encoded_digipin = digipin
            self.last_encoded_lat = lat
            self.last_encoded_lon = lon
            
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def decode_digipin(self):
        """Decode DIGIPIN to coordinates"""
        try:
            digipin = self.decode_input.text().strip()
            
            # Validate
            is_valid, error_msg = DigipinValidator.validate_digipin(digipin)
            if not is_valid:
                QMessageBox.warning(self, 'Validation Error', error_msg)
                return
            
            # Decode
            result = DigipinDecoder.decode(digipin)
            
            # Display result with enhanced styling
            formatted_digipin = DigipinValidator.format_digipin(digipin)
            precision_level = len(digipin.replace('-', ''))
            
            result_text = f'''
<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Decoding Successful</h3>
</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; margin-top: 15px; text-align: center;">
    <p style="margin: 0 0 8px 0; color: #fff; font-size: 14px; font-weight: 600;">🔓 DIGIPIN CODE</p>
    <p style="margin: 0; font-size: 28px; font-weight: bold; color: #fff; letter-spacing: 3px; font-family: 'Courier New', monospace; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{formatted_digipin}</p>
    <p style="margin: 8px 0 0 0; color: #fff; font-size: 12px;">Precision Level {precision_level}</p>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 15px;">
    <p style="margin: 0 0 10px 0; color: #495057; font-weight: bold;">📍 Center Coordinates:</p>
    <div style="background: white; padding: 12px; border-radius: 6px; border: 2px solid #28a745;">
        <p style="margin: 5px 0; color: #155724;"><b>Latitude:</b> <span style="color: #28a745; font-size: 18px; font-weight: bold;">{result['latitude']}°</span></p>
        <p style="margin: 5px 0; color: #155724;"><b>Longitude:</b> <span style="color: #28a745; font-size: 18px; font-weight: bold;">{result['longitude']}°</span></p>
    </div>
</div>

<div style="background: #fff3cd; padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 4px solid #ffc107;">
    <p style="margin: 0 0 8px 0; color: #856404; font-weight: bold;">📦 Bounding Box:</p>
    <p style="margin: 3px 0; color: #856404; font-size: 13px;">▪ Min Latitude: <b>{result['bounds']['minLat']}</b></p>
    <p style="margin: 3px 0; color: #856404; font-size: 13px;">▪ Max Latitude: <b>{result['bounds']['maxLat']}</b></p>
    <p style="margin: 3px 0; color: #856404; font-size: 13px;">▪ Min Longitude: <b>{result['bounds']['minLon']}</b></p>
    <p style="margin: 3px 0; color: #856404; font-size: 13px;">▪ Max Longitude: <b>{result['bounds']['maxLon']}</b></p>
</div>

<div style="background: #d1ecf1; padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 4px solid #17a2b8;">
    <p style="margin: 0; color: #0c5460;"><b>📏 Accuracy:</b> <span style="color: #117a8b;">{PRECISION_INFO.get(precision_level, {}).get('accuracy', 'N/A')}</span></p>
</div>
            '''
            
            self.decode_result.setHtml(result_text)
            self.status_label.setText(f'✓ Successfully decoded: {formatted_digipin}')
            
            # Store for later use
            self.last_decoded_result = result
            self.last_decoded_digipin = digipin
            
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def copy_encoded_result(self):
        """Copy encoded DIGIPIN to clipboard"""
        if hasattr(self, 'last_encoded_digipin'):
            from qgis.PyQt.QtWidgets import QApplication
            QApplication.clipboard().setText(self.last_encoded_digipin)
            self.status_label.setText('DIGIPIN copied to clipboard')
        else:
            QMessageBox.information(self, 'Info', 'Please encode coordinates first')
    
    def copy_decoded_coords(self):
        """Copy decoded coordinates to clipboard"""
        if hasattr(self, 'last_decoded_result'):
            from qgis.PyQt.QtWidgets import QApplication
            coords = f"{self.last_decoded_result['latitude']}, {self.last_decoded_result['longitude']}"
            QApplication.clipboard().setText(coords)
            self.status_label.setText('Coordinates copied to clipboard')
        else:
            QMessageBox.information(self, 'Info', 'Please decode a DIGIPIN first')
    
    def create_point_from_encode(self):
        """Create a point layer from encoded result"""
        if not hasattr(self, 'last_encoded_digipin'):
            QMessageBox.information(self, 'Info', 'Please encode coordinates first')
            return
        
        self.create_point_layer(
            self.last_encoded_lat,
            self.last_encoded_lon,
            self.last_encoded_digipin,
            'Encoded_Point'
        )
    
    def create_point_from_decode(self):
        """Create a point layer from decoded result"""
        if not hasattr(self, 'last_decoded_result'):
            QMessageBox.information(self, 'Info', 'Please decode a DIGIPIN first')
            return
        
        result = self.last_decoded_result
        self.create_point_layer(
            result['latitude'],
            result['longitude'],
            self.last_decoded_digipin,
            'Decoded_Point'
        )
    
    def create_point_layer(self, lat, lon, digipin, layer_name):
        """Create a point layer and add to map"""
        # Create layer
        layer = QgsVectorLayer('Point?crs=EPSG:4326', layer_name, 'memory')
        provider = layer.dataProvider()
        
        # Add fields
        provider.addAttributes([
            QgsField('DIGIPIN', QVariant.String),
            QgsField('Latitude', QVariant.Double),
            QgsField('Longitude', QVariant.Double)
        ])
        layer.updateFields()
        
        # Create feature
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
        feature.setAttributes([digipin, lat, lon])
        
        provider.addFeature(feature)
        layer.updateExtents()
        
        # Add to project
        QgsProject.instance().addMapLayer(layer)
        
        # Zoom to feature
        self.iface.mapCanvas().setExtent(layer.extent())
        self.iface.mapCanvas().refresh()
        
        self.status_label.setText(f'Created layer: {layer_name}')
        QMessageBox.information(self, 'Success', f'Point layer "{layer_name}" created and added to map')
    
    def zoom_to_decoded(self):
        """Zoom to decoded location"""
        if not hasattr(self, 'last_decoded_result'):
            QMessageBox.information(self, 'Info', 'Please decode a DIGIPIN first')
            return
        
        result = self.last_decoded_result
        bounds = result['bounds']
        
        from qgis.core import QgsRectangle
        rect = QgsRectangle(
            bounds['minLon'], bounds['minLat'],
            bounds['maxLon'], bounds['maxLat']
        )
        
        self.iface.mapCanvas().setExtent(rect)
        self.iface.mapCanvas().refresh()
        
        self.status_label.setText('Zoomed to DIGIPIN location')
    
    def refresh_layers(self):
        """Refresh the layer combo box with point layers"""
        self.layer_combo.clear()
        
        layers = QgsProject.instance().mapLayers().values()
        point_layers = [layer for layer in layers 
                       if isinstance(layer, QgsVectorLayer) 
                       and layer.geometryType() == QgsWkbTypes.PointGeometry]
        
        for layer in point_layers:
            self.layer_combo.addItem(layer.name(), layer)
    
    def batch_encode_layer(self):
        """Batch encode all points in selected layer"""
        if self.layer_combo.count() == 0:
            QMessageBox.warning(self, 'Warning', 'No point layers available')
            return
        
        layer = self.layer_combo.currentData()
        if not layer:
            QMessageBox.warning(self, 'Warning', 'Please select a layer')
            return
        
        precision = self.batch_precision.value()
        field_name = self.output_field_name.text().strip()
        
        if not field_name:
            QMessageBox.warning(self, 'Warning', 'Please enter a field name')
            return
        
        try:
            # Add DIGIPIN field if it doesn't exist
            if layer.fields().indexOf(field_name) == -1:
                layer.dataProvider().addAttributes([QgsField(field_name, QVariant.String)])
                layer.updateFields()
            
            field_idx = layer.fields().indexOf(field_name)
            
            # Start editing
            layer.startEditing()
            
            # Show progress
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(layer.featureCount())
            
            success_count = 0
            error_count = 0
            
            # Process features
            for i, feature in enumerate(layer.getFeatures()):
                geom = feature.geometry()
                if geom and not geom.isNull():
                    point = geom.asPoint()
                    try:
                        digipin = DigipinEncoder.encode(point.y(), point.x(), precision)
                        layer.changeAttributeValue(feature.id(), field_idx, digipin)
                        success_count += 1
                    except ValueError:
                        error_count += 1
                
                self.progress_bar.setValue(i + 1)
            
            # Commit changes
            layer.commitChanges()
            
            # Hide progress
            self.progress_bar.setVisible(False)
            
            # Show results
            result_text = f'''
<b>Batch Encoding Complete</b><br>
<br>
Layer: {layer.name()}<br>
Field: {field_name}<br>
Precision: Level {precision}<br>
<br>
Successfully encoded: {success_count}<br>
Errors: {error_count}<br>
            '''
            
            self.batch_result.setHtml(result_text)
            self.status_label.setText(f'Batch encoding complete: {success_count} features processed')
            
            QMessageBox.information(
                self, 
                'Success', 
                f'Successfully encoded {success_count} features.\nErrors: {error_count}'
            )
            
        except Exception as e:
            layer.rollBack()
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, 'Error', f'Batch encoding failed: {str(e)}')
    
    def toggle_batch_source(self):
        """Toggle between layer and file input for batch processing"""
        is_file = self.batch_file_radio.isChecked()
        self.layer_group.setVisible(not is_file)
        self.file_group.setVisible(is_file)
    
    def browse_input_file(self):
        """Browse for input CSV or GeoJSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select Input File',
            '',
            'Supported Files (*.csv *.geojson *.json);;CSV Files (*.csv);;GeoJSON Files (*.geojson *.json);;All Files (*.*)'
        )
        
        if file_path:
            self.file_path_input.setText(file_path)
            
            # If CSV, try to detect lat/lon columns
            if file_path.lower().endswith('.csv'):
                self.detect_csv_columns(file_path)
    
    def detect_csv_columns(self, file_path):
        """Detect and populate latitude/longitude columns from CSV"""
        try:
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                self.csv_lat_combo.clear()
                self.csv_lon_combo.clear()
                
                for header in headers:
                    self.csv_lat_combo.addItem(header)
                    self.csv_lon_combo.addItem(header)
                
                # Try to auto-select common column names
                lat_keywords = ['lat', 'latitude', 'y']
                lon_keywords = ['lon', 'long', 'longitude', 'x']
                
                for i, header in enumerate(headers):
                    header_lower = header.lower()
                    if any(kw in header_lower for kw in lat_keywords):
                        self.csv_lat_combo.setCurrentIndex(i)
                    if any(kw in header_lower for kw in lon_keywords):
                        self.csv_lon_combo.setCurrentIndex(i)
                        
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'Could not read CSV headers: {str(e)}')
    
    def batch_process(self):
        """Main batch processing function"""
        if self.batch_layer_radio.isChecked():
            self.batch_encode_layer()
        else:
            self.batch_encode_file()
    
    def batch_encode_file(self):
        """Batch encode from CSV or GeoJSON file"""
        file_path = self.file_path_input.text()
        
        if not file_path:
            QMessageBox.warning(self, 'Warning', 'Please select an input file')
            return
        
        precision = self.batch_precision.value()
        field_name = self.output_field_name.text().strip()
        
        if not field_name:
            QMessageBox.warning(self, 'Warning', 'Please enter a field name')
            return
        
        try:
            if file_path.lower().endswith('.csv'):
                self.process_csv_file(file_path, precision, field_name)
            elif file_path.lower().endswith(('.geojson', '.json')):
                self.process_geojson_file(file_path, precision, field_name)
            else:
                QMessageBox.warning(self, 'Warning', 'Unsupported file format')
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'File processing failed: {str(e)}')
    
    def process_csv_file(self, file_path, precision, field_name):
        """Process CSV file and encode to DIGIPIN"""
        import csv
        import os
        
        lat_field = self.csv_lat_combo.currentText()
        lon_field = self.csv_lon_combo.currentText()
        
        if not lat_field or not lon_field:
            QMessageBox.warning(self, 'Warning', 'Please select latitude and longitude fields')
            return
        
        # Read CSV
        rows = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            # Add DIGIPIN field if not exists
            if field_name not in headers:
                headers = list(headers) + [field_name]
            
            self.progress_bar.setVisible(True)
            success_count = 0
            error_count = 0
            
            for row in reader:
                try:
                    lat = float(row[lat_field])
                    lon = float(row[lon_field])
                    digipin = DigipinEncoder.encode(lat, lon, precision)
                    row[field_name] = digipin
                    success_count += 1
                except (ValueError, KeyError):
                    row[field_name] = ''
                    error_count += 1
                
                rows.append(row)
        
        # Save output
        if self.save_to_file_check.isChecked():
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save Output CSV',
                os.path.splitext(file_path)[0] + '_digipin.csv',
                'CSV Files (*.csv)'
            )
            
            if output_path:
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(rows)
                
                self.status_label.setText(f'Saved to: {output_path}')
        
        # Create layer if requested
        if self.create_new_layer_check.isChecked():
            self.create_layer_from_csv_data(rows, lat_field, lon_field, field_name, 'CSV_DIGIPIN_Layer')
        
        self.progress_bar.setVisible(False)
        
        # Show results
        result_text = f'''
<b>CSV Processing Complete</b><br>
<br>
File: {os.path.basename(file_path)}<br>
Field: {field_name}<br>
Precision: Level {precision}<br>
<br>
Successfully encoded: {success_count}<br>
Errors: {error_count}<br>
        '''
        
        self.batch_result.setHtml(result_text)
        QMessageBox.information(self, 'Success', f'Processed {success_count} records.\nErrors: {error_count}')
    
    def process_geojson_file(self, file_path, precision, field_name):
        """Process GeoJSON file and encode to DIGIPIN"""
        import json
        import os
        
        # Read GeoJSON
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        if 'features' not in geojson_data:
            QMessageBox.warning(self, 'Warning', 'Invalid GeoJSON format')
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(geojson_data['features']))
        
        success_count = 0
        error_count = 0
        
        for i, feature in enumerate(geojson_data['features']):
            try:
                geom = feature['geometry']
                if geom['type'] == 'Point':
                    lon, lat = geom['coordinates']
                    digipin = DigipinEncoder.encode(lat, lon, precision)
                    
                    if 'properties' not in feature:
                        feature['properties'] = {}
                    feature['properties'][field_name] = digipin
                    success_count += 1
                else:
                    error_count += 1
            except (ValueError, KeyError, TypeError):
                error_count += 1
            
            self.progress_bar.setValue(i + 1)
        
        # Save output
        if self.save_to_file_check.isChecked():
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save Output GeoJSON',
                os.path.splitext(file_path)[0] + '_digipin.geojson',
                'GeoJSON Files (*.geojson *.json)'
            )
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(geojson_data, f, indent=2)
                
                self.status_label.setText(f'Saved to: {output_path}')
        
        # Create layer if requested
        if self.create_new_layer_check.isChecked():
            self.create_layer_from_geojson(geojson_data, 'GeoJSON_DIGIPIN_Layer')
        
        self.progress_bar.setVisible(False)
        
        # Show results
        result_text = f'''
<b>GeoJSON Processing Complete</b><br>
<br>
File: {os.path.basename(file_path)}<br>
Field: {field_name}<br>
Precision: Level {precision}<br>
<br>
Successfully encoded: {success_count}<br>
Errors: {error_count}<br>
        '''
        
        self.batch_result.setHtml(result_text)
        QMessageBox.information(self, 'Success', f'Processed {success_count} features.\nErrors: {error_count}')
    
    def create_layer_from_csv_data(self, rows, lat_field, lon_field, digipin_field, layer_name):
        """Create a point layer from CSV data"""
        layer = QgsVectorLayer('Point?crs=EPSG:4326', layer_name, 'memory')
        provider = layer.dataProvider()
        
        # Add fields from CSV
        if rows:
            fields = []
            for key in rows[0].keys():
                fields.append(QgsField(key, QVariant.String))
            provider.addAttributes(fields)
            layer.updateFields()
            
            # Add features
            for row in rows:
                try:
                    lat = float(row[lat_field])
                    lon = float(row[lon_field])
                    
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
                    feature.setAttributes(list(row.values()))
                    provider.addFeature(feature)
                except (ValueError, KeyError):
                    pass
            
            layer.updateExtents()
            QgsProject.instance().addMapLayer(layer)
            self.status_label.setText(f'Created layer: {layer_name}')
    
    def create_layer_from_geojson(self, geojson_data, layer_name):
        """Create a layer from GeoJSON data"""
        import tempfile
        import json
        import os
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False, encoding='utf-8')
        json.dump(geojson_data, temp_file)
        temp_file.close()
        
        # Load as layer
        layer = QgsVectorLayer(temp_file.name, layer_name, 'ogr')
        
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            self.status_label.setText(f'Created layer: {layer_name}')
        
        # Clean up temp file
        try:
            os.unlink(temp_file.name)
        except:
            pass
    
    # Grid Visualization Methods
    
    def toggle_grid_extent_options(self):
        """Toggle grid extent options based on selection"""
        extent_type = self.grid_extent_combo.currentText()
        self.grid_layer_combo.setVisible(extent_type == 'Layer Extent')
        
        if extent_type == 'Layer Extent':
            # Populate with all layers
            self.grid_layer_combo.clear()
            layers = QgsProject.instance().mapLayers().values()
            for layer in layers:
                if isinstance(layer, QgsVectorLayer):
                    self.grid_layer_combo.addItem(layer.name(), layer)
    
    def update_grid_warning(self):
        """Update warning label based on precision level"""
        precision = self.grid_precision.value()
        
        if precision >= 9:
            self.grid_warning_label.setText('⚠️ Very High! May be slow')
        elif precision >= 7:
            self.grid_warning_label.setText('⚠️ High precision - processing may take time')
        else:
            self.grid_warning_label.setText('')
    
    def generate_grid(self):
        """Generate DIGIPIN grid"""
        from qgis.core import QgsRectangle
        from ..core.grid_utils import OptimizedGridGenerator
        
        precision = self.grid_precision.value()
        extent_type = self.grid_extent_combo.currentText()
        
        # Get extent
        if extent_type == 'Current Map Extent':
            extent = self.iface.mapCanvas().extent()
        elif extent_type == 'Layer Extent':
            layer = self.grid_layer_combo.currentData()
            if not layer:
                QMessageBox.warning(self, 'Warning', 'Please select a layer')
                return
            extent = layer.extent()
        else:
            # Custom extent - for now use map extent
            extent = self.iface.mapCanvas().extent()
        
        # Estimate cell count
        estimated_cells = OptimizedGridGenerator.estimate_cell_count(extent, precision)
        
        # Warn if too many cells
        if estimated_cells > 50000:
            reply = QMessageBox.question(
                self,
                'Large Grid Warning',
                f'Estimated {estimated_cells:,} cells. This may take a long time and use significant memory.\n\nContinue anyway?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText('Generating grid...')
            
            # Progress callback
            def update_progress(value):
                self.progress_bar.setValue(value)
                from qgis.PyQt.QtWidgets import QApplication
                QApplication.processEvents()
            
            # Generate grid
            max_cells = 50000 if precision >= 8 else 100000
            layer = OptimizedGridGenerator.generate_grid_chunked(
                extent,
                precision,
                progress_callback=update_progress,
                max_cells=max_cells
            )
            
            # Apply styling
            style_type = self.grid_style_combo.currentText()
            self.apply_grid_style(layer, style_type, precision)
            
            # Add to project
            QgsProject.instance().addMapLayer(layer)
            
            self.progress_bar.setVisible(False)
            
            # Show results
            cell_count = layer.featureCount()
            result_text = f'''
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Grid Generated Successfully</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📊 Grid Statistics:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Precision Level: <b>{precision}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Total Cells: <b>{cell_count:,}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Style: <b>{style_type}</b></p>
</div>
            '''
            
            self.grid_result.setHtml(result_text)
            self.status_label.setText(f'✓ Grid generated: {cell_count:,} cells')
            
            QMessageBox.information(self, 'Success', f'Grid generated with {cell_count:,} cells')
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, 'Error', f'Grid generation failed: {str(e)}')
    
    def apply_grid_style(self, layer, style_type, precision):
        """Apply styling to grid layer"""
        from qgis.core import (
            QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer,
            QgsGraduatedSymbolRenderer, QgsRendererRange,
            QgsFillSymbol, QgsSimpleFillSymbolLayer
        )
        from qgis.PyQt.QtGui import QColor
        
        if style_type == 'Simple':
            # Simple outline style
            symbol = QgsFillSymbol.createSimple({
                'color': '255,255,255,50',
                'outline_color': '#0066cc',
                'outline_width': '0.5'
            })
            from qgis.core import QgsSingleSymbolRenderer
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
            
        elif style_type == 'Colored by Precision':
            # Color based on precision level
            colors = ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15']
            color_idx = min(precision - 1, len(colors) - 1)
            symbol = QgsFillSymbol.createSimple({
                'color': colors[color_idx] + ',100',
                'outline_color': '#333333',
                'outline_width': '0.3'
            })
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
        
        layer.triggerRepaint()
    
    # Spatial Analysis Methods
    
    def refresh_analysis_layers(self):
        """Refresh layers for spatial analysis"""
        self.analysis_layer_combo.clear()
        
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                self.analysis_layer_combo.addItem(layer.name(), layer)
        
        # Update field combo when layer changes
        self.analysis_layer_combo.currentIndexChanged.connect(self.update_analysis_fields)
        self.update_analysis_fields()
    
    def update_analysis_fields(self):
        """Update DIGIPIN field combo based on selected layer"""
        self.analysis_digipin_field.clear()
        
        layer = self.analysis_layer_combo.currentData()
        if layer:
            for field in layer.fields():
                self.analysis_digipin_field.addItem(field.name())
    
    def run_spatial_analysis(self):
        """Run selected spatial analysis"""
        from ..core.analysis_utils import DigipinSpatialAnalysis
        
        layer = self.analysis_layer_combo.currentData()
        if not layer:
            QMessageBox.warning(self, 'Warning', 'Please select a layer')
            return
        
        digipin_field = self.analysis_digipin_field.currentText()
        if not digipin_field:
            QMessageBox.warning(self, 'Warning', 'Please select a DIGIPIN field')
            return
        
        try:
            self.progress_bar.setVisible(True)
            self.status_label.setText('Running analysis...')
            
            if self.analysis_density_radio.isChecked():
                self.run_density_analysis(layer, digipin_field)
            elif self.analysis_coverage_radio.isChecked():
                self.run_coverage_analysis(layer, digipin_field)
            elif self.analysis_neighbors_radio.isChecked():
                self.run_neighbor_analysis(layer, digipin_field)
            elif self.analysis_distance_radio.isChecked():
                self.run_distance_analysis(layer, digipin_field)
            
            self.progress_bar.setVisible(False)
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, 'Error', f'Analysis failed: {str(e)}')
    
    def run_density_analysis(self, layer, digipin_field):
        """Run point density analysis"""
        from ..core.analysis_utils import DigipinSpatialAnalysis
        
        precision = self.analysis_precision.value()
        
        # Calculate density
        density_map = DigipinSpatialAnalysis.calculate_density(layer, digipin_field, precision)
        
        if not density_map:
            QMessageBox.warning(self, 'Warning', 'No valid DIGIPIN data found')
            return
        
        # Create density layer
        density_layer = DigipinSpatialAnalysis.create_density_layer(density_map, f'Density_L{precision}')
        QgsProject.instance().addMapLayer(density_layer)
        
        # Show results
        total_cells = len(density_map)
        total_points = sum(density_map.values())
        avg_density = total_points / total_cells if total_cells > 0 else 0
        max_density = max(density_map.values()) if density_map else 0
        
        result_text = f'''
<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Density Analysis Complete</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📊 Statistics:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Total Cells: <b>{total_cells:,}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Total Points: <b>{total_points:,}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Average Density: <b>{avg_density:.2f}</b> points/cell</p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Maximum Density: <b>{max_density}</b> points/cell</p>
</div>
        '''
        
        self.analysis_result.setHtml(result_text)
        self.status_label.setText(f'✓ Density analysis complete: {total_cells:,} cells analyzed')
        
        QMessageBox.information(self, 'Success', f'Density layer created with {total_cells:,} cells')
    
    def run_coverage_analysis(self, layer, digipin_field):
        """Run coverage analysis"""
        from ..core.analysis_utils import DigipinSpatialAnalysis
        
        stats = DigipinSpatialAnalysis.calculate_coverage(layer, digipin_field)
        
        if not stats:
            QMessageBox.warning(self, 'Warning', 'No valid DIGIPIN data found')
            return
        
        # Format precision distribution
        precision_dist = stats.get('precision_distribution', {})
        dist_html = '<br>'.join([f'Level {p}: {c:,} features' for p, c in sorted(precision_dist.items())])
        
        result_text = f'''
<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Coverage Analysis Complete</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📊 Coverage Statistics:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Unique Cells: <b>{stats.get('unique_cells', 0):,}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Total Features: <b>{stats.get('total_features', 0):,}</b></p>
</div>

<div style="background: #fff3cd; padding: 12px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 0 0 8px 0; color: #856404; font-weight: bold;">Precision Distribution:</p>
    <p style="margin: 3px 0; color: #856404; font-size: 13px;">{dist_html}</p>
</div>
        '''
        
        self.analysis_result.setHtml(result_text)
        self.status_label.setText(f'✓ Coverage analysis complete')
        
        QMessageBox.information(self, 'Success', f'Coverage analysis complete: {stats.get("unique_cells", 0):,} unique cells')
    
    def run_neighbor_analysis(self, layer, digipin_field):
        """Run neighbor analysis"""
        from ..core.analysis_utils import DigipinSpatialAnalysis
        
        include_diagonals = self.analysis_include_diagonals.isChecked()
        
        # Get unique DIGIPINs
        field_idx = layer.fields().indexOf(digipin_field)
        if field_idx == -1:
            QMessageBox.warning(self, 'Warning', 'DIGIPIN field not found')
            return
        
        unique_digipins = set()
        for feature in layer.getFeatures():
            digipin = feature.attribute(digipin_field)
            if digipin:
                unique_digipins.add(digipin.replace('-', ''))
        
        # Analyze first few DIGIPINs (to prevent long processing)
        sample_size = min(10, len(unique_digipins))
        sample_digipins = list(unique_digipins)[:sample_size]
        
        neighbor_counts = []
        for digipin in sample_digipins:
            neighbors = DigipinSpatialAnalysis.find_neighbors(digipin, include_diagonals)
            neighbor_counts.append(len(neighbors))
        
        avg_neighbors = sum(neighbor_counts) / len(neighbor_counts) if neighbor_counts else 0
        
        result_text = f'''
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Neighbor Analysis Complete</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📊 Neighbor Statistics:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Analyzed Cells: <b>{sample_size}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Average Neighbors: <b>{avg_neighbors:.1f}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Include Diagonals: <b>{'Yes' if include_diagonals else 'No'}</b></p>
</div>
        '''
        
        self.analysis_result.setHtml(result_text)
        self.status_label.setText(f'✓ Neighbor analysis complete')
        
        QMessageBox.information(self, 'Success', f'Analyzed {sample_size} cells')
    
    def run_distance_analysis(self, layer, digipin_field):
        """Run distance matrix analysis"""
        from ..core.analysis_utils import DigipinSpatialAnalysis
        
        # Calculate distance matrix (limited to first 50 features)
        matrix = DigipinSpatialAnalysis.calculate_distance_matrix(layer, digipin_field, max_features=50)
        
        if not matrix:
            QMessageBox.warning(self, 'Warning', 'No valid DIGIPIN data found')
            return
        
        # Calculate statistics
        all_distances = []
        for digipin1, distances in matrix.items():
            all_distances.extend(distances.values())
        
        if all_distances:
            avg_distance = sum(all_distances) / len(all_distances)
            min_distance = min(all_distances)
            max_distance = max(all_distances)
        else:
            avg_distance = min_distance = max_distance = 0
        
        result_text = f'''
<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px; color: white;">
    <h3 style="margin: 0 0 10px 0; color: #fff;">✓ Distance Analysis Complete</h3>
</div>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <p style="margin: 5px 0; color: #495057;"><b>📊 Distance Statistics:</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Analyzed Points: <b>{len(matrix)}</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Average Distance: <b>{avg_distance:.2f} km</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Minimum Distance: <b>{min_distance:.2f} km</b></p>
    <p style="margin: 5px 0 5px 20px; color: #6c757d;">Maximum Distance: <b>{max_distance:.2f} km</b></p>
</div>
        '''
        
        self.analysis_result.setHtml(result_text)
        self.status_label.setText(f'✓ Distance analysis complete')
        
        QMessageBox.information(self, 'Success', f'Distance matrix calculated for {len(matrix)} points')


