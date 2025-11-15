# --- PART 1: IMPORT LIBRARIES AND INITIALIZE ---
# We must first import the libraries we need.

# Import the 'pygame' library. This is the entire toolbox we will use
# to create the game window, draw shapes, handle clicks, etc.
import pygame

# Import the 'sys' library. This (System) library lets us
# interact with the computer's operating system, which we
# mainly use here to properly close the game window when the user quits.
import sys

# --- PART 2: DEFINE OUR GLOBAL CONSTANTS ---
# Constants are variables that we set once and never change.
# Using all-caps for the names (like 'WIDTH') is a standard Python
# convention to show "This value isn't supposed to change."

# --- Screen Dimensions ---
# Set the width of our game window in pixels
WIDTH = 600
# Set the height of our game window in pixels
HEIGHT = 600

# --- Board Dimensions ---
# Our Tic-Tac-Toe board is a 3x3 grid.
BOARD_ROWS = 3
BOARD_COLS = 3
# We can calculate the size of each square based on the window width
# The '//' operator does "integer division," which means it drops any
# decimal (e.g., 600 // 3 = 200).
SQUARE_SIZE = WIDTH // BOARD_COLS

# --- Colors (Using RGB values) ---
# Colors in Pygame are defined by (Red, Green, Blue) tuples.
# Each value ranges from 0 (none of that color) to 255 (full color).
BG_COLOR = (28, 170, 156)  # A nice teal color
LINE_COLOR = (23, 145, 135)  # A darker teal
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Colors for the X's and O's
PLAYER_X_COLOR = (84, 84, 84)  # A dark gray
PLAYER_O_COLOR = (242, 235, 211)  # An off-white

# --- Line Widths ---
# How thick (in pixels) our lines should be.
LINE_WIDTH = 15
# How thick the 'X' and 'O' lines should be.
FIGURE_WIDTH = 15

# --- Figure Padding ---
# This is a small margin so 'X's and 'O's don't touch the grid lines.
FIGURE_PADDING = 30

# --- Player and AI Identifiers ---
# We'll represent players internally as numbers.
PLAYER_X = 1
PLAYER_O = 2
EMPTY = 0  # Represents an empty square on the board

# --- PART 3: SETUP THE PYGAME WINDOW ---

# Initialize all the pygame modules. You must do this first!
pygame.init()

# Create the main game window (called a 'surface' in Pygame).
# We pass it a tuple (WIDTH, HEIGHT) for its size.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title that appears in the top bar of the window.
pygame.display.set_caption('Tic Tac Toe - Player vs. Player')

# Fill the entire screen with our background color.
# We do this once at the start to set the initial color.
screen.fill(BG_COLOR)

# --- PART 4: CLASSES AND GAME LOGIC ---
# We will use classes to organize our code. A class is a "blueprint"
# for creating objects. This keeps our code clean and reusable.

