
# coding: utf-8

# In[1]:


# This program aims to build an interface of the question networks, which 
# aims to describe the input node and link in real time. 
# Basic UI functions are designed to be integrated in the program

# part 1 
# basic definition 

import networkx as nx 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolTip, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QFont

# node and link initialization 
QNnodes = []
QNlinks = []
Nnode = 0
Nlink = 0


# In[2]:


# part 2 
# build the basic interface for the node and lnk 


class WidgetGallery(QDialog):
    
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        self.setGeometry(0, 0, 1200, 900)
        self.setWindowTitle('Question Network')
        self.setWindowIcon(QIcon('icon.png'))
        
        QToolTip.setFont(QFont('SansSerif', 12))
        
        # Creat the Subsequent questions and links input part
        self.createTopGroupBox()
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createMiddleLeftGroupBox()
        self.createMiddleRightGroupBox()
        self.createBottomGroupBox()
        self.createPreviewBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.TopGroupBox, 0, 0, 1, 2)
        mainLayout.addWidget(self.TopLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.TopRightGroupBox, 1, 1)
        mainLayout.addWidget(self.MiddleLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.MiddleRightGroupBox, 2, 1)
        mainLayout.addWidget(self.BottomGroupBox, 3, 0, 1, 2)
        mainLayout.addWidget(self.PreviewBox, 4, 0, 1, 2)
#         mainLayout.setRowStretch(1, 1)
#         mainLayout.setRowStretch(2, 1)
#         mainLayout.setColumnStretch(0, 1)
#         mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)


    def createTopGroupBox(self):
        self.TopGroupBox = QGroupBox("Central Question")
        
        # Creat the central quesiton input part 
        self.CQLabel = QLabel("Central Question")
        self.CQLabelEdit = QLineEdit()
        self.CQbtn = QPushButton("Add", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.CQLabel)
        layout.addWidget(self.CQLabelEdit)
        layout.addWidget(self.CQbtn)
#         layout.addStretch(1)
        self.TopGroupBox.setLayout(layout)
        
        self.CQbtn.clicked.connect(self.CQbuttonClicked)


    def createTopLeftGroupBox(self):
        self.TopLeftGroupBox = QGroupBox("Subsequent Question")
        
        self.SQLabel = QLabel("Subsequent Question")
        self.SQLabelEdit = QLineEdit()
        self.SQFeature = QLabel("Feature")
        self.SQFeatureEdit = QLineEdit()
        self.SQbtn = QPushButton("Add", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.SQLabel)
        layout.addWidget(self.SQLabelEdit)
        layout.addWidget(self.SQFeature)
        layout.addWidget(self.SQFeatureEdit)
        layout.addWidget(self.SQbtn)
#         layout.addStretch(1)
        self.TopLeftGroupBox.setLayout(layout)
        
        self.SQbtn.clicked.connect(self.SQbuttonAddClicked)

    def createTopRightGroupBox(self):
        self.TopRightGroupBox = QGroupBox("Links")
        
        self.LKFrom = QLabel("Link Start")
        self.LKFromEdit = QLineEdit()
        self.LKTo = QLabel("Link End")
        self.LKToEdit = QLineEdit()
        self.LKFeature = QLabel("Feature")
        self.LKFeatureEdit = QLineEdit()
        self.LKbtn = QPushButton("Add", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.LKFrom)
        layout.addWidget(self.LKFromEdit)
        layout.addWidget(self.LKTo)
        layout.addWidget(self.LKToEdit)
        layout.addWidget(self.LKFeature)
        layout.addWidget(self.LKFeatureEdit)
        layout.addWidget(self.LKbtn)
