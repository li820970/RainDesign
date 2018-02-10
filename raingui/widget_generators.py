import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import rainparsing


def create_collection_tree_widget(collection_obj):
    """

    :type collection_obj: rainparsing.CollectionFolder
    """
    tree = QTreeWidget()
    tree.setHeaderHidden(True)

    for skin_folder in collection_obj.get_all_skin_folders():
        widget_item = create_skin_folder_tree(skin_folder)
        widget_item.model = skin_folder
        tree.addTopLevelItem(widget_item)
    for resource_obj in collection_obj.get_all_resources():
        widget_item = create_resource_folder_tree(resource_obj)
        widget_item.model = resource_obj
        tree.addTopLevelItem(widget_item)
    # tree.itemDoubleClicked.connect( click_callback)
    return tree


def create_skin_folder_tree(skin_folder_obj):
    """

    :type skin_folder_obj: rainparsing.SkinFolder
    """
    tree = QTreeWidgetItem([skin_folder_obj.name])
    for file in skin_folder_obj.get_all_skinfiles():
        widget_item = QTreeWidgetItem([file.name])
        widget_item.model = file
        tree.addChild(widget_item)
    for file in skin_folder_obj.get_all_varfiles():
        widget_item = QTreeWidgetItem([file.name])
        widget_item.model = file
        tree.addChild(widget_item)
    for file in skin_folder_obj.get_all_subfolders():
        widget_item = QTreeWidgetItem([file.name])
        widget_item.model = file
        tree.addChild(widget_item)
    return tree

def create_resource_folder_tree(resource_folder_obj):
    """

    :type resource_folder_obj: rainparsing.ResourceFolder
    """

    tree = QTreeWidgetItem([resource_folder_obj.name])
    for folder in resource_folder_obj.get_all_subfolders():
        widget_item = create_resource_folder_tree(folder)
        widget_item.model = folder
        tree.addChild(widget_item)
    for file in resource_folder_obj.get_all_importables():
        widget_item = QTreeWidgetItem([file.name])
        widget_item.model = file
        tree.addChild(widget_item)
    for file in resource_folder_obj.get_all_resource_files():
        widget_item = QTreeWidgetItem([file.name])
        widget_item.model = file
        tree.addChild(widget_item)
    return tree

def create_file_tree_widget(file_obj):
    """

    :type file_obj: rainparsing.SkinFile
    """
    tree = QTreeWidget()
    tree.setColumnCount(2)
    tree.setHeaderHidden(True)

    tree.header().setSectionResizeMode(tree.header().ResizeToContents)
    tree.header().setStretchLastSection(False)
    # header_widget = create_section_tree(file_obj.header)
    # header_widget.model = file_obj.header
    # tree.addTopLevelItem(header_widget)
    # header_widget.setFlags(header_widget.flags() )
    # meta_widget = create_section_tree(file_obj.metadata)
    # meta_widget.model = file_obj.metadata
    # tree.addTopLevelItem(meta_widget)
    #
    # var_widget = create_section_tree(file_obj.variables)
    # var_widget.model = file_obj.variables
    # tree.addTopLevelItem(var_widget)

    for section_obj in file_obj:
        widget_item = create_section_tree(section_obj)
        widget_item.model = section_obj
        tree.addTopLevelItem(widget_item)
    #
    # for section_obj in file_obj.get_all_measures():
    #     widget_item = create_section_tree(section_obj)
    #     widget_item.model = section_obj
    #     tree.addTopLevelItem(widget_item)
    #
    # for section_obj in file_obj.get_all_meters():
    #     widget_item = create_section_tree(section_obj)
    #     widget_item.model = section_obj
    #     tree.addTopLevelItem(widget_item)

    return tree

def create_section_tree(section_obj):
    """

    :type section_obj: rainparsing.Section
    """
    tree = QTreeWidgetItem([str(section_obj)])
    for key, value in section_obj.props.items():
        widget_item = QTreeWidgetItem([key])
        widget_item.model = section_obj
        widget_item.setText(1, str(value))

        tree.addChild(widget_item)

        # widget_item.setData(1, role=)
    return tree

