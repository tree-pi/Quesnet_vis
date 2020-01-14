#!/usr/bin/env python
import os
import numpy as np
import json
import datetime
import networkx as nx

# Qt part
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolTip, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont
from pyface.qt import QtGui, QtCore

# mayavi vtk part
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MlabSceneModel, SceneEditor
from tvtk.pyface.api import Scene

# self developed function part
from QuestionNetwork import QNmodel
from mlabplot import MPlot3D

# main illustration screen class
class Visualization(HasTraits):
    scene1 = Instance(MlabSceneModel, ())

    @on_trait_change('scene1.activated')
    def update_plot1(self):
        # This function is called when the view is opened.
        self.scene1.mlab.view(0, 75, 150)
        self.scene1.background = (0.1, 0.1, 0.2)

    # the layout of the dialog screated
    view1 = View(Item('scene1', editor=SceneEditor(scene_class=Scene),
                     height=750, width=1000, show_label=False), resizable=True)

    def clear(self):
        self.scene1.mlab.clf()

# main window screen class
class QMayavi(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QMayavi, self).__init__(parent)

        self.setWindowTitle("Mesh Viewer")
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)

        self.visulization = Visualization()
        ui_mlab = Visualization().edit_traits(parent=self, kind='subpanel').control
        layout.addWidget(ui_mlab, 0, 0)
        self.mlab = MPlot3D(mlab=True)

    def draw_node(self, node_cor):
        print ('drawing node funciton called')
        self.mlab.draw_node(node_cor)

    def draw_link(self, link_from, link_to):
        self.mlab.draw_link(link_from, link_to)

    def draw_nodelabel(self, node_cor, node_label):
        self.mlab.draw_nodelabel(node_cor, node_label)

    def draw_linklabel(self, link_from, link_to, link_label):
        self.mlab.draw_linklabel(link_from, link_to, link_label)

    def draw_node_alfa(self, node_cor, node_color, node_size, node_label, status_color, status_size, status_label):

        normal_color = (1, 0, 0)

        color = []
        size = []

        print ('check parameter')
        print ('status_size')
        print (status_size)
        print (node_size)
        print ('status_color')
        print (status_color)
        print (node_color)

        # print len(node_size)
        print (node_size)

        if status_color:
            color = node_color
        else:
            for i in range(len(node_color)):
                color.append(normal_color)

        if status_size:
            size = node_size
        else:
            for i in range(len(node_color)):
                size.append(0.8)

        print ('size')
        print (size)

        self.mlab.draw_node_alfa(node_cor, node_color, node_size)

        if status_label:
            self.draw_nodelabel(node_cor, node_label)

    def draw_link_alfa(self, link_from, link_to, link_label, link_color,status_color, status_arrow, status_label):

        # node_size = len(node_cor)
        normal_color = (0, 0, 1)

        color = []

        if status_color:
            color = link_color
        else:
            for i in range(len(link_from)):
                color.append(normal_color)

        self.mlab.draw_link_alfa(link_from, link_to, color, status_arrow)

        if status_label:
            self.draw_linklabel(link_from, link_to, link_label)