#         layout.addStretch(1)
        self.TopRightGroupBox.setLayout(layout)
    
        self.LKbtn.clicked.connect(self.LKbuttonAddClicked)
    
    def createMiddleLeftGroupBox(self):
        self.MiddleLeftGroupBox = QGroupBox("Question Revise")
        
        self.SQRLabel = QLabel("Question Index")
        self.SQRLabelEdit = QLineEdit()
        self.SQRbtn = QPushButton("Delete", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.SQRLabel)
        layout.addWidget(self.SQRLabelEdit)
        layout.addWidget(self.SQRbtn)
#         layout.addStretch(1)
        self.MiddleLeftGroupBox.setLayout(layout)
    
        self.SQRbtn.clicked.connect(self.SQRbuttonClicked)
    
    def createMiddleRightGroupBox(self):
        self.MiddleRightGroupBox = QGroupBox("Link Revise")
        
        self.LKRid = QLabel("Link Index")
        self.LKRidEdit = QLineEdit()
        self.LKRbtn = QPushButton("Delete", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.LKRid)
        layout.addWidget(self.LKRidEdit)
        layout.addWidget(self.LKRbtn)
#         layout.addStretch(1)
        self.MiddleRightGroupBox.setLayout(layout)
    
        self.LKRbtn.clicked.connect(self.LKRbuttonClicked)
        
    def createBottomGroupBox(self):
        self.BottomGroupBox = QGroupBox("Summary")
        
        self.CQSummary = QLabel("Central Question")
        self.CQSummaryEdit = QLabel()
        self.SQSummary = QLabel("Subsequent Question")
        self.SQSummaryEdit = QTableWidget()
        self.LKSummary = QLabel("Links")
        self.LKSummaryEdit = QTableWidget()
#         self.LKSummaryEdit = QLabel()
        
        layout = QVBoxLayout()
        layout.addWidget(self.CQSummary)
        layout.addWidget(self.CQSummaryEdit)
        layout.addWidget(self.SQSummary)
        layout.addWidget(self.SQSummaryEdit)
        layout.addWidget(self.LKSummary)
        layout.addWidget(self.LKSummaryEdit)
                
        layout.addStretch(1)
        self.BottomGroupBox.setLayout(layout)
    
    def createPreviewBox(self):
        self.PreviewBox = QGroupBox("Preview")
        
        self.PVbtn = QPushButton("Preview",self)
        self.PVQNsimple = QLabel()
        self.PVQNfull = QLabel()
        
        layout = QGridLayout()
        layout.addWidget(self.PVbtn,0,0)
        layout.addWidget(self.PVQNsimple,1,0)
        layout.addWidget(self.PVQNfull,1,1)
        
#         layout.addStretch(1)
        self.PreviewBox.setLayout(layout)
        
        self.PVbtn.clicked.connect(self.PVbuttonClicked)
    
    def CQbuttonClicked(self):
        
        sender = self.sender()
        CQtext = self.CQLabelEdit.text()
        
        # add central question into the QNnodes
        Nnode = np.size(QNnodes)
        QNnodes.append({'index':str(Nnode),'question':CQtext,'feature':'central question'})
        
#         # renew the Nnode
#         Nnode = Nnode + 1
        
        # print the central quesiton in the summary panel 
        self.CQSummaryEdit.setText(CQtext)
    
    def SQbuttonAddClicked(self):
        
        sender = self.sender()
        SQtext = self.SQLabelEdit.text()
        SQfeature = self.SQFeatureEdit.text()
        
        # add central question into the QNnodes
        Nnode = np.size(QNnodes)
        QNnodes.append({'index':str(Nnode),'question':SQtext,'feature':SQfeature})
        
