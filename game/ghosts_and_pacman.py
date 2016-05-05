#
#   GHOSTS & Pac-Man
#   By: Hunter Forsyth (c3forsyt) and "Lennox" Shou Hao Ho (g4hoshou)
#
#   Requires python2.7+ and pygame.
#

import pygame
import time
import sys
from node_class import *
from bfs import *
from mini_Max import *
from ambush import *

# Config ----------------------------------------------------------------------

MINIMAX_SEARCH_DEPTH = 9    # Default minimax search depth, used only if
                            # not specified at launch with --minimax-depth

UPDATE_TIME = 200   # In milliseconds. (Eg. UPDATE_TIME = 200 is 5fps)
                    # Specify in increments of 50,
                    # fastest update time is 100.

SHOW_SEARCH_PATHS = True  # Overlay the graph search paths on the board
                          # in real time.

# -----------------------------------------------------------------------------

# Colors
BG_COLOR = 0,0,0
EMPTY_COLOR = 0,0,0
WALL_COLOR = 0,0,255
SEARCH_PATH_COLOR = 20,60,20
PLAYER_PATH_COLOR = 60,20,20
PACMAN_COLOR = 244,233,14
GHOST1_COLOR = 242,23,35
GHOST2_COLOR = 245,150,178
GHOST3_COLOR = 20,173,230
GHOST4_COLOR = 247,129,28

# Game board (for display only):
WALL = 0
EMPTY = 1
PACMAN = 2
GHOST1 = 3
GHOST2 = 4
GHOST3 = 5
GHOST4 = 6
SEARCH_PATH = 14
PLAYER_PATH = 15
GAME_BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Other constants:
DIR_RIGHT = 7
DIR_LEFT = 8
DIR_UP = 9
DIR_DOWN = 10
STRATEGY_BFS = 11
STRATEGY_MINIMAX = 12
STRATEGY_AMBUSH = 13
STRATEGY_MINIMAX_BFS = 14
BLOCK_SIZE = 20

# Setup
pygame.init()
font = pygame.font.SysFont(None, 24)
fontBig = pygame.font.SysFont(None, 34)
size = width, height = 720, 480
screen = pygame.display.set_mode(size)
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Ghosts & Pac-Man")


# Vars
lastKey = None
startOffset = 0
pacmanCoords = [9,12]
ghostCoords = [[9,9],
               [9,10],
               [8,10],
               [10,10]]
searchGraph = None
searchStrat = STRATEGY_BFS
dead = 0
ambushing = False
renderBoard = [row[:] for row in GAME_BOARD]
ambushPath = []
paused = True


""" Reset game variables, called on game over. """
def restart():
    global lastKey, startOffset, pacmanCoords, ghostCoords, ambushing, paused
    ambushing = False
    lastKey = None
    paused = True
    startOffset = 0
    pacmanCoords = [9,12]
    ghostCoords = [[9,9],
               [9,10],
               [8,10],
               [10,10]]


