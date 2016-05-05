#
#   GHOSTS & Pac-Man
#   By: Hunter Forsyth (c3forsyt) and "Lennox" Shou Hao Ho (g4hoshou)
#
#   Requires python2.7+ and pygame.
#

from math import sqrt

# ---Constants---
WALL = 0
EMPTY = 1
# ---Constants---


'''
Node class. Used to represent blocks in the game map.
'''
class Node:
    def __init__(self, id, neighbours, coord):
        self.id = id
        self.neighbours = neighbours
        self.coord = coord

    def get_id(self):
        return self.id

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def add_neighbour(self, new_neighbour):
        if new_neighbour not in self.neighbours:
            self.neighbours.append(new_neighbour)

    def get_neighbours(self):
        return self.neighbours

    def get_coord(self):
        return self.coord

    def is_neighbour(self, other):
        return other in self.neighbours

    '''
    Returns the straight-line distance between self and other.
    '''
    def distance(self, other):
        x1, y1 = self.coord
        x2, y2 = other.get_coord()
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    def __str__(self):
        return "Node(" + str(self.id) + ")"

    '''
    Hack to print out nicely. Output not actually valid for repr purposes.
    '''
    def __repr__(self):
        return "Node(" + str(self.id) + ")"


'''
Returns the map with the id values replaced by its corresponding Node objects.
Any WALLs will remain in place.

Warning: map will be modified.
'''
def convert_map_to_nodes(map):

    '''
    Add the Node's neighbours.
    '''
    def add_node_neighbours(map, node, xdim, ydim):
        if node == WALL:
            return None

        x, y = node.get_coord()

        #left
        if x != 0 and map[x-1][y] != WALL:
            node.add_neighbour(map[x-1][y])

        #right
        if x != xdim-1 and map[x+1][y] != WALL:
            node.add_neighbour(map[x+1][y])

        #up
        if y != 0 and map[x][y-1] != WALL:
            node.add_neighbour(map[x][y-1])

        #down
        if y != ydim-1 and map[x][y+1] != WALL:
            node.add_neighbour(map[x][y+1])


    #make sure the dimensions are valid.
    lengths = [len(lst) for lst in map]
    assert max(lengths) == min(lengths)
    ydim = lengths[0]
    xdim = len(map)

    #convert all id to nodes first (neighbour lists not yet filled).
    for i in range(xdim):
        for j in range(ydim):
            if map[i][j] == EMPTY:
                map[i][j] = Node(str(i) + "_" + str(j), [], (i, j))

    #fill in the neighbours.
    for i in range(xdim):
        for j in range(ydim):
            add_node_neighbours(map, map[i][j], xdim, ydim)

    return map


'''
Given path (list of Nodes), return the next move (direction).
'''
def gimme_direction(journey):
    #realistically, journey cannot be <= 0
    if len(journey) < 2:
        #Why are you calling this??? you already caught the User!
        return None

    current = journey[0].get_coord()
    next = journey[1].get_coord()

    if current[0] < next[0]:
        return "down"
    elif current[0] > next[0]:
        return "up"
    elif current[1] < next[1]:
        return "right"
    elif current[1] > next[1]:
        return "left"
    else:
        return None