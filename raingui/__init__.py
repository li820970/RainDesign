import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import os
import rainparsing
import widget_generators
import utils
import subprocess

def open_selected_obj(selected_obj):

    if str(selected_obj).endswith('.ini') or str(selected_obj).endswith('.inc'):
        return RainmeterFileWindow(selected_obj)
    else:
        cmd = 'explorer "' + selected_obj.path + '"'
        cmd = cmd.replace('/', '\\')
        print(cmd)
        subprocess.Popen(cmd)
        return None


class CollectionWindow(QMainWindow ):
    def __init__(self, path=None):
        QWidget.__init__(self)
        self.tree_widget = None

        if path is None:
            self.collection_folder = None
        else:
            self.collection_folder = rainparsing.CollectionFolder(path=path)
            self.update_tree()
        self.child_windows = []
        self.resize(480, 360)
        self.move(300, 300)
        self.setWindowTitle('RainDesign')
        self.init_menubar()
        self.show()
    def init_menubar(self):
        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu('File')

        self.menu_open_folder = QAction("Open Collection Folder", self)
        self.menu_open_folder.setShortcut("Ctrl+O")
        self.menu_open_folder.setStatusTip('Open a skin collection folder for parsing')
        self.menu_open_folder.triggered.connect(self.open_folder)

        self.menu_exit = QAction('Exit', self)
        self.menu_exit.setShortcut('Ctrl+Q')
        self.menu_exit.setStatusTip('Exit the program')
        self.menu_exit.triggered.connect(self.close)

        self.fileMenu.addAction(self.menu_open_folder)
        self.fileMenu.addAction(self.menu_exit)

    def open_folder(self):
        docs = os.path.expanduser('~') + '\\Documents\\Rainmeter\\Skins'
        print(docs)
        dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', docs, QFileDialog.ShowDirsOnly)
        if dir_ is None:
            return
        print('scanning ' + dir_)
        self.collection_folder = rainparsing.CollectionFolder(dir_)
        self.update_tree()
        return

    def update_tree(self):
        if self.collection_folder is not None:
            self.setWindowTitle(str(self.collection_folder))
            self.tree_widget = widget_generators.create_collection_tree_widget(self.collection_folder)
            self.tree_widget.itemDoubleClicked.connect(self.double_click_on_tree)
            self.setCentralWidget(self.tree_widget)

    def double_click_on_tree(self, clicked_item, column):
        """

        :type column: int
        :type clicked_item: QTreeWidgetItem
        """
        path = utils.path_from_widgetitem(clicked_item)
        selected_obj = clicked_item.model

        new_window = open_selected_obj(selected_obj)
        if new_window is not None:
            self.new_child_window(new_window)

    def new_child_window(self, window):
        self.child_windows.append(window)
        self.child_windows[-1].show()

class RainmeterFileWindow(QMainWindow):
    def __init__(self, file_obj, start_hidden = False):
        """

        :type file_obj: rainparsing.SkinFile
        """
        QWidget.__init__(self)
        self.file = file_obj
        self.resize(360, 480)
        self.move(300, 300)
        self.setWindowTitle(file_obj.name)
        self.init_menubar()
        self.child_windows = []
        self.widget_generator = widget_generators.create_file_tree_widget
        self.update_tree()
        if not start_hidden:
            self.show()

    def init_menubar(self):
        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu('File')
        self.viewMenu = mainMenu.addMenu('View')

        self.menu_save = QAction("Save", self)
        self.menu_save.setShortcut("Ctrl+S")

        self.menu_view_env = QAction("View Local Environment", self)
        self.menu_view_env.triggered.connect(self.open_env)

        self.menu_view_sortby = QMenu('Sort By', self)

        self.menu_view_sortbysection = QAction('Section', self)
        self.menu_view_sortbysection.triggered.connect(self.to_section_view)
        self.menu_view_sortby.addAction(self.menu_view_sortbysection)

        self.menu_view_sortbygroup = QAction('Group', self)
        self.menu_view_sortbygroup.triggered.connect(self.to_group_view)
        self.menu_view_sortby.addAction(self.menu_view_sortbygroup)


        self.fileMenu.addAction(self.menu_save)
        self.viewMenu.addAction(self.menu_view_env)
        self.viewMenu.addMenu(self.menu_view_sortby)

        if len(self.file.dependencies) > 0:
            self.menu_view_includes = QMenu("View Included Files", self)
            self.include_buttons = []
            for include in self.file.dependencies:
                self.include_buttons.append(QAction(include, self))

                self.include_buttons[-1].triggered.connect(self.make_include_listener(include))


                self.menu_view_includes.addAction(self.include_buttons[-1])
            self.viewMenu.addMenu(self.menu_view_includes)


    def make_include_listener(self, include_name):
        def listener(arg1):
            window = RainmeterFileWindow(rainparsing.SkinFile(include_name, self.file.env))
            self.new_child_window(window)
        return listener
    def open_env(self):
        window = EnvWindow(self.file.env, 'Env at ' + self.file.name)
        self.new_child_window(window)


    def new_child_window(self, window):
        self.child_windows.append(window)
        self.child_windows[-1].show()
    def to_section_view(self):
        self.widget_generator = widget_generators.create_file_tree_widget
        self.update_tree()

    def to_group_view(self):
        self.widget_generator = widget_generators.create_file_tree_widget_by_group
        self.update_tree()

    def update_tree(self):
        self.tree_widget = self.widget_generator(self.file)
        self.tree_widget.itemDoubleClicked.connect(self.double_click_on_tree)
        self.setCentralWidget(self.tree_widget)

    def double_click_on_tree(self, clicked_item, column):
        """

         :type column: int
         :type clicked_item: QTreeWidgetItem
         """
        self.tree_widget.editItem(clicked_item, column)

class EnvWindow(QMainWindow):
    def __init__(self, env_obj,name):
        """

        :type file_obj: rainparsing.SkinFile
        """
        QWidget.__init__(self)
        self.env_obj = env_obj
        self.resize(360, 480)
        self.move(300, 300)
        self.setWindowTitle(name)
        self.init_menubar()
        self.child_windows = []
        self.update_tree()
        self.show()

    def init_menubar(self):
        pass

    def update_tree(self):
        self.tree_widget = widget_generators.create_env_tree_widget(self.env_obj)
        self.setCentralWidget(self.tree_widget)

    def double_click_on_tree(self, clicked_item, column):
        """

         :type column: int
         :type clicked_item: QTreeWidgetItem
         """
        pass