""" Game engine. """
def pacman():
    global lastKey, searchGraph, startOffset, searchStrat, paused, MINIMAX_SEARCH_DEPTH

    justChangedStrat = False
    justPaused = False
    lastTick = 0

    def printInvalidArgs():
        print("Invalid arguments.")
        print("Usage is ghosts_and_pacman.py [--search-depth=d]")

    # Check arguments:
    if len(sys.argv) > 2:
        printInvalidArgs()
        return
    if len(sys.argv) > 1:
        if "--minimax-depth=" in sys.argv[1] and len(sys.argv[1]) > 16:
            split = sys.argv[1].split("=")
            if len(split) != 2:
                printInvalidArgs()
                return
            try:
                depth = int(split[1])
            except ValueError:
                printInvalidArgs()
                return
            MINIMAX_SEARCH_DEPTH = depth
        else:
            printInvalidArgs()
            return

    # Check parameters:
    if UPDATE_TIME%50 != 0 or UPDATE_TIME < 100:
        print("Invalid update time.")
        return
    if MINIMAX_SEARCH_DEPTH < 3:
        print("Minimax search depth too small, minimum is 3.")
        return
    if MINIMAX_SEARCH_DEPTH > 15:
        print("Minimax search depth is very large, performance will be bad.")

    # Initialize the search graph:
    searchGraph = convert_map_to_nodes([row[:] for row in GAME_BOARD])

    while 1: # Engine loop

        # Quit on close or esc key:
        keysDown = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if keysDown[pygame.K_ESCAPE]:
            return

        # Get control keys:
        if keysDown[pygame.K_RIGHT]:
            lastKey = pygame.K_RIGHT
        if keysDown[pygame.K_LEFT]:
            lastKey = pygame.K_LEFT
        if keysDown[pygame.K_UP]:
            lastKey = pygame.K_UP
        if keysDown[pygame.K_DOWN]:
            lastKey = pygame.K_DOWN

        # Change AI strategy:
        if keysDown[pygame.K_s] and not justChangedStrat:
            justChangedStrat = True
            if searchStrat == STRATEGY_BFS:
                searchStrat = STRATEGY_MINIMAX
            elif searchStrat == STRATEGY_MINIMAX:
                searchStrat = STRATEGY_MINIMAX_BFS
            elif searchStrat == STRATEGY_MINIMAX_BFS:
                searchStrat = STRATEGY_AMBUSH
            elif searchStrat == STRATEGY_AMBUSH:
                searchStrat = STRATEGY_BFS
            render()
        elif not keysDown[pygame.K_s]:
            justChangedStrat = False

        # Pause the game:
        if keysDown[pygame.K_p] and not justPaused:
            justPaused = True
            paused = not paused
        elif not keysDown[pygame.K_p]:
            justPaused = False

        # Update:
        if time.time()*1000 > lastTick + UPDATE_TIME:
            lastTick = time.time()*1000
            gameloop()
            lastKey = None
            startOffset += 1
        else:
            time.sleep(0.05)


""" Main gameloop. """
def gameloop():
    clearSearchPaths()
    global dead
    if dead > 0:
        dead -= 1
        if dead == 0:
            restart()
    else:
        if not paused:
            logic()
    render()


