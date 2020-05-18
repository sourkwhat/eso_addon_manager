import os
import sys

from eso_addon_manager import constants
from eso_addon_manager.logs import init_gui_logger

os.environ['QT_API'] = 'pyqt5'
import qdarkstyle
from qtpy import QtWidgets, QtCore


def run_gui():
    init_gui_logger()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = QtWidgets.QMainWindow()
    window.setWindowTitle(constants.MAIN_WINDOW_TITLE)
    window.setFixedSize(
        constants.MAIN_WINDOW_WIDTH,
        constants.MAIN_WINDOW_HEIGHT
    )
    window.setCentralWidget(ESOAddonManagerUI(window))

    window.show()
    app.exec_()


class ESOAddonManagerUI(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(MetaConfigWidget(self))
        self.layout().addWidget(ConfigWidget(self))
        self.layout().addStretch(1)

    def init_controller(self):
        pass


class MetaConfigWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    @property
    def profile_combo(self):
        if not hasattr(self, '_profile_combobox'):
            self._profile_combobox = QtWidgets.QComboBox(self)
        return self._profile_combobox

    def init_ui(self):
        self.setTitle('AddOn Profiles')
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.profile_combo)

    def init_controller(self):
        self.profile_combo.addItem('Default')


class ConfigWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setTitle('Configuration')
        self.setLayout(QtWidgets.QFormLayout())
        self.layout().addRow('Hello', self.api_version_edit)

    def init_controller(self):
        pass

    @property
    def api_version_edit(self):
        if not hasattr(self, '_api_version_edit'):
            self._api_version_edit = QtWidgets.QLineEdit(self)
        return self._api_version_edit


if __name__ == '__main__':
    run_gui()