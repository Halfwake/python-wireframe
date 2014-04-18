import math

import numpy

def translation_matrix(dx = 0, dy = 0, dz = 0):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])

def scale_matrix(sx = 0, sy = 0, sz = 0):
    return numpy.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1],
    ])

def rotate_matrix_x(radians):
    c = numpy.cos(radians)
    s = numpy.sin(radians)
    return numpy.array([
        [1, 0, 0, 0],
        [0, c,-s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1],
    ])

def rotate_matrix_y(radians):
    c = numpy.cos(radians)
    s = numpy.sin(radians)
    return numpy.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1],
    ])

def rotate_matrix_z(radians):
    c = numpy.cos(radians)
    s = numpy.sin(radians)
    return numpy.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def rotate_matrix(axis, radians):
    assert axis in 'x y z'.split(), '%s is not a valid axis!' % (axis,)
    if axis == 'x':
        pass
    elif axis == 'y':
        pass
    elif axis == 'z':
        pass
    
def _repr_node(node):
    return '(%.2f, %.2f, %.2f)' % (node[0], node[1], node[2])
        
def _repr_edge(edge):
    start, stop = edge
    return '%s TO %s'  % (start, stop)

class Wireframe(object):
    def __init__(self):
        self.nodes = numpy.zeros((0, 4))
        self.edges = []
    def add_nodes(self, new_nodes):
        ones_column = numpy.ones((len(new_nodes), 1))
        ones_added = numpy.hstack((new_nodes, ones_column))
        self.nodes = numpy.vstack((self.nodes, ones_added))
    def add_edges(self, new_edges):
        self.edges.extend(new_edges)
    def _repr_nodes(self):
        buff = ['\n --- Nodes --- ']
        for i, node in enumerate(self.nodes):
            buff.append(' %d: %s' % (i, _repr_node(node),))
        return '\n'.join(buff)
    def translate(self, matrix):
        self.nodes = numpy.dot(self.nodes, matrix)
    def transform(self, vector):
        matrix = translation_matrix(*vector)
        self.nodes = numpy.dot(self.nodes, matrix)
    def scale(self, center, scale):
        center_x, center_y = center
        for node in self.nodes:
            node.x = center_x + scale * (node.x - center_x)
            node.y = center_y + scale * (node.y - center_y)
            node.z *= scale
    def find_center(self):
        num_nodes = len(self.nodes)
        mean_x = sum([node[0] for node in self.nodes]) / num_nodes
        mean_y = sum([node[1] for node in self.nodes]) / num_nodes
        mean_z = sum([node[2] for node in self.nodes]) / num_nodes
        return mean_x, mean_y, mean_z
    def rotate(self, axis, center, radians):
        assert axis in 'x y z'.split(), '%s is not a valid axis!' % (axis,)
        func = 'rotate_' + axis
        getattr(self, func)(center, radians)
    def rotate_x(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            y = node[1] - cy
            z = node[2] - cz
            d = numpy.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node[2] = cz + d * numpy.cos(theta)
            node[1] = cy + d * numpy.sin(theta)

    def rotate_y(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node[0] - cx
            z = node[2] - cz
            d = numpy.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node[2] = cz + d * numpy.cos(theta)
            node[0] = cx + d * numpy.sin(theta)
    def rotate_z(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node[0] - cx
            y = node[1] - cy
            d = numpy.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node[0] = cx + d * numpy.cos(theta)
            node[1] = cy + d * numpy.sin(theta)
    def _repr_edges(self):
        buff = ['\n --- Edges --- ']
        for i, edge in enumerate(self.edges):
            buff.append(' %d: %s' % (i, _repr_edge(edge),))
        return '\n'.join(buff)
    def __repr__(self, amount = 400):
        half_amount = amount / 2
        return '\n'.join([self._repr_nodes()[:half_amount], self._repr_edges()[:half_amount]])

class Cube(Wireframe):
    def __init__(self, x, y):
        pos = (x, y)
        super(Cube, self).__init__()
        cube_nodes = [(x, y, z) for x in pos for y in pos for z in pos]
        self.add_nodes(cube_nodes)
        cube_edges = [(n, n + 4) for n in range(0, 4)]
        cube_edges.extend([(n, n + 1) for n in range(0, 8, 2)])
        cube_edges.extend([(n, n + 2) for n in (0, 1, 4, 5)])
        cube_edges = numpy.array(cube_edges)
        self.add_edges(cube_edges)
        
if __name__ == '__main__':
    cube = Cube(10, 10)
    