""" Main game logic. """
def logic():
    global lastKey, searchGraph, startOffset, dead, ambushing, ambushPath

    # Game over detection:
    for ghost in range(4):
        if ghostCoords[ghost] == pacmanCoords:
            dead = round(1000 / UPDATE_TIME) # Show game over screen for one second.

    # Player movement:
    if lastKey == pygame.K_RIGHT:
        movePacman(DIR_RIGHT)
    elif lastKey == pygame.K_LEFT:
        movePacman(DIR_LEFT)
    elif lastKey == pygame.K_UP:
        movePacman(DIR_UP)
    elif lastKey == pygame.K_DOWN:
        movePacman(DIR_DOWN)

    # Ghost movement:
    searchBoard = [row[:] for row in GAME_BOARD]
    ghostsToMove = 1
    if startOffset > 4:
        ghostsToMove = 2
    if startOffset > 8:
        ghostsToMove = 3
    if startOffset > 12:
        ghostsToMove = 4

    # === AI CODE BELOW =======================================:
    if searchStrat == STRATEGY_BFS or searchStrat == STRATEGY_MINIMAX or searchStrat == STRATEGY_MINIMAX_BFS:
        ambushing = False
        for ghost in range(ghostsToMove): # Move each ghost individually.
            dir = None

            if searchStrat == STRATEGY_BFS: # BFS STRATEGY

                # Run BFS.
                dir = BFSHelper(ghost)

            elif searchStrat == STRATEGY_MINIMAX: # MINIMAX STRATEGY

                # Run minimax strategy:
                search = mini_max(searchGraph[ghostCoords[ghost][1]][ghostCoords[ghost][0]],
                 searchGraph[pacmanCoords[1]][pacmanCoords[0]], MINIMAX_SEARCH_DEPTH, "min", -float('Inf'), float('Inf'))
                if search and len(search) == 3:
                    dir = convertDirFormat(gimme_direction(search[1]))
                    addSearchPath(search[1], SEARCH_PATH)
                    addSearchPath(search[2], PLAYER_PATH)

            elif searchStrat == STRATEGY_MINIMAX_BFS: # MINIMAX + BFS STRATEGY

                # Run minimax strategy if player is within straight-line distance 0.5*MINIMAX_SEARCH_DEPTH.
                if searchGraph[ghostCoords[ghost][1]][ghostCoords[ghost][0]]\
                 .distance(searchGraph[pacmanCoords[1]][pacmanCoords[0]]) < 0.5*MINIMAX_SEARCH_DEPTH:
                    search = mini_max(searchGraph[ghostCoords[ghost][1]][ghostCoords[ghost][0]],
                     searchGraph[pacmanCoords[1]][pacmanCoords[0]], MINIMAX_SEARCH_DEPTH, "min", -float('Inf'), float('Inf'))
                    if search and len(search) == 3:
                        dir = convertDirFormat(gimme_direction(search[1]))
                        addSearchPath(search[1], SEARCH_PATH)
                        addSearchPath(search[2], PLAYER_PATH)

                # If not, run BFS.
                else:
                    dir = BFSHelper(ghost)

            # Direction has been determined, move the ghost
            moveGhost(dir, ghost + 1)

    elif searchStrat == STRATEGY_AMBUSH: # AMBUSH STRATEGY
                                         # Uses BFS, except when it is possible to block the player in.
                                         # Moves all ghosts together.
        ghostNodes = [
            searchGraph[ghostCoords[0][1]][ghostCoords[0][0]],
            searchGraph[ghostCoords[1][1]][ghostCoords[1][0]],
            searchGraph[ghostCoords[2][1]][ghostCoords[2][0]],
            searchGraph[ghostCoords[3][1]][ghostCoords[3][0]]
        ]

        # Currently not attempting to ambush, so check if possible to, and
        # if not, run BFS.
        if not ambushing:

            # Generate the path (determine if it's possible to ambush):
            search = ambush(searchGraph[pacmanCoords[1]][pacmanCoords[0]], ghostNodes)

            # It is possible to start ambushing:
            if search != False:

                # Parse the path:
                ambushing = True
                distance_to_beat, ambush_coords, configuration = search
                ambushPath = [None] * len(ghostNodes)
                for i in range(len(configuration)):
                    for j in range(len(ghostNodes)):
                        if ghostNodes[j].get_coord() == configuration[i][0].get_coord():
                            ambushPath[j] = configuration[i][1]

                # Move the ghosts:
                ambushPathFollowerHelper()

                # Update the path:
                ambushPathUpdaterHelper()

            # Can't ambush yet, run BFS:
            else:
                ambushing = False
                for ghost in range(ghostsToMove):
                    dir = BFSHelper(ghost)
                    moveGhost(dir, ghost + 1)

        # Currently attempting to ambush, continue moving all ghosts along their paths:
        else:

            # Move the ghosts:
            ambushPathFollowerHelper()

            # Update the path:
            ambushPathUpdaterHelper()

    # === AI CODE ABOVE =======================================:


