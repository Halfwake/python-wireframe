import pygame
from pygame.locals import *

import wireframe

TITLE = 'Wireframe Test'
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class ProjectionViewer(object):
    def __init__(self):
        self.wireframes = {}
        self.show_nodes = True
        self.show_edges = True
        self.node_color = (255, 255, 255)
        self.edge_color = (200, 200, 200)
        self.node_radius = 4
    def translate_all(self, vector):
        matrix = wireframe.translation_matrix(*vector)
        for _wireframe in self.wireframes.itervalues():
            _wireframe.translate(matrix)
    def rotate_all(self, axis, theta):
        for wireframe in self.wireframes.itervalues():
            center = wireframe.find_center()
            wireframe.rotate(axis, center, theta)
    def scale_all(self, scale):
        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2
        for wireframe in self.wireframes.itervalues():
            wireframe.scale((center_x, center_y), scale)
    def draw(self, screen):
        for wireframe in self.wireframes.values():
            if self.show_edges:
                for start_node, end_node in wireframe.edges:
                    pygame.draw.aaline(
                        screen,
                        self.edge_color,
                        wireframe.nodes[start_node][:2],
                        wireframe.nodes[end_node][:2],
                        1,
                    )
            if self.show_nodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(
                        screen,
                        self.node_color,
                        (int(node[0]), int(node[1])),
                        self.node_radius,
                        0)
    def add_wireframe(self, name, wireframe):
        self.wireframes[name] = wireframe

key_to_function = {
    K_LEFT : lambda x : x.translate_all([-10, 0, 0]),
    K_RIGHT : lambda x : x.translate_all([10, 0, 0]),
    K_DOWN : lambda x : x.translate_all([0, 10, 0]),
    K_UP : lambda x : x.translate_all([0, -10, 0]),
    K_EQUALS : lambda x : x.scale_all(1.25),
    K_MINUS : lambda x : x.scale_all(0.8),

    K_q : lambda x : x.rotate_all('x',  0.1),
    K_w : lambda x : x.rotate_all('x', -0.1),
    K_a : lambda x : x.rotate_all('y',  0.1),
    K_s : lambda x : x.rotate_all('y', -0.1),
    K_z : lambda x : x.rotate_all('z',  0.1),
    K_x : lambda x : x.rotate_all('z', -0.1),
}
    
if __name__ == '__main__':
    background = (10, 50, 50)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    projection_viewer = ProjectionViewer()
    projection_viewer.add_wireframe('test_cube1', wireframe.Cube(100, 200))
    projection_viewer.add_wireframe('test_cube2', wireframe.Cube(150, 250))
    #projection_viewer.wireframes['test_cube'].translate('x', 250)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key in key_to_function:
                    key_to_function[event.key](projection_viewer)
        screen.fill(background)
        projection_viewer.draw(screen)
        pygame.display.flip()
    
        