class Board:
    """
    This class represents the internal "brain" of the Tic-Tac-Toe board.
    It doesn't draw anything; it just keeps track of the game state.
    """

    def __init__(self):
        # The constructor. This runs when we create a new Board object.
        # We create a 2D list (a list of lists) to represent the 3x3 grid.
        # We start by filling it with 'EMPTY' (which we defined as 0).
        self.squares = [[EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        # We also keep track of how many squares are filled.
        self.marked_squares = 0

    def mark_square(self, row, col, player):
        """Marks a square on the board for a given player."""
        # We set the value of the square in our 2D list.
        self.squares[row][col] = player
        # We increment the count of marked squares.
        self.marked_squares += 1

    def is_square_available(self, row, col):
        """Checks if a specific square is empty."""
        # It's available if its value is still the 'EMPTY' (0) value.
        return self.squares[row][col] == EMPTY

    def is_board_full(self):
        """Checks if all 9 squares have been marked."""
        return self.marked_squares == 9

    def is_board_empty(self):
        """Checks if no squares have been marked."""
        return self.marked_squares == 0

    def get_empty_squares(self):
        """Returns a list of (row, col) tuples for all empty squares."""
        empty_squares = []
        # We "iterate" (loop) through all rows and columns.
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # If the square is empty...
                if self.is_square_available(row, col):
                    # ...add its (row, col) to our list.
                    empty_squares.append((row, col))
        # Return the final list.
        return empty_squares

    def check_win(self, player):
        """Checks if the given 'player' has won the game."""
        
        # --- Check Vertical Wins ---
        # Loop through each column (0, 1, 2)
        for col in range(BOARD_COLS):
            # Check if all 3 squares in that column belong to the player
            if self.squares[0][col] == player and self.squares[1][col] == player and self.squares[2][col] == player:
                # If so, return True (they won)
                return True

        # --- Check Horizontal Wins ---
        # Loop through each row (0, 1, 2)
        for row in range(BOARD_ROWS):
            # Check if all 3 squares in that row belong to the player
            if self.squares[row][0] == player and self.squares[row][1] == player and self.squares[row][2] == player:
                # If so, return True (they won)
                return True

        # --- Check Diagonal Wins ---
        # 1. Check Top-Left to Bottom-Right Diagonal
        if self.squares[0][0] == player and self.squares[1][1] == player and self.squares[2][2] == player:
            return True
        # 2. Check Top-Right to Bottom-Left Diagonal
        if self.squares[0][2] == player and self.squares[1][1] == player and self.squares[2][0] == player:
            return True
            
        # --- No Win Found ---
        # If we check all 8 possibilities and none are true,
        # then this player has not won.
        return False

# The entire AI class is no longer needed for a 2-player game.
# class AI: ... (REMOVED) ...

class Game:
    """
    This class brings all the pieces together.
    It manages the game flow, drawing, and user input.
    """
    
    def __init__(self):
        # The constructor. This runs when we create a new Game object.
        # It creates a new Board object
        self.board = Board()
        # It creates a new AI object
        # self.ai = AI() # Removed AI
        # It sets the starting player (PLAYER_X)
        self.current_player = PLAYER_X
        # 'gamemode' can be 'pvp' (player vs player) or 'ai'
        self.gamemode = 'pvp' # Default to playing vs. player
        # 'game_over' is a "flag" that tells us if the game is running
        self.game_over = False
        # We call the draw_lines() method once to draw the grid.
        self.draw_lines()

    def draw_lines(self):
        """Draws the 3x3 grid lines on the screen."""
        
        # --- Draw Horizontal Lines ---
        # We need two horizontal lines.
        # Line 1: From (0, 200) to (600, 200)
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        # Line 2: From (0, 400) to (600, 400)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

        # --- Draw Vertical Lines ---
        # We need two vertical lines.
        # Line 1: From (200, 0) to (200, 600)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Line 2: From (400, 0) to (400, 600)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figure(self, row, col):
        """Draws an 'X' or 'O' in the specified (row, col) square."""
        
        # If the player is PLAYER_X (1)
        if self.current_player == PLAYER_X:
            # --- Draw 'X' ---
            # 'X' is made of two crossing lines.
            
            # Line 1: Top-left to bottom-right
            # We use 'FIGURE_PADDING' to make it a bit smaller than the square
            start_pos = (col * SQUARE_SIZE + FIGURE_PADDING, row * SQUARE_SIZE + FIGURE_PADDING)
            end_pos = (col * SQUARE_SIZE + SQUARE_SIZE - FIGURE_PADDING, row * SQUARE_SIZE + SQUARE_SIZE - FIGURE_PADDING)
            pygame.draw.line(screen, PLAYER_X_COLOR, start_pos, end_pos, FIGURE_WIDTH)
            
            # Line 2: Top-right to bottom-left
            start_pos = (col * SQUARE_SIZE + FIGURE_PADDING, row * SQUARE_SIZE + SQUARE_SIZE - FIGURE_PADDING)
            end_pos = (col * SQUARE_SIZE + SQUARE_SIZE - FIGURE_PADDING, row * SQUARE_SIZE + FIGURE_PADDING)
            pygame.draw.line(screen, PLAYER_X_COLOR, start_pos, end_pos, FIGURE_WIDTH)

        # Else if the player is PLAYER_O (2)
        elif self.current_player == PLAYER_O:
            # --- Draw 'O' (a circle) ---
            
            # We need the center of the circle.
            # 'int()' converts any decimal to a whole number.
            center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            center = (center_x, center_y)
            
            # We need the radius (size) of the circle.
            radius = (SQUARE_SIZE // 2) - FIGURE_PADDING
            
            # Draw the circle.
            # (surface, color, center, radius, width)
            pygame.draw.circle(screen, PLAYER_O_COLOR, center, radius, FIGURE_WIDTH)

    def make_move(self, row, col):
        """Handles the logic for making a move."""
        
        # 1. Mark the square in our internal 'board' object
        self.board.mark_square(row, col, self.current_player)
        
        # 2. Draw the 'X' or 'O' on the 'screen'
        self.draw_figure(row, col)
        
        # 3. Check if this move was a winning move
        if self.board.check_win(self.current_player):
            # If so, set the game_over flag to True
            self.game_over = True
        
        # 4. Switch to the next player
        # If current_player is 1, (1 % 2) + 1 = 1 + 1 = 2
        # If current_player is 2, (2 % 2) + 1 = 0 + 1 = 1
        # This is a clever trick to swap between 1 and 2.
        self.current_player = (self.current_player % 2) + 1

    def restart(self):
        """Resets the game to its initial state."""
        print("Restarting game...")
        # 1. Fill the screen with the background color (erasing all figures)
        screen.fill(BG_COLOR)
        # 2. Redraw the grid lines
        self.draw_lines()
        # 3. Create a new, empty Board object
        self.board = Board()
        # 4. Reset the starting player to PLAYER_X
        self.current_player = PLAYER_X
        # 5. Set the game_over flag back to False
        self.game_over = False

# --- PART 5: MAIN GAME CLASS AND LOOP ---
# This is the main "entry point" of our program.

class Main:
    """The main class that runs the game loop."""
    
    def __init__(self):
        # Create a new Game object when we start.
        self.game = Game()

    def run(self):
        """This is the main game loop."""
        
        # Create a new Game object.
        game = self.game
        
        # This 'while True' loop will run forever, checking for
        # user input and updating the game, until the user
        # clicks the "close" button on the window.
        while True:
            # --- Event Handling ---
            # 'pygame.event.get()' gets a list of all user actions
            # (like clicks, key presses, etc.) that have happened
            # since the last time we checked.
            for event in pygame.event.get():
                
                # --- Quit Event ---
                # Check if the event is the user clicking the 'X'
                # button on the window.
                if event.type == pygame.QUIT:
                    # If so, we 'quit' pygame...
                    pygame.quit()
                    # ...and 'exit' our program.
                    sys.exit()
                    
                # --- Key Press Event ---
                # Check if the event is a key being pressed down.
                if event.type == pygame.KEYDOWN:
                    # Check if the key pressed was the 'r' key.
                    if event.key == pygame.K_r:
                        # If so, call the game's restart method.
                        game.restart()
                        
                    # Check if the key was '0' (to set AI level to 0)
                    # We removed the AI, so these keys are no longer needed
                    # if event.key == pygame.K_0:
                    #     ...
                        
                    # Check if the key was '1' (to set AI level to 1)
                    # if event.key == pygame.K_1:
                    #     ...

                # --- Mouse Click Event ---
                # Check if the event is the mouse button being pressed down.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Check one condition:
                    # 1. Is the game *not* over?
                    # Since it's always pvp, we just check if game is over.
                    if not game.game_over:
                        # Get the (x, y) pixel coordinates of the mouse click
                        # 'event.pos[0]' is the x-coordinate
                        # 'event.pos[1]' is the y-coordinate
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        
                        # Convert pixel coordinates (e.g., 250, 450)
                        # into grid coordinates (e.g., row 2, col 1)
                        clicked_row = int(mouseY // SQUARE_SIZE)
                        clicked_col = int(mouseX // SQUARE_SIZE)
                        
                        # Check if the clicked square is available
                        if game.board.is_square_available(clicked_row, clicked_col):
                            # If it is, make the move!
                            game.make_move(clicked_row, clicked_col)
                            
                            # Check for a draw (board is full and no one won)
                            if not game.game_over and game.board.is_board_full():
                                game.game_over = True
                                print("It's a draw!")
            
            # --- AI's Turn ---
            # This entire block is no longer needed.
            # if game.gamemode == 'ai' and game.current_player == game.ai.player and not game.game_over:
            #     ...

            # --- Update the Display ---
            # After all logic and drawing for this frame is done,
            # we tell pygame to update the screen to show our changes.
            pygame.display.update()


# --- PART 6: RUN THE GAME ---

# This 'if' statement is a standard Python convention.
# It means "only run the code below if this script is
# being run directly" (not imported as a module).
if __name__ == '__main__':
    # 1. Create an instance of our Main class
    main_game = Main()
    # 2. Call the 'run' method to start the game loop
    main_game.run()