import os
import sys

from eso_addon_manager import constants
from eso_addon_manager.logs import init_gui_logger

os.environ['QT_API'] = 'pyqt5'
import qdarkstyle
from qtpy import QtWidgets, QtCore, QtGui


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
        self.layout().addWidget(AddOnManagerWidget(self))
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
        # self.layout().setMargin(0)
        self.layout().addRow('ESO UI API version', self.api_version_edit())
        self.layout().addRow('ESO AddOns Directory', self.addons_directory_edit())
        self.layout().addRow('Rollback downloads on error?', self.rollback_checkbox())
        self.layout().addRow('Prompt to install?', self.prompt_checkbox())

    def init_controller(self):
        pass

    def api_version_edit(self):
        if not hasattr(self, '_api_version_edit'):
            self._api_version_edit = QtWidgets.QLineEdit(self)
            self._api_version_edit.setValidator(QtGui.QIntValidator())
        return self._api_version_edit

    def rollback_checkbox(self):
        if not hasattr(self, '_rollback_checkbox'):
            self._rollback_checkbox = QtWidgets.QCheckBox(self)
        return self._rollback_checkbox

    def prompt_checkbox(self):
        if not hasattr(self, '_prompt_checkbox'):
            self._prompt_checkbox = QtWidgets.QCheckBox(self)
        return self._prompt_checkbox

    def addons_directory_edit(self):
        if not hasattr(self, '_addons_directory_edit'):
            self._addons_directory_edit = FileSelect(self)
        return self._addons_directory_edit


class FileSelect(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.start_dir = constants.HOMEDIR
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.file_edit())
        self.layout().addWidget(self.browse_button())

    def init_controller(self):
        self.browse_button().clicked.connect(self.on_browse_clicked)

    def file_edit(self):
        if not hasattr(self, '_file_edit'):
            self._file_edit = QtWidgets.QLineEdit(self)
        return self._file_edit

    def browse_button(self):
        if not hasattr(self, '_browse_button'):
            self._browse_button = QtWidgets.QPushButton(self)
            self._browse_button.setText('...')
        return self._browse_button

    @property
    def selected_file(self):
        return str(self.file_edit.text())

    def on_browse_clicked(self):
        selected_file = QtWidgets.QDialog.getOpenFileName(
            self,
            'Open File',
            self.start_dir,
            'All Files (*.*)'
        )

        if not selected_file:
            return None

        selected_file = str(selected_file)
        self.file_edit().setText(selected_file)


class AddOnManagerWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.addon_tree())
        self.layout().addWidget(self.addon_controls())

    def init_controller(self):
        pass

    def addon_tree(self):
        if not hasattr(self, '_addon_tree'):
            self._addon_tree = QtWidgets.QTreeView(self)
        return self._addon_tree

    def addon_controls(self):
        if not hasattr(self, '_addon_controls'):
            self._addon_controls = AddOnControlsWidget(self)
        return self._addon_controls


class AddOnControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addStretch(1)
        self.layout().addWidget(self.eso_ui_addon_button())
        self.layout().addWidget(self.run_update_button())
        self.layout().addStretch(1)

    def init_controller(self):
        self.eso_ui_addon_button().clicked.connect(
            self.on_eso_ui_addon_button_clicked
        )
        self.run_update_button().clicked.connect(
            self.on_run_update_button_clicked
        )

    def on_eso_ui_addon_button_clicked(self):
        result = ESOUIAddOnDialog.exec_dialog(self)
        
        if result is None:
            return

        print(result)

    def on_run_update_button_clicked(self):
        RunUpdateDialog.exec_dialog(self)

    def eso_ui_addon_button(self):
        if not hasattr(self, '_eso_ui_addon_button'):
            self._eso_ui_addon_button = QtWidgets.QPushButton(self)
            self._eso_ui_addon_button.setText('ESO UI')
        return self._eso_ui_addon_button

    def run_update_button(self):
        if not hasattr(self, '_run_update_button'):
            self._run_update_button = QtWidgets.QPushButton(self)
            self._run_update_button.setText('Run update!')
        return self._run_update_button


class ESOUIAddOnDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()
        self.result = None

    def init_ui(self):
        self.setWindowTitle('AddOn from ESO UI')
        self.setGeometry(200, 200, 500, 500)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addLayout(self.form_layout())
        self.form_layout().addRow('Reference Link', self.reference_link_edit())
        self.form_layout().addRow('Download Link', self.download_link_edit())
        self.form_layout().addRow('Dependency Download Links', self.dependencies_list_widget())
        self.layout().addLayout(self.control_layout())
        self.control_layout().addStretch(1)
        self.control_layout().addWidget(self.accept_button())
        self.control_layout().addWidget(self.cancel_button())
        self.control_layout().addStretch(1)

    def init_controller(self):
        self.accept_button().clicked.connect(
            self.on_accept_button_clicked
        )
        self.cancel_button().clicked.connect(
            lambda: self.done(0)
        )
        self._dependency_link_add_button.clicked.connect(
            self.on_dependency_link_add_button_clicked
        )
        self._dependency_link_delete_button.clicked.connect(
            self.on_dependency_link_delete_button_clicked
        )

    def on_dependency_link_delete_button_clicked(self):
        for item in self._dependencies_list.selectedItems():
            self._dependencies_list.takeItem(
                self._dependencies_list.row(item)
            )

    def on_dependency_link_add_button_clicked(self):
        self._dependencies_list.addItem(
            QtWidgets.QListWidgetItem(
                self.add_dependency_link_text()
            )
        )

    def on_accept_button_clicked(self):
        self.result = {
            'ref_link': self.reference_link(),
            'link': self.download_link(),
            'dependencies': self.dependencies()
        }
        self.done(0)

    def form_layout(self):
        if not hasattr(self, '_form_layout'):
            self._form_layout = QtWidgets.QFormLayout()
        return self._form_layout

    def control_layout(self):
        if not hasattr(self, '_control_layout'):
            self._control_layout = QtWidgets.QHBoxLayout()
        return self._control_layout

    def accept_button(self):
        if not hasattr(self, '_accept_button'):
            self._accept_button = QtWidgets.QPushButton(self)
            self._accept_button.setText('Accept')
        return self._accept_button

    def cancel_button(self):
        if not hasattr(self, '_cancel_button'):
            self._cancel_button = QtWidgets.QPushButton(self)
            self._cancel_button.setText('Cancel')
        return self._cancel_button

    def reference_link_edit(self):
        if not hasattr(self, '_reference_link_edit'):
            self._reference_link_edit = QtWidgets.QLineEdit(self)
        return self._reference_link_edit

    def reference_link(self):
        return str(self.reference_link_edit().text())

    def download_link_edit(self):
        if not hasattr(self, '_download_link_edit'):
            self._download_link_edit = QtWidgets.QLineEdit(self)
        return self._download_link_edit

    def download_link(self):
        return str(self.download_link_edit().text())

    def dependencies_list_widget(self):
        if not hasattr(self, '_dependencies_list_widget'):
            # Things stack from the top
            self._dependencies_widget = QtWidgets.QWidget(self)
            self._dependencies_widget.setLayout(QtWidgets.QVBoxLayout())
            #

            # Except for here, we venture sideways.
            self._dependencies_control_layout = QtWidgets.QHBoxLayout()
            self._dependencies_widget.layout().addLayout(self._dependencies_control_layout)
            self._dependency_link_edit = QtWidgets.QLineEdit()
            self._dependencies_control_layout.addWidget(self._dependency_link_edit)
            self._dependency_link_add_button = QtWidgets.QPushButton()
            self._dependency_link_add_button.setText('Add')
            self._dependencies_control_layout.addWidget(self._dependency_link_add_button)
            self._dependency_link_delete_button = QtWidgets.QPushButton()
            self._dependency_link_delete_button.setText('Delete')
            self._dependencies_control_layout.addWidget(self._dependency_link_delete_button)
            #

            # And now we return to the vertical
            self._dependencies_list = QtWidgets.QListWidget()
            self._dependencies_widget.layout().addWidget(self._dependencies_list)
            #

        return self._dependencies_widget

    def add_dependency_link_text(self):
        return str(self._dependency_link_edit.text())

    def dependencies(self):
        dependencies = []
        for idx in range(self._dependencies_list.count()):
            item = self.dependencies_list.item(idx)
            dependencies.append(str(item.text()))
        return dependencies

    @classmethod
    def exec_dialog(cls, parent):
        inst = cls(parent)
        inst.exec_()
        return inst.result


class RunUpdateDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        self.setWindowTitle('Running Update')
        self.setGeometry(200, 200, 500, 500)
        self.setLayout(QtWidgets.QVBoxLayout())

    def init_controller(self):
        pass

    def run_text_area(self):
        if not hasattr(self, '_run_text_area'):
            self._run_text_area = QtWidgets.QTextArea(self)
        return self._run_text_area

    @classmethod
    def exec_dialog(cls, parent):
        inst = cls(parent)
        inst.exec_()


if __name__ == '__main__':
    run_gui()