# QN node create sub window class
class QNmodelUI_NodeCreate(QtWidgets.QMainWindow):

    # build the information transfer variable, between sub window to main window
    signal_node = QtCore.pyqtSignal(list)

    signal_node_id = QtCore.pyqtSignal(list)
    signal_node_label = QtCore.pyqtSignal(list)
    signal_node_feature = QtCore.pyqtSignal(list)

    signal_link_id = QtCore.pyqtSignal(list)
    signal_link_from = QtCore.pyqtSignal(list)
    signal_link_from_label = QtCore.pyqtSignal(list)
    signal_link_to = QtCore.pyqtSignal(list)
    signal_link_to_label = QtCore.pyqtSignal(list)
    signal_link_label = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(QNmodelUI_NodeCreate, self).__init__(parent)

        path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        uic.loadUi(os.path.join(path1, 'resources', 'questionnetwork_node_create1.ui'), self)

        self.setWindowTitle("QN model Revise")

        self.cbxNodeCreate_feature.addItem('Central Question')
        self.cbxNodeCreate_feature.addItem('Question')
        self.cbxNodeCreate_feature.addItem('Answer')

        self.chxNodeCreate_link.setChecked(False)
        self.rbnNodeCreate_pnode.setEnabled(False)
        self.rbnNodeCreate_onode.setEnabled(False)
        self.cbxNodeCreate_link.setEnabled(False)
        self.ledNodeCreate_link.setEnabled(False)
        self.btnNodeCreate_link.setEnabled(False)

        self.chxNodeCreate_feature.setChecked(False)
        self.ledNodeCreate_feature.setEnabled(False)
        self.ledNodeCreate_feature_con.setEnabled(False)
        self.btnNodeCreate_feature.setEnabled(False)

        # add the required the model
        self.QNmodel_create = QNmodel()
        self.QNmodel_create._init_()

        print ('QNmodel_create')
        print (self.QNmodel_create.node_id)

        # tree view of the QNmodel_create for preview
        self.tmodel_node_create = self.treemodel_node_create_initialization(self)
        self.node_preview.setModel(self.tmodel_node_create)
        # self.node_view.clicked.connect(self.treefunction)

        self.NodeCreate_progressText.setText('initialization finished')

        # load QN model label call function
        self.btnNodeCreate_node.clicked.connect(self.btnNodeCreate_nodeClicked)

        # load QN model link call function
        self.btnNodeCreate_link.clicked.connect(self.btnNodeCreate_linkClicked)

        # load QN model feature call function
        self.btnNodeCreate_feature.clicked.connect(self.btnNodeCreate_featureClicked)

        # check box enable function
        self.chxNodeCreate_link.stateChanged.connect(self.chxNodeCreate_linkClicked)
        self.chxNodeCreate_feature.stateChanged.connect(self.chxNodeCreate_featureClicked)

        # radio button enable function
        self.rbnNodeCreate_onode.toggled.connect(self.rbnNodeCreate_onodeClicked)


    def btnNodeCreate_nodeClicked(self):

        node = []
        node.append('testnode1')
        node.append('testnode2')

        self.signal_node.emit(node)

        # add the label and feature
        add_label = self.ledNodeCreate_label.text()
        add_feature = self.cbxNodeCreate_feature.currentText()
        self.QNmodel_create.add_node(add_label, add_feature)

        self.signal_node_id.emit(self.QNmodel_create.node_id)
        self.signal_node_label.emit(self.QNmodel_create.node_label)
        self.signal_node_feature.emit(self.QNmodel_create.node_feature)

        self.QNmodel_create_update()
        self.QNmodel_create_link_cbxupdate()

        self.NodeCreate_progressText.setText(add_label+add_feature)

    def btnNodeCreate_linkClicked(self):

        node_len = len(self.QNmodel_create.node_id)
        if node_len < 2:
            self.NodeCreate_progressText.setText('Error, not enough nodes for a link')

        link_feature = self.ledNodeCreate_link.text()
        link_to = node_len - 1

        # add the link from
        if self.rbnNodeCreate_onode.isChecked():
            # using the current node and other node
            label = self.cbxNodeCreate_link.currentText()
            for index in range(len(self.QNmodel_create.node_label)):
                if self.QNmodel_create.node_label[index] == label:
                    link_from = index

        else:
            # using the current node and previous node
            link_from = node_len - 2

        self.QNmodel_create.add_link(link_from, link_to, link_feature)

        # self.signal_node_id.emit(self.QNmodel_create.node_id)
        self.signal_link_id.emit(self.QNmodel_create.link_id)
        self.signal_link_from.emit(self.QNmodel_create.link_from)
        self.signal_link_from_label.emit(self.QNmodel_create.link_from_label)
        self.signal_link_to.emit(self.QNmodel_create.link_to)
        self.signal_link_to_label.emit(self.QNmodel_create.link_to_label)
        self.signal_link_label.emit(self.QNmodel_create.link_label)

        self.NodeCreate_progressText.setText('link create function called')

    def btnNodeCreate_featureClicked(self):

        # ---------------------------------------------------------------------
        # only solve one extra feature situation, TODO multi extra features input

        key = self.ledNodeCreate_feature.text()
        content = self.ledNodeCreate_feature_con.text()
        length1 = len(self.QNmodel_create.node_id)
        length2 = len(self.QNmodel_create.node_feature_content)

        if len(self.QNmodel_create.node_feature_key) == 0:
            self.QNmodel_create.node_feature_key.append(key)

        if length1 == length2:
            # previous nodes all have extra feature
            self.QNmodel_create.add_extrafeature(key, content)
        else:
            for index in range(length2, length1-1, 1):
                self.QNmodel_create.add_extrafeature(key, 'not given')

            self.QNmodel_create.add_extrafeature(key, content)

        print (self.QNmodel_create.node_feature_key)
        print (self.QNmodel_create.node_feature_content)

        self.QNmodel_create_update()
        self.NodeCreate_progressText.setText('feature create function called')


    def chxNodeCreate_linkClicked(self):

        if self.chxNodeCreate_link.isChecked():
             # self.chxNodeCreate_link.setDefault(False)
            self.rbnNodeCreate_pnode.setEnabled(True)
            self.rbnNodeCreate_onode.setEnabled(True)
            self.ledNodeCreate_link.setEnabled(True)
            self.btnNodeCreate_link.setEnabled(True)
            self.rbnNodeCreate_pnode.setChecked(True)

        else:
            self.rbnNodeCreate_pnode.setEnabled(False)
            self.rbnNodeCreate_onode.setEnabled(False)
            self.cbxNodeCreate_link.setEnabled(False)
            self.ledNodeCreate_link.setEnabled(False)
            self.btnNodeCreate_link.setEnabled(False)

    def rbnNodeCreate_onodeClicked(self):
        if self.rbnNodeCreate_onode.isChecked():
            self.cbxNodeCreate_link.setEnabled(True)
        else:
            self.cbxNodeCreate_link.setEnabled(False)

    def chxNodeCreate_featureClicked(self):

        if self.chxNodeCreate_feature.isChecked():
            # self.chxNodeCreate_feature.setDefault(False)
            self.ledNodeCreate_feature.setEnabled(True)
            self.ledNodeCreate_feature_con.setEnabled(True)
            self.btnNodeCreate_feature.setEnabled(True)
        else:
            self.ledNodeCreate_feature.setEnabled(False)
            self.ledNodeCreate_feature_con.setEnabled(False)
            self.btnNodeCreate_feature.setEnabled(False)


    def treemodel_node_create_initialization(self, parent):

        print ('key length')
        print (len(self.QNmodel_create.node_feature_key))

        if len(self.QNmodel_create.node_feature_key) == 0:
            model = QStandardItemModel(0, 3, parent)
            model.setHorizontalHeaderLabels(['index', 'feature', 'label'])

            return model

        else:
            label = ['index', 'feature', 'label']

            for index in range(len(self.QNmodel_create.node_feature_key)):
                label.append(str(self.QNmodel_create.node_feature_key[index]))

            print ('label')
            print (label)
            print (3+len(self.QNmodel_create.node_feature_key))

            model = QStandardItemModel(0, 3+len(self.QNmodel_create.node_feature_key), parent)
            model.setHorizontalHeaderLabels(label)
            # model.appendColumn([QtGui.QStandardItem('new')])

            return model

    def QNmodel_create_update(self):

        # update the tree view
        # self.node_preview.setModel()
        self.tmodel_node_create = self.treemodel_node_create_initialization(self)
        self.node_preview.setModel(self.tmodel_node_create)

        print (self.QNmodel_create.node_id)

        for idx_node in range(len(self.QNmodel_create.node_id)):

            item_node_id = QStandardItem(self.QNmodel_create.node_id[idx_node])
            item_node_feature = QStandardItem(self.QNmodel_create.node_feature[idx_node])
            item_node_label = QStandardItem(self.QNmodel_create.node_label[idx_node])
            # item_node_content = []
            # if self.QNmodel.node_content[idx_node]:
            #     item_node_content = QtGui.QStandardItem(self.QNmodel.node_content[idx_node])

            basic = [item_node_id, item_node_feature, item_node_label]

            for index in range(len(self.QNmodel_create.node_feature_key)):
                basic.append(QStandardItem(self.QNmodel_create.node_feature_content[idx_node]))

            self.tmodel_node_create.appendRow([item_node_id, item_node_feature, item_node_label])

    def QNmodel_create_link_cbxupdate(self):

        print ('cbxNodeCreate_link update')

        self.cbxNodeCreate_link.clear()

        if len(self.QNmodel_create.node_label) > 1:
            for index in range(len(self.QNmodel_create.node_label)-1):
                self.cbxNodeCreate_link.addItem(self.QNmodel_create.node_label[index])


