import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from model.model import Model
from model.file_table_model import fileTableModel
from views.main_view import MainView
from controllers.main_ctrl import ImageDisplayController
from controllers.image_manager_ctrl import ImageManagerController

class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.model = Model()
        self.file_table_model = fileTableModel(data=[], header=["File path", "Has segmentation mask?", "Segmentation mask path"])

        self.main_controller = ImageDisplayController(self.model)

        self.image_manager_controller = ImageManagerController(self.file_table_model)
        
        self.main_view = MainView(self.model, self.file_table_model, self.main_controller, self.image_manager_controller)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())