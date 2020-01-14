import os
os.environ['ETS_TOOLKIT'] = 'qt4'

import numpy as np
from mayavi import mlab

import calculate as calc

BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)


class MPlot3D():
    def __init__(self, mlab=None, scale=1.0):
        self.scale = scale

        self.obj_node = []
        self.obj_link = []
        self.obj_nodetext = []
        self.obj_linktext = []

        if mlab is None:
            self._new_figure()

    def draw_node(self, node_cor):

        point_area = np.array(node_cor)

        # print point_area

        point_x = point_area[:,0]
        point_y = point_area[:,1]
        point_z = point_area[:,2]
        # print point_x
        # print float(point_z)

        self.obj_node.append(mlab.points3d(point_x, point_y, point_z, color=(1, 0, 0),
                    resolution=20, scale_factor = 0.8))

        mlab.show()

    def draw_link(self, link_from, link_to):

        point_from = np.array(link_from)
        point_to = np.array(link_to)

        from_x = point_from[:,0]
        from_y = point_from[:,1]
        from_z = point_from[:,2]
        to_x = point_to[:,0]
        to_y = point_to[:,1]
        to_z = point_to[:,2]

        for index in range(len(from_x)):
            self.obj_link.append(mlab.plot3d([from_x[index],to_x[index]],
                                             [from_y[index],to_y[index]],
                                             [from_z[index],to_z[index]],
                                             color = (0,0,1), tube_radius = 0.1))

        # mlab.show()

        print ('obj_node')
        print (self.obj_node)

    def draw_nodelabel(self, node_cor, node_label):

        node_cor = np.array(node_cor)
        point_x = node_cor[:,0]
        point_y = node_cor[:,1]
        point_z = node_cor[:,2]

        for index in range(len(node_cor)):
            self.obj_nodetext.append(mlab.text3d(point_x[index]+0.3, point_y[index]+0.3, point_z[index]+0.3,
                                    node_label[index], line_width = 1.0))

        # print 'obj_nodetext'
        # print self.obj_nodetext

    def draw_linklabel(self, link_from, link_to, label):

        from_cor = np.array(link_from)
        to_cor = np.array(link_to)
        point_x = 0.5*(from_cor[:,0]+to_cor[:,0])
        point_y = 0.5*(from_cor[:,1]+to_cor[:,1])
        point_z = 0.5*(from_cor[:,2]+to_cor[:,2])

        for index in range(len(link_from)):
            self.obj_linktext.append(mlab.text3d(point_x[index], point_y[index], point_z[index],
                                    label[index], line_width = 0.8))

    def draw_node_alfa(self, cor, color, size):

        point_area = np.array(cor)

        # print point_area

        point_x = point_area[:,0]
        point_y = point_area[:,1]
        point_z = point_area[:,2]
        color = np.array(color)
        size = np.array(size)
        # print point_x
        # print float(point_z)
        print ('cor color and size ')
        print (type(point_x))
        print (type(color))
        print (type(size))
        print (point_x)
        print (color)
        print (size)

        node_obj = mlab.points3d(point_x, point_y, point_z,resolution=20, scale_factor = 1)

        # node_obj = mlab.points3d(point_x, point_y, point_z, node_size)

        # node_obj.glyph.color_mode = 'color_by_vector'
        # node_obj.mlab_source.dataset.point_data.vectors = color

        node_obj.glyph.scale_mode = 'scale_by_vector'
        # node_obj.mlab_source.dataset.point_data.vectors = color
        node_obj.mlab_source.dataset.point_data.scalars = size

        self.obj_node.append(node_obj)

        # print 'obj_node'
        # print self.obj_node

    def draw_link_alfa(self, linkfrom, linkto, color, status_arrow):

        point_from = np.array(linkfrom)
        point_to = np.array(linkto)

        print (point_from)
        print (type(point_from))
        # print point[:,0]

        from_x = point_from[:,0]
        from_y = point_from[:,1]
        from_z = point_from[:,2]
        to_x = point_to[:,0]
        to_y = point_to[:,1]
        to_z = point_to[:,2]
        vec_x = point_to[:,0] - point_from[:,0]
        vec_y = point_to[:,1] - point_from[:,1]
        vec_z = point_to[:,2] - point_from[:,2]

        if status_arrow:
            for index in range(len(from_x)):
                self.obj_link.append(mlab.quiver3d(from_x[index], from_y[index], from_z[index],
                                    vec_x[index], vec_y[index], vec_z[index],
                                    color = color[index], mode='2darrow', scale_factor=1, line_width=0.1))
        else:
                for index in range(len(from_x)):
                    self.obj_link.append(mlab.plot3d([from_x[index],to_x[index]],
                                                     [from_y[index],to_y[index]],
                                                     [from_z[index],to_z[index]],
                                                     color = (0,0,1), tube_radius = 0.1))

        # mlab.show()

        print ('obj_node')
        print (self.obj_node)


    def get_gcf(self):
        return mlab.gcf()

    def get_currentView(self):
        return mlab.view()




    def set_curentView(self,current_view):
        mlab.view(*current_view)

    def _new_figure(self):
        mlab.figure(1, size=(800, 600), bgcolor=BLACK, fgcolor=WHITE)

    def _new_figure_alfa(self):
        fig_handler = mlab.figure(1, size=(800, 600), bgcolor=BLACK, fgcolor=WHITE)
        mlab.show()
        return fig_handler

    def draw_arrow(self, arrow, color=RED, scale=10):
        pnt, vec = arrow
        # scale = self.scale * scale
        mlab.quiver3d(pnt[0], pnt[1], pnt[2], vec[0], vec[1], vec[2],
                      color=color, mode='arrow', scale_factor=self.scale)

    def draw_frame(self, pose, scale=10, label=''):
        R, t = pose
        scale = self.scale * scale
        clr = [RED, GREEN, BLUE]
        vecs = R[:, 0], R[:, 1], R[:, 2]
        for k in range(3):
            mlab.quiver3d(t[0], t[1], t[2], vecs[k][0], vecs[k][1], vecs[k][2],
                          color=clr[k], mode='arrow', scale_factor=scale)
        mlab.text3d(t[0], t[1], t[2], label, scale=scale/5)

    def draw_frames(self, points, frames, scale=10):
        scale = self.scale * scale
        clr = [RED, GREEN, BLUE]
        vectors = [[], [], []]
        for frame in frames:
            vectors[0].append(frame[:, 0])
            vectors[1].append(frame[:, 1])
            vectors[2].append(frame[:, 2])
        vectors[0] = np.array(vectors[0])
        vectors[1] = np.array(vectors[1])
        vectors[2] = np.array(vectors[2])
        for k in range(3):
            mlab.quiver3d(points[:, 0], points[:, 1], points[:, 2],
                          vectors[k][:, 0], vectors[k][:, 1], vectors[k][:, 2],
                          color=clr[k], mode='arrow', scale_factor=scale)

    def draw_transformation(self, matrix1, matrix2, label1='', label2=''):
        self.draw_frame(calc.matrix_to_pose(matrix1), label=label1)
        self.draw_frame(calc.matrix_to_pose(matrix2), label=label2)
        self.draw_line(calc.matrix_to_pose(matrix1)[1],
                       calc.matrix_to_pose(matrix2)[1])

    def draw_plane(self, plane, points3d, color=(1, 0.1, 0)):
        # a plane is a*x+b*y+c*z+d=0
        # [a,b,c] is the normal. Thus, we have to calculate d and we're set
        a, b, c, d = plane
        #xmin, xmax = int(np.min(points3d[:,0])), int(np.max(points3d[:,0]))
        #ymin, ymax = int(np.min(points3d[:,1])), int(np.max(points3d[:,1]))
        ymin, ymax = -0.1, 0.1
        zmin, zmax = 0, 1.5 * np.max(points3d[:, 2])
        #x, z = np.mgrid[xmin:xmax:10, 0:500:10]
        #y = (a * x + c * z + d) / -b
        y, z = np.mgrid[ymin:ymax:0.09, zmin:zmax:0.09]
        x = (b * y + c * z + d) / -a
        print (x, y, z)
        mlab.mesh(x, y, z, color=color, opacity=0.5, transparent=True)

    def draw_line(self, point0, point1, color=WHITE, scale=0.25):
        scale = self.scale * scale
        mlab.plot3d([point0[0], point1[0]], [point0[1], point1[1]],
                    [point0[2], point1[2]], color=color, tube_radius=scale)

    def draw_point(self, point, color=WHITE, scale=1):
        scale = self.scale * scale
        mlab.points3d(point[0], point[1], point[2],
                      color=color, scale_factor=scale)  # , mode='cube')

    def draw_points(self, points3d, color=WHITE, scale=1):
        scale = self.scale * scale
        mlab.points3d(points3d[:, 0], points3d[:, 1], points3d[:, 2],
                      color=color, scale_factor=scale)  # , mode='cube')

    def draw_cloud(self, points3d, scale=1):
        scale = self.scale * scale
        mlab.points3d(points3d[:, 0], points3d[:, 1],
                      points3d[:, 2], points3d[:, 2],
                      colormap='jet', opacity=0.75, scale_factor=scale)
        mlab.outline()
        mlab.colorbar(title='Planar disparity (mm)')
        mlab.axes()

    def draw_lines(self, points3d, color=WHITE, scale=0.1):
        scale = self.scale * scale
        mlab.plot3d(points3d[:, 0], points3d[:, 1], points3d[:, 2], color=color, tube_radius=scale)

    def clear(self):
        mlab.clf()
        # self._new_figure()

    def show(self):
        mlab.show()