""" Compute and paint everything to the screen. """
def render():
    screen.fill(BG_COLOR)

    # Title text::
    screen.blit(fontBig.render("Ghosts & Pac-Man", 1, (255,255,255)), (410, 30))

    # Strategy text:
    strategy = ""
    if (searchStrat == STRATEGY_BFS):
        strategy = "BFS"
    elif (searchStrat == STRATEGY_MINIMAX):
        strategy = "Minimax"
    elif (searchStrat == STRATEGY_AMBUSH):
        strategy = "Ambush heuristic"
    elif (searchStrat == STRATEGY_MINIMAX_BFS):
        strategy = "Minimax + BFS"
    screen.blit(font.render("Ghosts using search strategy:", 1, (255,255,255)), (410, 70))
    screen.blit(font.render(strategy, 1, (60,255,60)), (410, 90))
    screen.blit(font.render("Press 'S' to change strategy.", 1, (255,255,255)), (410, 140))
    if searchStrat == STRATEGY_AMBUSH:
        if ambushing:
            screen.blit(font.render("(Attempting to block player)", 1, (255,50,50)), (410, 110))
        else:
            screen.blit(font.render("(Currently using BFS)", 1, (50,255,50)), (410, 110))

    # Pause text:
    if paused:
        screen.blit(font.render("Press 'P' to unpause.", 1, (255,255,50)), (410, 170))
        screen.blit(font.render(">>> Paused <<<", 1, (255,255,50)), (410, 190))
    else:
        screen.blit(font.render("Press 'P' to pause.", 1, (255,255,255)), (410, 170))

    # Info text:
    screen.blit(font.render("Update rate: " + str(UPDATE_TIME) + "ms (" + str(1000/UPDATE_TIME) + "fps)", 1, (120,120,120)), (410, 340))
    screen.blit(font.render("Show search paths: " + str(SHOW_SEARCH_PATHS), 1, (120,120,120)), (410, 360))
    screen.blit(font.render("Minimax search depth: " + str(MINIMAX_SEARCH_DEPTH), 1, (120,120,120)), (410, 380))
    screen.blit(font.render("Use the arrow keys to move.", 1, (255,255,50)), (410, 400))
    screen.blit(font.render("Press 'Esc' to quit.", 1, (255,255,50)), (410, 420))

    # Game board:
    if not dead:
        # Fill in player positions:
        renderBoard[pacmanCoords[1]][pacmanCoords[0]] = PACMAN
        renderBoard[ghostCoords[0][1]][ghostCoords[0][0]] = GHOST1
        renderBoard[ghostCoords[1][1]][ghostCoords[1][0]] = GHOST2
        renderBoard[ghostCoords[2][1]][ghostCoords[2][0]] = GHOST3
        renderBoard[ghostCoords[3][1]][ghostCoords[3][0]] = GHOST4

        # Render the game board:
        for y in range(len(renderBoard)):
            for x in range(len(renderBoard[0])):
                renderColor = EMPTY_COLOR
                if renderBoard[y][x] == EMPTY:
                    renderColor = EMPTY_COLOR
                elif renderBoard[y][x] == WALL:
                    renderColor = WALL_COLOR
                elif renderBoard[y][x] == SEARCH_PATH:
                    renderColor = SEARCH_PATH_COLOR
                elif renderBoard[y][x] == PLAYER_PATH:
                    renderColor = PLAYER_PATH_COLOR
                elif renderBoard[y][x] == PACMAN:
                    renderColor = PACMAN_COLOR
                elif renderBoard[y][x] == GHOST1:
                    renderColor = GHOST1_COLOR
                elif renderBoard[y][x] == GHOST2:
                    renderColor = GHOST2_COLOR
                elif renderBoard[y][x] == GHOST3:
                    renderColor = GHOST3_COLOR
                elif renderBoard[y][x] == GHOST4:
                    renderColor = GHOST4_COLOR

                pygame.draw.rect(screen, renderColor,
                     (10 + (x * BLOCK_SIZE), 10 + (y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))
    else:
        # Game over text:
        screen.blit(font.render("Game Over", 1, (255,255,255)), (160, 200))

    pygame.display.flip()


# HELPER FUNCTIONS BELOW:

""" Helper that updates pacman's coords if applicable based on direction. """
def movePacman(direction):
    global pacmanCoords
    genericMove(direction, pacmanCoords)

""" Helper that updates ghostNum's coords if applicable based on direction.
    ghostNum is in [1,4].
"""
def moveGhost(direction, ghostNum):
    global ghostCoords
    coords = None
    if ghostNum == 1:
        coords = ghostCoords[0]
    elif ghostNum == 2:
        coords = ghostCoords[1]
    elif ghostNum == 3:
        coords = ghostCoords[2]
    elif ghostNum == 4:
        coords = ghostCoords[3]
    genericMove(direction, coords)

""" Helper to move a generic set of coords in a direction if applicable.
    coords is of the form [x,y].
"""
def genericMove(direction, coords):
    if direction == None:
        return
    if direction == DIR_RIGHT:
        if coords == [18,10]: # Warp
            coords[0] = 0
            coords[1] = 10
        elif coords[0] + 1 < len(GAME_BOARD[0]) and \
         GAME_BOARD[coords[1]][coords[0] + 1] == 1 and \
         not ghostAtCoords([coords[0] + 1, coords[1]]):
            coords[0] += 1
    elif direction == DIR_LEFT:
        if coords == [0,10]: # Warp
            coords[0] = 18
            coords[1] = 10
        elif coords[0] - 1 >= 0 and \
         GAME_BOARD[coords[1]][coords[0] - 1] == 1 and \
         not ghostAtCoords([coords[0] - 1, coords[1]]):
            coords[0] -= 1
    elif direction == DIR_DOWN:
        if coords[1] + 1 < len(GAME_BOARD) and \
         GAME_BOARD[coords[1] + 1][coords[0]] == 1 and \
         not ghostAtCoords([coords[0], coords[1] + 1]):
            coords[1] += 1
    elif direction == DIR_UP:
        if coords[1] - 1 >= 0 and \
         GAME_BOARD[coords[1] - 1][coords[0]] == 1 and \
         not ghostAtCoords([coords[0], coords[1] - 1]):
            coords[1] -= 1

""" Return the direction the ghost specified by ghostNum should move
    according to BFS. ghostNum is in [0,3].
"""
def BFSHelper(ghostNum):
    dir = None
    search = bfs(searchGraph[ghostCoords[ghostNum][1]][ghostCoords[ghostNum][0]], (pacmanCoords[1], pacmanCoords[0]))
    if search and len(search) == 2:
        dir = convertDirFormat(search[1])
        addSearchPath(search[0], SEARCH_PATH)
    return dir

""" Move all ghosts along the current ambush path if they are included in it.
    If a ghost is not included in the path, move it according to BFS.
"""
def ambushPathFollowerHelper():
    global ambushPath
    for i in range(len(ambushPath)):

        # Ghost is included:
        if ambushPath[i] is not None and len(ambushPath[i]) >= 2:
            path = ambushPath[i]
            dir = convertDirFormat(gimme_direction(path))
            moveGhost(dir, i + 1)

        # Ghost is not included, move according to BFS:
        elif ambushPath[i] is None:
            dir = BFSHelper(i)
            moveGhost(dir, i + 1)

""" Remove the first element of each ghost's path in ambushPath. """
def ambushPathUpdaterHelper():
    global ambushPath
    for i in range(len(ambushPath)):
        if ambushPath[i] is not None and len(ambushPath[i]) >= 2:
            ambushPath[i] = ambushPath[i][1:]

""" Helper function, return true iff a ghost is at coords. """
def ghostAtCoords(coords):
    global searchStrat, ambushing
    if searchStrat == STRATEGY_AMBUSH and ambushing:
        return False
    for ghost in range(4):
        if coords == ghostCoords[ghost]:
            return True
    return False

""" Helper function to convert a dir string to the frontend format. """
def convertDirFormat(dir):
    if dir == "right":
        return DIR_RIGHT
    elif dir == "left":
        return DIR_LEFT
    elif dir == "up":
        return DIR_UP
    elif dir == "down":
        return DIR_DOWN

""" Clear all graphical search paths on the grid. """
def clearSearchPaths():
    global renderBoard
    renderBoard = [row[:] for row in GAME_BOARD]

""" Add a graphical search path to the grid.
    Type should be either SEARCH_PATH or PLAYER_PATH.
"""
def addSearchPath(path, type):
    if SHOW_SEARCH_PATHS:
        global renderBoard
        if len(path) > 0:
            path.pop(0)
        for node in path:
            x, y = node.get_coord()
            renderBoard[x][y] = type

if __name__ == '__main__': pacman()
