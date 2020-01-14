
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import pickle
import os
import math as m

class QNmodel():

    # model = nx.Graph()
    #
    # node_id = []
    # node_feature = []
    # node_label = []
    # node_content = []
    # node_reference = []
    # node_color = []
    # node_size = []
    # node_cor = []
    # node_feature_key = []
    # node_feature_content = []
    #
    # link_id = []
    # link_from = []
    # link_to = []
    # link_from_label = []
    # link_to_label = []
    # link_label = []
    # link_from_cor = []
    # link_to_cor = []

    def _init_(self):

        # serve as restart function
        self.model = nx.Graph()

        self.node_id = []
        self.node_feature = []
        self.node_label = []
        self.node_content = []
        self.node_reference = []
        self.node_color = []
        self.node_size = []
        self.node_cor = []
        self.node_feature_key = []
        self.node_feature_content = []

        self.link_id = []
        self.link_from = []
        self.link_to = []
        self.link_from_label = []
        self.link_to_label = []
        self.link_label = []
        self.link_from_cor = []
        self.link_to_cor = []
        self.link_color = []

    def load_pickle(self, filename):

        # self._init_()

        print ('QN model initialization')

        # python3 version
        with open(filename, 'rb') as f:
            mydict = pickle.load(f)

        # python2 version
        # picklefile = open(filename)
        # mydict = pickle.load(picklefile)
        # picklefile.close()

        # divde the node and link
        [dic_node, dic_link] = mydict

        # set the color map
        color_map = []
        rgb_map = []
        title_name = []

        # add nodes into the QNmodel
        (row, col) = dic_node.shape
        for index in range(row):
            nd_id = dic_node.iloc[index]['id']
            nd_content = dic_node.iloc[index]['content']
            nd_feature = dic_node.iloc[index]['feature']
            nd_label = dic_node.iloc[index]['label']
            nd_reference = dic_node.iloc[index]['reference']

            self.node_id.append(nd_id)
            self.node_feature.append(nd_feature)
            self.node_label.append(nd_label)
            self.node_content.append(nd_content)
            self.node_reference.append(nd_reference)

            # build the color map
            if nd_feature == 'Central question':
                rgb_map.append({'r': 205, 'g': 37, 'b': 38, 'a': 0})
                color_map.append((1,0,0))
                node_size = 1
                title_name = nd_label
            elif nd_feature == 'Question':
                rgb_map.append({'r': 205, 'g': 137, 'b': 38, 'a': 0})
                color_map.append((0,0,1))
                node_size = 0.7
            else:
                rgb_map.append({'r': 144, 'g': 202, 'b': 249, 'a': 0})
                color_map.append((0,1,0))
                node_size = 0.3

            self.node_color.append(color_map[-1])
            self.node_size.append(node_size)

            self.model.add_node(nd_id,feature=nd_feature,content=nd_content,label=nd_label,reference=nd_reference)

        # add links into the graph
        (row, col) = dic_link.shape
        for index in range(row):
            lk_id = dic_link.iloc[index]['id']
            lk_from = dic_link.iloc[index]['start']
            lk_to = dic_link.iloc[index]['end']
            lk_label = dic_link.iloc[index]['label']

            for idx_label in range(len(self.node_id)):
                if self.node_id[idx_label] == lk_from:
                    label_from = self.node_label[idx_label]
                if self.node_id[idx_label] == lk_to:
                    label_to = self.node_label[idx_label]
                    color = self.node_color[idx_label]

            self.link_id.append(lk_id)
            self.link_from.append(lk_from)
            self.link_to.append(lk_to)
            self.link_label.append(lk_label)
            self.link_from_label.append(label_from)
            self.link_to_label.append(label_to)
            self.link_color.append(color)

            self.model.add_edge(lk_from,lk_to,label=lk_label,id_lk=lk_id)

        # print self.node_size

    def add_node(self, label, feature):

        # generate a random id for a new node
        if feature == 'Central Question':
            id = 'cq'+str(np.random.randint(100000))
        elif feature == 'Question':
            id = 'qd'+str(np.random.randint(100000))
        else:
            id = 'ad'+str(np.random.randint(100000))

        self.node_id.append(id)
        self.node_label.append(label)
        self.node_feature.append(feature)

    def add_link(self, lkfrom, lkto, feature):

        # fundamental link adding function
        self.link_id.append('lk'+str(np.random.randint(100000)))
        self.link_from.append(self.node_id[lkfrom])
        self.link_from_label.append(self.node_label[lkfrom])
        self.link_to.append(self.node_id[lkto])
        self.link_to_label.append(self.node_label[lkto])
        self.link_label.append(feature)

    def add_link_alpha(self, lkfrom, lkto, lkfeature):

        # link creation adding function
        self.link_id.append('lk'+str(np.random.randint(100000)))
        self.link_from.append(lkfrom)
        self.link_to.append(lkto)
        self.link_label.append(lkfeature)

    def add_extrafeature(self, key, content):

        self.node_feature_content.append(content)

    def cor_generate(self):

        print ('node coordinate generation')

        i = 0
        j = 0
        k = 0
        r = 10

        # TODO: add more layout algorithms
        for index in range(len(self.node_id)):

            self.node_cor.append([i,j,k])
            # text.append('node'+str(index))

            i = r * m.sin(1*index)
            j = r * m.cos(1*index)
            if index%6 == 0:
                k = k+10
                r = r+10

        for index in range(len(self.link_id)):

            node_from = self.link_from[index]
            node_to = self.link_to[index]

            for index_node in range(len(self.node_id)):
                if self.node_id[index_node] == node_from:
                    node_from_idx = index_node

            self.link_from_cor.append(self.node_cor[node_from_idx])

            for index_node in range(len(self.node_id)):
                if self.node_id[index_node] == node_to:
                    node_to_idx = index_node

            self.link_to_cor.append(self.node_cor[node_to_idx])

    def create_model(self):
        # generate QN network based on the creation panel

        # other attributes initialization
        self.model = nx.Graph()

        self.node_size = []
        self.node_color = []
        self.node_cor = []
        self.node_content = []

        self.link_from = []
        self.link_to = []
        self.link_from_cor = []
        self.link_to_cor = []
        self.link_color = []

        # set the color map
        color_map = []
        rgb_map = []
        title_name = []

        # fill the QNmodel node attribute
        for index in range(len(self.node_id)):
            if self.node_feature[index] == 'Central question':
                rgb_map.append({'r': 205, 'g': 37, 'b': 38, 'a': 0})
                color_map.append((1,0,0))
                node_size = 1
                title_name = nd_label
            elif self.node_feature[index] == 'Question':
                rgb_map.append({'r': 205, 'g': 137, 'b': 38, 'a': 0})
                color_map.append((0,0,1))
                node_size = 0.7
            else:
                rgb_map.append({'r': 144, 'g': 202, 'b': 249, 'a': 0})
                color_map.append((0,1,0))
                node_size = 0.3

            self.node_color.append(color_map[-1])
            self.node_size.append(node_size)

            # TODO: add the reference and content attribute later
            self.node_content.append('')
            self.node_reference.append('')

            nd_id = self.node_id[index]
            nd_feature = self.node_feature[index]
            nd_content = self.node_content[index]
            nd_label = self.node_label[index]
            nd_reference = self.node_reference[index]

            self.model.add_node(nd_id,feature=nd_feature,content=nd_content,label=nd_label,reference=nd_reference)

        # fill the link attribute
        for index in range(len(self.link_id)):

            lk_id = self.link_id[index]
            lk_label = self.link_label[index]
            lk_from_label = self.link_from_label[index]
            lk_to_label = self.link_to_label[index]

            for idx_label in range(len(self.node_label)):
                if self.node_label[idx_label] == lk_from_label:
                    id_from = self.node_id[idx_label]

                if self.node_label[idx_label] == lk_to_label:
                    id_to = self.node_id[idx_label]
                    color = self.node_color[idx_label]

            self.link_from.append(id_from)
            self.link_to.append(id_to)
            self.link_color.append(color)

            lk_from = self.link_from[index]
            lk_to = self.link_to[index]

            self.model.add_edge(lk_from,lk_to,label=lk_label,id_lk=lk_id)

        # generate the coordinate of the QNmodel
        self.cor_generate()