#         # renew the Nnode
#         Nnode = Nnode + 1
        
        # print the all quesiton in the summary panel, refresh every time
        QNnodesize = np.size(QNnodes)
        
        self.SQSummaryEdit.setRowCount(QNnodesize+1)
        self.SQSummaryEdit.setColumnCount(3)
        self.SQSummaryEdit.setItem(0,0, QTableWidgetItem("Index"))
        self.SQSummaryEdit.setItem(0,1, QTableWidgetItem("Subsequent Question"))
        self.SQSummaryEdit.setItem(0,2, QTableWidgetItem("Feature"))
        
        index = 1
        
        for node in QNnodes:
            self.SQSummaryEdit.setItem(index,0, QTableWidgetItem(node['index']))
            self.SQSummaryEdit.setItem(index,1, QTableWidgetItem(node['question']))
            self.SQSummaryEdit.setItem(index,2, QTableWidgetItem(node['feature']))
            index = index + 1
    
    def LKbuttonAddClicked(self):
        
        sender = self.sender()
        LKstart = self.LKFromEdit.text()
        LKend = self.LKToEdit.text()
        LKfeature = self.LKFeatureEdit.text()
        
        # add link to QNlinks
        Nlink = np.size(QNlinks)
        QNlinks.append({'index':str(Nlink),'start':LKstart,'end':LKend,'feature':LKfeature})
        
#         #renew the Nlink
#         Nlink = Nlink + 1
        
        # print the all quesiton in the summary panel, refresh every time
        QNlinksize = np.size(QNlinks)
        
        self.LKSummaryEdit.setRowCount(QNlinksize+1)
        self.LKSummaryEdit.setColumnCount(4)
        self.LKSummaryEdit.setItem(0,0, QTableWidgetItem("Index"))
        self.LKSummaryEdit.setItem(0,1, QTableWidgetItem("Start"))
        self.LKSummaryEdit.setItem(0,2, QTableWidgetItem("End"))
        self.LKSummaryEdit.setItem(0,3, QTableWidgetItem("Feature"))
        
        index = 1
        
        for link in QNlinks:
            self.LKSummaryEdit.setItem(index,0, QTableWidgetItem(link['index']))
            self.LKSummaryEdit.setItem(index,1, QTableWidgetItem(link['start']))
            self.LKSummaryEdit.setItem(index,2, QTableWidgetItem(link['end']))
            self.LKSummaryEdit.setItem(index,3, QTableWidgetItem(link['feature']))
            index = index + 1
    
    def SQRbuttonClicked(self):
        
        sender = self.sender()
        
        SQdelete = self.SQRLabelEdit.text()
        
        for node in QNnodes:
            if node['index'] == SQdelete:
                QNnodes.remove(node)
        
        # rearrange the index in the QNnodes
        QNnodesize = np.size(QNnodes)
        for nodeindex in range(QNnodesize):
            QNnodes[nodeindex]['index'] = str(nodeindex)
        
        # refresh the summary table
                
        self.SQSummaryEdit.setRowCount(QNnodesize+1)
        self.SQSummaryEdit.setColumnCount(3)
        self.SQSummaryEdit.setItem(0,0, QTableWidgetItem("Index"))
        self.SQSummaryEdit.setItem(0,1, QTableWidgetItem("Subsequent Question"))
        self.SQSummaryEdit.setItem(0,2, QTableWidgetItem("Feature"))
        
        index = 1
        
        for node in QNnodes:
            self.SQSummaryEdit.setItem(index,0, QTableWidgetItem(node['index']))
            self.SQSummaryEdit.setItem(index,1, QTableWidgetItem(node['question']))
            self.SQSummaryEdit.setItem(index,2, QTableWidgetItem(node['feature']))
            index = index + 1

    def LKRbuttonClicked(self):
        
        sender = self.sender()
        
        LKdelete = self.LKRidEdit.text()
        
        for link in QNlinks:
            if link['index'] == LKdelete:
                QNlinks.remove(link)
        
        
        # rearrange the index in the QNlinks
        QNlinksize = np.size(QNlinks)
        for linkindex in range(QNlinksize):
            QNlinks[linkindex]['index'] = str(linkindex)
        
        # refresh the summary table
        self.LKSummaryEdit.setRowCount(QNlinksize+1)
        self.LKSummaryEdit.setColumnCount(4)
        self.LKSummaryEdit.setItem(0,0, QTableWidgetItem("Index"))
        self.LKSummaryEdit.setItem(0,1, QTableWidgetItem("Start"))
        self.LKSummaryEdit.setItem(0,2, QTableWidgetItem("End"))
        self.LKSummaryEdit.setItem(0,3, QTableWidgetItem("Feature"))
        
        index = 1
        
        for link in QNlinks:
            self.LKSummaryEdit.setItem(index,0, QTableWidgetItem(link['index']))
            self.LKSummaryEdit.setItem(index,1, QTableWidgetItem(link['start']))
            self.LKSummaryEdit.setItem(index,2, QTableWidgetItem(link['end']))
            self.LKSummaryEdit.setItem(index,3, QTableWidgetItem(link['feature']))
            index = index + 1        
        
    def PVbuttonClicked(self):
        
        sender = self.sender()
        
        #build the network object from the QNnodes and QNlinks
        Q = nx.Graph()
        
        # save the QNnodes and QNlinks
        QNnodesfile = 'QNnodes' + self.CQLabelEdit.text() + '.txt'
        QNlinksfile = 'QNlinks' + self.CQLabelEdit.text() + '.txt'
        
        with open(QNnodesfile, 'w') as outputfile:
