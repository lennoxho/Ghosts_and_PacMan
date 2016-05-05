#
#   GHOSTS & Pac-Man
#   By: Hunter Forsyth (c3forsyt) and "Lennox" Shou Hao Ho (g4hoshou)
#
#   Requires python2.7+ and pygame.
#

from node_class import *
from operator import itemgetter
from cProfile import run
from collections import defaultdict

#---globals---
mini_max_cache = defaultdict(lambda: None)
#---globals---


'''
Returns the miniMax path and its value (distance).

during the first call to mini_max, alpha should be set to -float('Inf'),
beta set to float('Inf')
'''
def mini_max(node, target_node, steps, min_or_max, alpha, beta):
    assert steps >= 0

    #leaf, just compute distance.
    if steps == 0:
        global mini_max_cache

        pattern = (id(node), id(target_node))
        if mini_max_cache[pattern] is None:
            dist = node.distance(target_node)
            mini_max_cache[pattern] = dist
            return dist, [], []

        else:
            return mini_max_cache[pattern], [], []

    else:
        #currently trying to minimize distance. Ghost's turn.
        if min_or_max == "min":
            #staying in place is also an option.
            value, ghost_path, player_path = mini_max(node, target_node, steps-1, "max", alpha, beta)
            #the return path does not matter since -float('Inf') is below the minimum distance anyway
            if value < alpha:
                return -float('Inf'), [], []

            candidates = [(value, ghost_path, player_path)]
            beta = value
            for n in node.get_neighbours():
                value, ghost_path, player_path = mini_max(n, target_node, steps-1, "max", alpha, beta)
                if value < alpha:
                    return -float('Inf'), [], []

                candidates.append((value, ghost_path, player_path))
                if value < beta:
                    beta = value

            min_value, ghost_path, player_path = min(candidates, key=itemgetter(0))

            return min_value, [node] + ghost_path, player_path

        #currently trying to maximize distance. Player's turn.
        else:
            value, ghost_path, player_path = mini_max(node, target_node, steps-1, "min", alpha, beta)
            if value > beta:
                return float('Inf'), [], []

            candidates = [(value, ghost_path, player_path)]
            alpha = value
            for n in target_node.get_neighbours():
                value, ghost_path, player_path = mini_max(node, n, steps-1, "min", alpha, beta)
                if value > beta:
                    return float('Inf'), [], []

                candidates.append((value, ghost_path, player_path))
                if value > alpha:
                    alpha = value

            max_value, ghost_path, player_path = max(candidates, key=itemgetter(0))

            return max_value, ghost_path, [target_node] + player_path