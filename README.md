#Ghosts & Pac-Man

------------
Requirements
------------
1. Python 2.7 or above.  
2. Pygame (and its dependencies).  
    2.1. sudo apt-get install python-pygame, or  
    2.2. pip install pygame, or  
    2.3. Download the .whl (precompiled Python libraries) from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame.  


---------------------------
How to Run Ghosts & Pac-Man
---------------------------
1. Go to the "game" directory.
2. Run "python ghosts_and_pacman.py" from the command line.  
    2.1. The game window will pop up with the game paused.  
    2.2. Press 'P' to start the game.
3. Press 'P' at any point in the game to pause the game.
4. Use the arrow keys to move Pac-Man.  
    4.1. Pac-Man is represented by the yellow block.  
    4.2. The Ghosts are represented by the red, orange, pink and blue  
         blocks respectively.
5. Press 'S' to change the Ghosts' strategy at any point.  
    5.1. See "csc384-project.pdf" for more on the strategies.
6. Press 'Esc' at any point to exit the game.  

*. To run the game with a non-default miniMax search depth,
   Run "python ghosts_and_pacman.py --minimax-depth=<depth>", where
   <depth> is the search depth.  
   *.1. <depth> must be >= 3  
   *.2. <depth> only affects the "Minimax" and "Minimax + BFS" strategies.  
   *.3. If minimax-depth is not specified, <depth> defaults to 9.


----------------------------
Notes on running on UofT cdf
----------------------------
1. The default Python version (2.7) should be able to run the game.  
   1.1. Just follow the instructions above.
2. Only the default Python installation has Pygame installed. "Python3"
   for instance should not be able to run the game.


-------
Authors
-------
Hunter James Forsyth   https://github.com/hunterforsyth  
"Lennox" Shou Hao Ho   https://ca.linkedin.com/in/lennoxho