#             json.dump(QNnodes, outputfile)
            for node in QNnodes:
                outputfile.write("%s\n" % node)
        
        
        with open(QNlinksfile, 'w') as outputfile:
#             json.dump(QNlinksfile, outputfile)
            for link in QNlinks:
                outputfile.write("%s\n" % link)
        
        # add nodes into the graph
        for node in QNnodes:
            nd_index = node['index']
            nd_label = node['question']

            Q.add_node(nd_index,label=nd_label)

        # add edges into the graph
        for link in QNlinks:
            link_from = link['start']
            link_to = link['end']
            #     nd_index = node['id']
            link_label = link['feature']
                
            Q.add_edge(link_from,link_to,label=link_label)
    
        fig = plt.figure(frameon=False)
        fig.set_size_inches(4, 2.5) 
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

        pos = nx.kamada_kawai_layout(Q)
        # nx.draw(Q,pos)

#         # set the color map 
#         color_map = []
#         for node in allnodes:
#             if node['id'] == rid:
#                 color_map.append('orange')
#             elif node['id'][0] == 'a':
#                 color_map.append('green')
#             else:
#                 color_map.append('blue')

#         nx.draw_networkx(Q,pos,node_color=color_map,arrows=True,arrowstyle='->',arrowsize=25,with_labels=False)
        
        # draw the simple graph
        nx.draw_networkx(Q,pos,arrows=True,arrowstyle='->',arrowsize=25,with_labels=False)
        node_labels = nx.get_node_attributes(Q,'label')
        edge_labels = nx.get_edge_attributes(Q,'label')
        
        QNname = self.CQLabelEdit.text()
        simple = 'QN_simple ' + QNname + '.png'
        fig.savefig(simple, dpi=100)
        
        # draw the full graph
        nx.draw_networkx_labels(Q,pos,labels=node_labels,font_size = 12)
        nx.draw_networkx_edge_labels(Q, pos, labels = edge_labels,font_size = 9)
        
        full = 'QN_full ' + QNname + '.png'
        fig.savefig(full, dpi=100)
                
        # nx.draw(Q,with_labels = True,font_weight = 'bold',node_size = 1000,node_color='green',node_shape='h')
        
        # illustration
        QNpicfull = QPixmap(full)
        QNpicsimple = QPixmap(simple)
        
        self.PVQNsimple.setPixmap(QNpicsimple)
        self.PVQNfull.setPixmap(QNpicfull)


# In[ ]:


if __name__ == '__main__':

    import sys
    
    QNnodes = []
    QNlinks = []
    Nnode = 0
    Nlink = 0

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 

