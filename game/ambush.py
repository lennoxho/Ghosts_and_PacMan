#
#   GHOSTS & Pac-Man
#   By: Hunter Forsyth (c3forsyt) and "Lennox" Shou Hao Ho (g4hoshou)
#
#   Requires python2.7+ and pygame.
#

from node_class import *
from bfs import depth_limited_bfs, multiple_target_bfs

# ---Constants---
ambush_points = {   1: [(7, 4), (7, 8), (4, 9)],
                    2: [(7, 10), (7, 14), (4, 9)],
                    3: [(13, 4), (13, 6), (16, 9), (20, 9)],
                    4: [(13, 12), (13, 14), (16, 9), (20, 9)]   }
# ---Constants---


'''
Return the sector the coord is in.

WARNING: hard-coded goodness! :) /s
'''
def in_sector(coord):
    x, y = coord

    if x < 7 and y < 9:
        return 1

    elif x < 7 and y > 9:
        return 2

    elif x > 13 and y < 9:
        return 3

    elif x > 13 and y > 9:
        return 4

    #coord is not in any of the sectors.
    else:
        return None


'''
Figure out a configuration for the ghosts to ambush points.
If not possible, return False.
'''
def organize_ambush(distance_to_beat, ghosts, ambush_coords):
    if len(ambush_coords) == 1:
        target_coord = ambush_coords[0]
        for ghost in ghosts:
            ret = depth_limited_bfs(ghost, [target_coord], distance_to_beat)
            if ret != None:
                return [(ghost, ret[0])]

        return False

    else:
        target_coord = ambush_coords[0]
        for ghost in ghosts:
            ret = depth_limited_bfs(ghost, [target_coord], distance_to_beat)
            if ret != None:
                sub_configuration = organize_ambush(distance_to_beat, [g for g in ghosts if g is not ghost], ambush_coords[1:])

                if sub_configuration != False:
                    return [(ghost, ret[0])] + sub_configuration

        return False


'''
Figure out if ambush is possible. If so, return the configuration.
Otherwise, return False.
'''
def ambush(player, ghosts):
    sector = in_sector(player.get_coord())

    #No ambush opportunity
    if sector is None:
        return False

    ambush_coords = ambush_points[sector]
    path = multiple_target_bfs(player, ambush_coords)
    assert path is not None

    #not counting current node
    distance_to_beat = len(path[0]) - 1
    configuration = organize_ambush(distance_to_beat, ghosts, ambush_coords)

    if configuration == False:
        return False

    return distance_to_beat, ambush_coords, configuration