# QN model link create sub window class
class QNmodelUI_LinkCreate(QtWidgets.QMainWindow):

    # build the information transfer variable, between sub window and main window
    signal_link_temp_id = QtCore.pyqtSignal(list)
    signal_link_temp_from = QtCore.pyqtSignal(list)
    signal_link_temp_to = QtCore.pyqtSignal(list)
    signal_link_temp_label = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(QNmodelUI_LinkCreate, self).__init__(parent)

        path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        uic.loadUi(os.path.join(path1, 'resources', 'questionnetwork_link_create.ui'), self)

        self.setWindowTitle("QN model Revise")

        # link create variable initialization
        self.link_import = QNmodel() # QNmodel link from node creation panel
        self.link_add = QNmodel() # QNmodel link from link creation panel
        self.link_create = QNmodel() # QNmodel link to pass to main window

        self.link_import._init_()
        self.link_add._init_()
        self.link_create._init_()

        # tree model initialization
        self.tmodel_link_temp = self.treemodel_link_create_initialization(self)
        self.link_preview.setModel(self.tmodel_link_temp)

        # create node create pop up window
        self.winNodeCreate = QNmodelUI_NodeCreate()

        self.winNodeCreate.signal_link_id.connect(self.deal_emit_link_id)
        # self.progressText.setText('create node function linked')
        # self.winNodeCreate.show()

        # create link create call function
        self.btnLinkCreate_link.clicked.connect(self.btnLinkCreate_linkClicked)

    def deal_emit_link_id(self, data):
        self.LinkCreate_progressText.setText(str(data))

    def node_initialization(self, data):

        # combo box initialization
        self.cbxLinkCreate_link_from.clear()
        self.cbxLinkCreate_link_to.clear()

        for index in range(len(data)):
            self.cbxLinkCreate_link_from.addItem(data[index])
            self.cbxLinkCreate_link_to.addItem(data[index])

    def link_initialization(self, lkid, lkfrom, lkto, lklabel):

        print ('link initialization')

        print (self.link_import.link_id)
        # link_import initialization
        self.link_restart(self.link_import)

        self.link_import.link_id = lkid
        self.link_import.link_from = lkfrom
        self.link_import.link_to = lkto
        self.link_import.link_label = lklabel

        print (self.link_import.link_id)

        self.update_tree(self.link_import, self.link_add)


    def btnLinkCreate_linkClicked(self):
        self.LinkCreate_progressText.setText('Add new link')

        link_from = self.cbxLinkCreate_link_from.currentText()
        link_to = self.cbxLinkCreate_link_to.currentText()
        link_label = self.ledLinkCreate_feature.text()

        self.link_add.add_link_alpha(link_from, link_to, link_label)
        self.update_tree(self.link_import, self.link_add)

        self.link_update()
        self.signal_link_temp_id.emit(self.link_create.link_id)
        self.signal_link_temp_from.emit(self.link_create.link_from)
        self.signal_link_temp_to.emit(self.link_create.link_to)
        self.signal_link_temp_label.emit(self.link_create.link_label)

        # self.signal_link_temp.emit(self.link_create)

    def link_restart(self, linkmodel):
        # reset the link creation model
        linkmodel.link_id = []
        linkmodel.link_from = []
        linkmodel.link_to = []
        linkmodel.link_label = []

    def link_update(self):
        # update the link creation model
        self.link_create.link_id = []
        self.link_create.link_from = []
        self.link_create.link_to = []
        self.link_create.link_label = []

        for idx_link in range(len(self.link_import.link_id)):
            self.link_create.link_id.append(self.link_import.link_id[idx_link])
            self.link_create.link_from.append(self.link_import.link_from[idx_link])
            self.link_create.link_to.append(self.link_import.link_to[idx_link])
            self.link_create.link_label.append(self.link_import.link_label[idx_link])

        for idx_link in range(len(self.link_add.link_id)):
            self.link_create.link_id.append(self.link_add.link_id[idx_link])
            self.link_create.link_from.append(self.link_add.link_from[idx_link])
            self.link_create.link_to.append(self.link_add.link_to[idx_link])
            self.link_create.link_label.append(self.link_add.link_label[idx_link])

    def treemodel_link_create_initialization(self, parent):

        label = ['index', 'from', 'to', 'label']
        model = QStandardItemModel(0, 4, parent)
        model.setHorizontalHeaderLabels(label)

        return model

    def update_tree(self, link_import, link_add):
        self.LinkCreate_progressText.setText('QN creation model link updated')
        print ('link tree update')

        self.tmodel_link_temp = self.treemodel_link_create_initialization(self)
        self.link_preview.setModel(self.tmodel_link_temp)

        print ('link id check')
        print (self.link_import.link_id)

        for idx_link in range(len(self.link_import.link_id)):

            item_link_id = QStandardItem(self.link_import.link_id[idx_link])
            item_link_from = QStandardItem(self.link_import.link_from[idx_link])
            item_link_to = QStandardItem(self.link_import.link_to[idx_link])
            item_link_label =pQStandardItem(self.link_import.link_label[idx_link])

            self.tmodel_link_temp.appendRow([item_link_id,item_link_from,item_link_to,item_link_label])

        for idx_link in range(len(self.link_add.link_id)):

            item_link_id = QStandardItem(self.link_add.link_id[idx_link])
            item_link_from =QStandardItem(self.link_add.link_from[idx_link])
            item_link_to = QStandardItem(self.link_add.link_to[idx_link])
            item_link_label =QStandardItem(self.link_add.link_label[idx_link])

            self.tmodel_link_temp.appendRow([item_link_id,item_link_from,item_link_to,item_link_label])