def create_env_tree_widget(env_obj):
    """

    :type env_obj: rainparsing.envs.local_env
    """
    tree = QTreeWidget()
    tree.setColumnCount(2)
    tree.setHeaderHidden(True)

    tree.header().setSectionResizeMode(tree.header().ResizeToContents)
    tree.header().setStretchLastSection(False)
    variables = QTreeWidgetItem(['Variables'])
    for key, value in env_obj.variables.items():
        widget_item = QTreeWidgetItem([key])
        widget_item.setText(1, str(value))
        variables.addChild(widget_item)
    tree.addTopLevelItem(variables)

    measures = QTreeWidgetItem(['Measures'])
    for key, value in env_obj.measures.items():
        # widget_item = QTreeWidgetItem([str(key)])
        measures.addChild(create_section_tree(value))
        # measures.addChild(widget_item)
    tree.addTopLevelItem(measures)

    meterstyles = QTreeWidgetItem(['MeterStyles'])
    for key, value in env_obj.meterstyles.items():
        # widget_item = QTreeWidgetItem([str(key)])
        meterstyles.addChild(create_section_tree(value))
        # meterstyles.addChild(widget_item)
    tree.addTopLevelItem(meterstyles)
    return tree

def create_file_tree_widget_by_group(file_obj):
    """

    :type file_obj: rainparsing.SkinFile
    """
    tree = QTreeWidget()
    tree.setColumnCount(2)
    tree.setHeaderHidden(True)

    tree.header().setSectionResizeMode(tree.header().ResizeToContents)
    tree.header().setStretchLastSection(False)
    # header_widget = create_section_tree(file_obj.header)
    # header_widget.model = file_obj.header
    # tree.addTopLevelItem(header_widget)
    # header_widget.setFlags(header_widget.flags() )
    # meta_widget = create_section_tree(file_obj.metadata)
    # meta_widget.model = file_obj.metadata
    # tree.addTopLevelItem(meta_widget)
    #
    # var_widget = create_section_tree(file_obj.variables)
    # var_widget.model = file_obj.variables
    # tree.addTopLevelItem(var_widget)

    groups = {}
    ungrouped = QTreeWidgetItem(['UNGROUPED'])
    for section_obj in file_obj:
        widget_item = create_section_tree(section_obj)
        widget_item.model = section_obj
        for group in section_obj.groups:
            if group in groups:
                groups[group].addChild(widget_item)
            else:
                newgroup = QTreeWidgetItem([group])
                newgroup.addChild(widget_item)
                groups[group] = (newgroup)
        if len(section_obj.groups) == 0:
            ungrouped.addChild(widget_item)

    # for section_obj in file_obj.get_all_measures():
    #     widget_item = create_section_tree(section_obj)
    #     widget_item.model = section_obj
    #     for group in section_obj.groups:
    #         if group in groups:
    #             groups[group].addChild(widget_item)
    #         else:
    #             newgroup = QTreeWidgetItem([group])
    #             newgroup.addChild(widget_item)
    #             groups[group] = (newgroup)
    #     if len(section_obj.groups) == 0:
    #         ungrouped.addChild(widget_item)
    # for section_obj in file_obj.get_all_meters():
    #     widget_item = create_section_tree(section_obj)
    #     widget_item.model = section_obj
    #     for group in section_obj.groups:
    #         if group in groups:
    #             groups[group].addChild(widget_item)
    #         else:
    #             newgroup = QTreeWidgetItem([group])
    #             newgroup.addChild(widget_item)
    #             groups[group] = (newgroup)
    #     if len(section_obj.groups) == 0:
    #         ungrouped.addChild(widget_item)
    for group, group_obj in groups.items():
        tree.addTopLevelItem(group_obj)
    tree.addTopLevelItem(ungrouped)
    return tree