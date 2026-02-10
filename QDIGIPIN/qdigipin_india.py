"""
Main QGIS Plugin Class
"""

import os
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import QgsApplication

from .gui.main_dialog import QDigipinMainDialog
from .processing.provider import DigipinProvider


class QDigipinIndia:
    """QGIS Plugin Implementation for DIGIPIN India"""

    def __init__(self, iface):
        """Constructor
        
        Args:
            iface: QGIS interface instance
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        
        # Initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'locale',
            f'qdigipin_{locale}.qm'
        )
        
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&Q-DIGIPIN India')
        self.toolbar = self.iface.addToolBar('Q-DIGIPIN India')
        self.toolbar.setObjectName('QDigipinIndiaToolbar')
        
        # Processing provider
        self.provider = None
        
        # Main dialog
        self.main_dialog = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API"""
        return QCoreApplication.translate('QDigipinIndia', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Add a toolbar icon to the toolbar"""
        
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        
        if status_tip is not None:
            action.setStatusTip(status_tip)
        
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        
        if add_to_toolbar:
            self.toolbar.addAction(action)
        
        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action
            )
        
        self.actions.append(action)
        
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI"""
        
        icon_path = os.path.join(self.plugin_dir, 'resources', 'icons', 'plugin_icon.png')
        
        # Main dialog action
        self.add_action(
            icon_path,
            text=self.tr('Open DIGIPIN Tools'),
            callback=self.show_main_dialog,
            parent=self.iface.mainWindow(),
            status_tip=self.tr('Open Q-DIGIPIN India Tools'),
            add_to_toolbar=True
        )
        
        # Initialize processing provider
        self.initProcessing()

    def initProcessing(self):
        """Initialize Processing provider"""
        self.provider = DigipinProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI"""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr('&Q-DIGIPIN India'),
                action
            )
            self.iface.removeToolBarIcon(action)
        
        # Remove the toolbar
        del self.toolbar
        
        # Remove processing provider
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

    def show_main_dialog(self):
        """Show the main plugin dialog"""
        if self.main_dialog is None:
            self.main_dialog = QDigipinMainDialog(self.iface, self.plugin_dir)
        
        self.main_dialog.show()
        self.main_dialog.raise_()
        self.main_dialog.activateWindow()
