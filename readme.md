
# Artificial Intelligence (Triggle)

This project was developed as part of a university course on **Artifical Intelligence**. The main objective was to create a game called **Triggle** that could initially be played player-vs-player, with later stages introducing an AI opponent.

## Phase I
For the user interface, **Pygame** was used. The application consists of three main menus:
- Main menu,
- Options menu and
- Game menu.
The main menu includes buttons to start a game or exit the application. Clicking the `Play` button opens the options menu, where players can choose wether to play against the AI or another player. Next, player selects who goes first, followed by selecting the size of the game board (ranging from 4 to 8). Finally, clicking the `Play` button launches the game window.

### Logic
The application logic relies on the following data structures:

#### Matrix
The **Matrix** serves as a helper data structure for rendering the game board in **Pygame** and managing the positioning of poles. Its dimensions are determined based on the player's input.

#### Graph
The **Graph** is the **primary data structure** in the application and is implemented as a **dictionary**. Each key in graph is a **tuple** `(i, j)` representing node's index, while the corresponding value is a **set** of neighboring nodes to which a band is streched.

#### Set
**Sets** are used to store specific data due to their ability to hold only unique elements. They are particularly useful for:
- storing formed paths (stretched bands) and
- tracking cycle of length 3 (triangles) separately for each player.

### Functions

#### Main functions
- **make_move** - This function takes a goal node as a parameter. It checks whether the distance between the starting and goal nodes is valid. It simulates moving from the starting the starting node in all possible directions, exactly 4 steps, to determine if the goal node can be reached. If the move is valid, a line is drawn representing the streched band, and the functions `find_triangles` and `draw_triangles` are called. If the move is invalid, an error is returned.
- **make_move_tournament** - This function is very similar to `make_move` but is adapted to the format provided in the class. Differences include:
    - The direction is predetermined, so not all directions are checked.
    - It checks wether the move goes outside the board.
    - It does not check if the goal node is reached, as direction is already given.
- **find_triangles** - After each player's move, this function checks wether any new triangles are formed. Identified triangles are added to the active player's set of triangles and are visualized using the `draw_triangles` function.

#### Rendering functions
These functions visualize the game and display the current state of the board:
- **coordiantes_to_pixel** - Converts a node's coordinates into pixel values for screen drawing.
- **create_empty_borad** - Draws an empty board with all poles, based on the selected dimensions.
- **create_graph** - Generates a graph based on the board's dimensions, used to track nodes and possible moves.
- **draw_line** - Draws a line between two poles to represent a stretched band.
- **draw_triangles** - Draws triangles formed by the active player, using a distinct color for each player.

#### Validation functions
These functions are used to verify different aspects of the game:
- **in_boundaries** - Checks wether the given cooridnates are within the boundaries of the board, ensuring moves stay within playable area.
- **check_length** - Verifies that the distance between two poles is exactly 3.
- **end_game** - Determines whether the game has ended.

## Phase II
Functions for this phase will be expalined for classes.

### Game World
The **Game World** represents the current state of a *Triggle* match. At the top of the screen, the UI displays which player is currently active and the last move made. Each player's score is shown on the left and right sides, while the Triggle board is rendered in the center. The game world updates in real time to reflect new bands, formed triangles, and any changes in turns or game state.

### Board
The **Board** class is responsible for rendering the game board. The **render** method contains the logic for drawing the board using the class attributes, while the **update** method handles user input and updates attribute values accordingly.

Poles are stored as a separate class because they include logic for collision detection. For this reason, the board maintains an array of pole instances, each with its own unique index.

Within the **update** method, the function for playing a move is called. The **make_move** function performs the following steps:
- Validates user input. If the input is invalid, the same player must make another move, the function continues execution.
- Saves current game state within the Board class.
- Generates all possible new game states based on the current one.

### Game State
The **Game State** is used to store the current state of the game. The main functions are:
- **update_state** - Takes path formed between two selected poles and updates the game accordingly. Specifically:
    - The path is added to the array of `paths` and to the graph.
    - All triangles formed as a result of the new path are identified.
    - The active player is switched, and the last move is recorded.
    - The function modifies the current instance of the game state.
- **get_new_state** - Performs the same opeartions as `update_state`, but insteead of modifying the existing instance, it returns a **new** game state reflecting the changes.
- **generate_all_possible_moves** - Generates all possible future states based on the current game state. It does this by simulating every valid move the active player can make. For each move, a **deep copy** of the current state is changed, and `get_new_state` is called to produce a new state without altering the original. All generated states are collected in an array, which the function returns. Deep copying is a computationally expensive operation and will be optimized using shallow-like copy in the next phase.

## Phase III
In this phase, the main task was to implement the **MinMax algorithm** along with **Alpha-Beta pruning** to enable AI decisiong-making and improve performance by reducing unnecessary computations.

## Authors
- 👤 [Aleksa Perić](https://github.com/aleksa1205)
- 👤 [Jovan Cvetković](https://github.com/CJovan02)
- 👤 [Anja Janković](https://github.com/saznanyaa)