# main window class
class QNMODELUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(QNMODELUI, self).__init__()
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        uic.loadUi(os.path.join(path, 'resources', 'questionnetwork.ui'), self)

        self.dirname = path
        self.plot = QMayavi()
        self.boxPlot.addWidget(self.plot)

        # test the tree view of the model
        # self.tree_model = self.tree_model_initialization(self)
        # self.tree_view.setModel(self.tree_model)
        # self.tree_view.clicked.connect(self.treefunction)

        self.tree_model_node = self.treemodel_node_initialization(self)
        self.node_view.setModel(self.tree_model_node)
        self.node_view.clicked.connect(self.treefunction)

        self.tree_model_link = self.treemodel_link_initialization(self)
        self.link_view.setModel(self.tree_model_link)
        self.link_view.clicked.connect(self.treefunction)

        # load QN model call function
        self.btnLoadQN.clicked.connect(self.btnLoadQNClicked)

        # create QN model call function
        # restart QN model function
        self.btnRestart.clicked.connect(self.btnRestartClicked)

        # QN model node create funciton
        self.btnCreateNode.clicked.connect(self.btnCreateNodeClicked)

        # QN model linnk create funciton
        self.btnCreateLink.clicked.connect(self.btnCreateLinkClicked)

        # QN model preview function
        self.btnPreview.clicked.connect(self.btnPreviewClicked)

        # draw QN model call function*r
        self.btnDrawQN.clicked.connect(self.btnDrawQNClicked)

        # Node and Link features checkbox illustrated
        self.chxShowNode.stateChanged.connect(self.chxShowNodeClicked)
        self.chxShowLink.stateChanged.connect(self.chxShowLinkClicked)

        self.chxShowNode.setChecked(True)
        self.chxShowLink.setChecked(True)

        # load QN model node features call function
        self.btnShowNode.clicked.connect(self.btnShowNodeClicked)

        # load QN model link features call function
        self.btnShowLink.clicked.connect(self.btnShowLinkClicked)

        # QNmodel initialization
        self.QNmodel = QNmodel()
        self.QNmodel._init_()

        # QNmodel_node initialization, to store the temp QN node model
        self.QNmodel_temp = QNmodel()
        self.QNmodel_temp._init_()

        # # connect the pop up window
        # self.window2 = QNmodelUI_Popup()
        # self.window2.__init__()

        # create node create pop up window
        self.winNodeCreate = QNmodelUI_NodeCreate()
        # self.winNodeCreate.__init__()

        # create link create pop up window
        self.winLinkCreate = QNmodelUI_LinkCreate()
        # self.winLinkCreate.__init__()

    def btnLoadQNClicked(self):
        print ('pickle load function called')

        filename = QtWidgets.QFileDialog.getOpenFileName(
                self.plot, 'Open file', self.dirname,
                'Json File (*.json);; Pickle File (*.p)')
        print (filename)

        # pyqt5 requires the filename as a string
        filename = str(filename[0])

        self.dirname = os.path.dirname(filename)

        if filename:
            if filename.split('.')[-1] == 'json':
                print ('json file obsreved')

            if filename.split('.')[-1] == 'p':
                print ('pickle file observed')

                self.dirname = os.path.dirname(filename)
                self.QNmodel.load_pickle(filename)

                self.QNmodel_update()

        self.QNmodel_check()

    def btnRestartClicked(self):
        self.progressText.setText('restart function called')

        self.QNmodel._init_()

        self.tree_model_node = self.treemodel_node_initialization(self)
        self.node_view.setModel(self.tree_model_node)
        self.tree_model_link = self.treemodel_link_initialization(self)
        self.link_view.setModel(self.tree_model_link)

        self.progressText.setText('restart function checked')


    def btnCreateNodeClicked(self):
        self.progressText.setText('create node function called')

        # update the QNmodel node part when the add node buttom clicked
        self.winNodeCreate.signal_node_id.connect(self.deal_emit_node_id)
        self.winNodeCreate.signal_node_label.connect(self.deal_emit_node_label)
        self.winNodeCreate.signal_node_feature.connect(self.deal_emit_node_feature)

        # update the QNmodel_temp link part when the add link button clicked
        self.winNodeCreate.signal_link_id.connect(self.deal_emit_link_id)
        self.winNodeCreate.signal_link_from.connect(self.deal_emit_link_from)
        self.winNodeCreate.signal_link_to.connect(self.deal_emit_link_to)
        self.winNodeCreate.signal_link_from_label.connect(self.deal_emit_link_from_label)
        self.winNodeCreate.signal_link_to_label.connect(self.deal_emit_link_to_label)
        self.winNodeCreate.signal_link_label.connect(self.deal_emit_link_label)

        self.winNodeCreate.signal_node_id.connect(self.deal_emit_slot)

        # receive the information and pass the link creation
        # self.winNodeCreate.signal_node_label.connect(self.deal_emit_node_label)

        self.progressText.setText('create node function linked')
        self.winNodeCreate.show()

    def deal_emit_node_id(self, data):
        # reset the related parameter
        self.QNmodel.node_id = []

        # update the parameter value
        self.QNmodel.node_id = data

    def deal_emit_node_label(self, data):
        self.QNmodel.node_label = []
        self.QNmodel.node_label = data

        self.winLinkCreate.node_initialization(data)

    def deal_emit_node_feature(self, data):
        self.QNmodel.node_feature = []
        self.QNmodel.node_feature = data

    def deal_emit_link_id(self, data):
        self.QNmodel_temp.link_id = []
        self.QNmodel_temp.link_id = data

    def deal_emit_link_from(self, data):
        self.QNmodel_temp.link_from = []
        self.QNmodel_temp.link_from = data

    def deal_emit_link_from_label(self, data):
        self.QNmodel_temp.link_from_label = []
        self.QNmodel_temp.link_from_label = data

    def deal_emit_link_to(self, data):
        self.QNmodel_temp.link_to = []
        self.QNmodel_temp.link_to = data

    def deal_emit_link_to_label(self, data):
        self.QNmodel_temp.link_to_label = []
        self.QNmodel_temp.link_to_label = data

    def deal_emit_link_label(self, data):
        self.QNmodel_temp.link_label = []
        self.QNmodel_temp.link_label = data

        # update the create link model
        self.winLinkCreate.link_initialization(self.QNmodel_temp.link_id, self.QNmodel_temp.link_from_label,
                                                self.QNmodel_temp.link_to_label, self.QNmodel_temp.link_label)

    def deal_emit_slot(self, data):
        self.progressText.setText(str(data))


    def btnCreateLinkClicked(self):
        self.progressText.setText('create link function called')

        self.winLinkCreate.__init__()

        # test
        # self.winLinkCreate.signal_link_temp.connect(self.deal_emit_link_temp)

        # update the QN model link part from the link creation
        self.winLinkCreate.signal_link_temp_id.connect(self.deal_emit_link_temp_id)
        self.winLinkCreate.signal_link_temp_from.connect(self.deal_emit_link_temp_from)
        self.winLinkCreate.signal_link_temp_to.connect(self.deal_emit_link_temp_to)
        self.winLinkCreate.signal_link_temp_label.connect(self.deal_emit_link_temp_label)

        self.winLinkCreate.show()

    def deal_emit_link_temp_id(self, data):
        self.QNmodel.link_id = []
        self.QNmodel.link_id = data

    def deal_emit_link_temp_from(self, data):
        self.QNmodel.link_from_label = []
        self.QNmodel.link_from_label = data

    def deal_emit_link_temp_to(self, data):
        self.QNmodel.link_to_label = []
        self.QNmodel.link_to_label = data

    def deal_emit_link_temp_label(self, data):
        self.QNmodel.link_label = []
        self.QNmodel.link_label = data

    def deal_emit_link_temp(self, data):
        self.progressText.setText(str(data))

    def btnPreviewClicked(self):
        # preview the node and link in the QN model creation section
        print ('QN model creation preview')

        # update the QN model link part from the link creation
        print (self.QNmodel.node_id)
        print (self.QNmodel.node_label)
        print (self.QNmodel.node_feature)
        print (self.QNmodel.link_id)
        print (self.QNmodel.link_from_label)
        print (self.QNmodel.link_to_label)
        print (self.QNmodel.link_label)

        self.QNmodel_update()
        self.QNmodel.create_model()

    def btnDrawQNClicked(self):

        self.progressText.setText('drawing function called')

        # generate the coordinate of the node
        self.QNmodel.cor_generate()

        # drawing the point and the link in the map
        self.plot.draw_node(self.QNmodel.node_cor)

        # drawing the point and the link in the map
        self.plot.draw_link(self.QNmodel.link_from_cor, self.QNmodel.link_to_cor)

    def chxShowNodeClicked(self):

        if self.chxShowNode.isChecked():
            self.chxShowNodeColor.setEnabled(True)
            self.chxShowNodeLabel.setEnabled(True)
            self.chxShowNodeSize.setEnabled(True)
        else:
            self.chxShowNodeColor.setEnabled(False)
            self.chxShowNodeLabel.setEnabled(False)
            self.chxShowNodeSize.setEnabled(False)

    def chxShowLinkClicked(self):

        if self.chxShowLink.isChecked():
            self.chxShowLinkArrow.setEnabled(True)
            self.chxShowLinkColor.setEnabled(True)
            self.chxShowLinkLabel.setEnabled(True)
        else:
            self.chxShowLinkArrow.setEnabled(False)
            self.chxShowLinkColor.setEnabled(False)
            self.chxShowLinkLabel.setEnabled(False)


    def btnShowNodeClicked(self):

        self.progressText.setText('Node update illustration function called')
        self.remove_node()

        print ('parameter pre')
        print (self.QNmodel.node_size)

        if self.chxShowNode.isChecked():
            # drawing the node with the required settings
            self.plot.draw_node_alfa(self.QNmodel.node_cor, self.QNmodel.node_color,
                                    self.QNmodel.node_size, self.QNmodel.node_label, self.chxShowNodeColor.isChecked(),
                                    self.chxShowNodeSize.isChecked(),
                                    self.chxShowNodeLabel.isChecked())

        # self.QNmodel_check()

        # mouse pick function
        self.figure = self.plot.mlab.get_gcf()
        self.picker = self.figure.on_mouse_pick(self.picker_callback)

    def remove_node(self):


        for i in range(0,len(self.plot.mlab.obj_node)):

            self.plot.mlab.obj_node[0].remove()
            del self.plot.mlab.obj_node[0]

        for i in range(0,len(self.plot.mlab.obj_nodetext)):

            # print 'self.plot.mlab.obj_nodetext'
            # print self.plot.mlab.obj_nodetext[0]
            self.plot.mlab.obj_nodetext[0].remove()
            del self.plot.mlab.obj_nodetext[0]

        # if self.plot.mlab.obj_node:
        #     for index in self.plot.mlab.obj_node[:]:
        #         print index
        #         index.remove()
        #         del index
        # #
        # #
        # if self.plot.mlab.obj_nodetext:
        #     for index in self.plot.mlab.obj_nodetext[:]:
        #         self.plot.mlab.obj_nodetext[0].remove()
        #         del self.plot.mlab.obj_nodetext[0]

        # print 'after'
        # print self.plot.mlab.obj_node
        # print self.plot.mlab.obj_nodetext

    def btnShowLinkClicked(self):

        self.progressText.setText('Link update illustration function called')

        self.remove_link()
        # print 'parameter pre'
        # print self.QNmodel.node_size

        if self.chxShowLink.isChecked():
            # drawing the node with the required settings
            self.plot.draw_link_alfa(self.QNmodel.link_from_cor, self.QNmodel.link_to_cor,
                                    self.QNmodel.link_label, self.QNmodel.link_color,
                                    self.chxShowLinkColor.isChecked(),
                                    self.chxShowLinkArrow.isChecked(),
                                    self.chxShowLinkLabel.isChecked())
        # self.QNmodel_check()


    def remove_link(self):

        for i in range(0,len(self.plot.mlab.obj_link)):
            self.plot.mlab.obj_link[0].remove()
            del self.plot.mlab.obj_link[0]

        for i in range(0,len(self.plot.mlab.obj_linktext)):
            self.plot.mlab.obj_linktext[0].remove()
            del self.plot.mlab.obj_linktext[0]


    def picker_callback(self, picker_obj):

        self.current_view = self.plot.mlab.get_currentView()
        # print self.plot.mlab.obj_node
        # print self.plot.mlab.obj_node[0]
        self.glyph_points = self.plot.mlab.obj_node[0].glyph.glyph_source.glyph_source.output.points.to_array()

        if picker_obj.actor in self.plot.mlab.obj_node[0].actor.actors:

            self.point_id = picker_obj.point_id/self.glyph_points.shape[0]
            print (self.point_id)

            print (self.QNmodel.node_label[self.point_id])

    # design the tree model for the illustration of Question Networks
    def treemodel_node_initialization(self, parent):

        model = QStandardItemModel(0, 4, parent)
        model.setHorizontalHeaderLabels(['index', 'feature', 'label', 'content'])
        return model

    def treemodel_link_initialization(self, parent):

        model = QStandardItemModel(0, 4, parent)
        model.setHorizontalHeaderLabels(['index', 'from', 'to', 'label'])
        return model

    def QNmodel_update(self):

        print ('QNmodel_update')

        self.tree_model_node = self.treemodel_node_initialization(self)
        self.node_view.setModel(self.tree_model_node)

        for idx_node in range(len(self.QNmodel.node_id)):

            item_node_id = QStandardItem(self.QNmodel.node_id[idx_node])
            item_node_feature = QStandardItem(self.QNmodel.node_feature[idx_node])
            item_node_label = QStandardItem(self.QNmodel.node_label[idx_node])
            # item_node_content = []
            # if self.QNmodel.node_content[idx_node]:
            #     item_node_content = QtGui.QStandardItem(self.QNmodel.node_content[idx_node])

            self.tree_model_node.appendRow([item_node_id, item_node_feature, item_node_label])


        self.tree_model_link = self.treemodel_link_initialization(self)
        self.link_view.setModel(self.tree_model_link)


        for idx_link in range(len(self.QNmodel.link_id)):

            item_link_id = QStandardItem(self.QNmodel.link_id[idx_link])
            item_link_from = QStandardItem(self.QNmodel.link_from_label[idx_link])
            item_link_to = QStandardItem(self.QNmodel.link_to_label[idx_link])
            item_link_label = QStandardItem(self.QNmodel.link_label[idx_link])

            # find the label of the link from and to
            # label_from =
            # label_to = []
            # for idx_label in range(len(self.QNmodel.node_id)):
            #     if self.QNmodel.node_id[idx_label] == item_link_from:
            #         label_from = self.QNmodel.node_label[idx_label]
            #     if self.QNmodel.node_id[idx_label] == item_link_to:
            #         label_to = self.QNmodel.node_label[idx_label]
            # item_from_label = QtGui.QStandardItem(label_from)
            # item_to_label = QtGui.QStandardItem(label_to)

            self.tree_model_link.appendRow([item_link_id, item_link_from, item_link_to, item_link_label])


    def QNmodel_check(self):

        print ('check model')
        print ('node_label')
        print (self.QNmodel.node_label)
        print ('node_size')
        print (self.QNmodel.node_size)
        print ('node_color')
        print (self.QNmodel.node_color)
        print ('finished')

    def treefunction(self, index):
        print (index.model().itemFromIndex(index).text())
        print (index.model().itemFromIndex(index))
        print (index.model())

        print ('check the tree model click function')
        print (index.model().rowCount())
        print (index.row())
        print (index.column())

        self.progressText.setText(index.model().itemFromIndex(index).text())

        row = index.row()
        column = index.column()
        content = QStandardItem('check')


# main function
if __name__ == "__main__":

    app = QtWidgets.QApplication.instance()
    QNmodel = QNMODELUI()
    QNmodel.show()
    app.exec_()
