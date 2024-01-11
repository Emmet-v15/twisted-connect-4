#!/usr/bin/env python
"""
    7/01/2024
    Programming Fundamentals - Assessment 2

        - A twist on connect 4

    General Styling: https://peps.python.org/pep-0008/
    Docstring format: https://peps.python.org/pep-0257/

    Tested to be working in vscode integrated terminal, command prompt, wsl & git bash.

    I'm proud of my score calculation function, so if you're going to read a function, read that :D
"""

__author__ = "Emmet Noman"
__email__ = "27587991@students.lincoln.ac.uk"

import sys
import time
import random
import numpy as np

try:
    import colours # custom module
except ModuleNotFoundError:
    print("colour.py was not found in the same folder. please make sure you have both required files.")
    sys.exit()

# Game rules
BOARD_SIZE = (6, 7) # x, y # Can support infinite length boards, although it can get hard to count columns past 10
OBSTACLE_SIZE = (2, 3) # x, y 
CONNECT_SIZE = 4 # the amount of cells in a row required to score a point.
MOVE_TIME_LIMIT = 5 # seconds of inactivity till move is lost

# Since we aren't allowed to import enum, we have to use constants to store enum values
# Cell types
EMPTY = 0
# ... any amount of player ids can go between 0 and 255 e.g. player 42, 21
OBSTACLE = 255 # unsigned 8 bit max int

class RanOutOfTimeException(Exception):
    def __init__(self):
        super().__init__(colours.yellow("You took too long") + ", the move has been transferred to the next player.")


class IllegalMoveException(Exception):
    def __init__(self, reason=None):
        """Tells the user they move was illegal and provide a reason if given.
        
        Keyword Arguemnts:
        reason (default: None) -- The reason their move is illegal.
        """
        super().__init__(colours.yellow(f"That move is not possible{f' because {reason}' if reason else ''}, try again."))

class InvalidInputException(Exception):
    """Raised when input validation fails."""
    def __init__(self, invalid_value, message):
        super().__init__(colours.yellow(f"\"{invalid_value}\" {message}"))

class Player():
    player_counter = 0
    players = {}
    def __init__(self, colour):
        """Creates a unique player.
        
        Arguments:
        name -- The name of the player (string).
        """
        Player.player_counter += 1
        self.id = Player.player_counter # static reference to player count
        Player.players[self.id] = self
        self.colour = colour
        self.__name = self.__get_username_input() # name should not be directly used, as it is formatted with colour in __str__.
        self.__score = 0
        self.pop_out_left = 1 # amount of pop outs left
        self.special_disc_left = 1 # ammount of special discs left

    def __get_username_input(self):
        """Private function to get username from player"""
        while True: # keep going until we have a valid input
            try:
                return validate_username_input(input(self.colour(f"Enter a username for player {self.id}\n:")), f"Player {self.id}")
                # if the validation succeeds, break out of the loop via return
            except InvalidInputException as e: # catch only the custom error defintion
                print(e) # tell the user the error & continue

    def __str__(self):
        return self.colour(self.__name) # print the name of the player when the object is printed.
    
    @property
    def score(self):
        return self.__score

    @score.setter # Setting the player.score will call this method.
    def score(self, value):
        """Prints score change on assignment"""
        
        difference = value - self.score
        if difference > 0:
            print(f"{self} gained {colours.yellow(abs(difference))} point{'s' if difference > 1 else ''}, They now have {colours.yellow(value)} points.")
        elif difference < 0:
            print(f"{self} lost {colours.yellow(abs(difference))} point{'s' if difference > 1 else ''}. They now have {colours.yellow(value)} points.")
        self.__score = value

class Board():
    def __init__(self, board_size):
        """Creates a board with an obstacle placed randomly at the bottom.

        Arguments:
        board_size -- A 2 element tuple that describes the size of the board.
        """
        self.board = np.zeros(board_size, dtype=np.uint8) # generate a 2 dimentional array, with zeroed 8 bit unsigned integer as the values.

    def add_obstacle(self, obstacle_size=OBSTACLE_SIZE):
        """Adds an obstacle at a random point along the bottom of the board.
        
        
        Keyword Arguments:
        obstacle_size (default OBSTACLE_SIZE) -- A 2 element tuple that describes the size of the obstacle.
        """

        rand_y = random.randint(0, self.board.shape[1]-obstacle_size[1]) # get the last possible leftmost position of the obstacle.
        self.board[self.board.shape[0]-obstacle_size[0]:self.board.shape[0], rand_y:rand_y+obstacle_size[1]] = OBSTACLE # calculate and set the obstucted cells to the pesudo-enum OBSTACLE, to denote that they have been obstructed.


    def calculate_scores(self, connect_size=CONNECT_SIZE):
        """Calculates and sets the scores of the players.

        Keyword Arguments:
        connect_size (default CONNECT_SIZE) -- the amount of discs that should be placed in one line to score a point.
        """
        matrix = self.board

        # all 4 directions that someone could have a point:
        backwards_diag = [np.diag(matrix, k=i) for i in range(-matrix.shape[0]+1,matrix.shape[1])] # get all foward facing diagonals 
        fowards_diag = [np.diag(np.flipud(matrix), k=i) for i in range(-matrix.shape[0]+1,matrix.shape[1])] # get all backward facing diagonals
        vertical = np.swapaxes(matrix, 0, 1) # swap the axes to have vertical lanes
        horizontal = matrix # default is horizontal

        score_buffer = {} # store the score so we only update the score property of player once.

        for direction in [backwards_diag, fowards_diag, vertical, horizontal]:
            for lane in direction:
                if len(lane) < connect_size: continue
                indices = np.where(np.diff(lane) != 0)[0] + 1 # find the indices where the discs change
                sublanes = np.split(lane, indices) # split the lane at the found indices
                results = [(sublane[0], len(sublane)) for sublane in sublanes] # create a list of tuples containing the value and its count for each lane
                for cell, connection_length in results:
                    if connection_length < connect_size or cell in [EMPTY, OBSTACLE]: # make sure it is a player that we are tracking
                        continue
                    # if score is not already set this round for the given player, default it to 0 and add the calculated score to it.
                    score_buffer[cell] = score_buffer.setdefault(cell, 0) + connection_length - (connect_size - 1)
            
        for playerid, score in score_buffer.items():
            Player.players[playerid].score = score

        for id, player in Player.players.items():
            if id not in score_buffer.keys():
                player.score = 0

    def perform_move(self, player, move_type, column):
        """Updates the board with respect to the player and move type.
        
        Arguments:
        player -- The Player (object) that performs the move.
        move_type -- The type of move being used. (string containing "n", "p" or "s", for normal, pop and special respectively.)
        
        Raises:
        IllegalMoveException -- if the move performed by the user is not allowed due to the rules of the game. e.g. the requested column is full.
        """

        column_cells = self.board[:, column] # get the column slice of the move

        for row in range(0, len(column_cells)): # loop over every row
            if np.all(column_cells) and move_type != 'p': # check if it is full unless it's popout.
                raise IllegalMoveException("the column is full")
            if row == self.board.shape[0]-1 or column_cells[row+1]: # check if column is full / is the bottom of the board / is the current spot the last free slot
                break # we will use this row, as this is the correct row.
        
        match move_type:
            case "n":
                self.board[row, column] = player.id # set the cell to the player's id to mark it as theirs
                return
            case "p":
                if not player.pop_out_left: raise IllegalMoveException("you have no more PopOut left")
                if self.board[-1, column] == player.id:
                    self.board[-1, column] = EMPTY
                    self.__apply_gravity()
                    player.pop_out_left -= 1
                else:
                    raise IllegalMoveException("you cannot popout a disc that you don't own")
                return
            case "s":
                # grab all 9 tiles around the cell it landed on.
                if not player.special_disc_left: raise IllegalMoveException("you have no more special discs left")
                row_slice = slice(max(0, row - 1), min(self.board.shape[0], row + 2)) # make sure it is not out of bounds
                col_slice = slice(max(0, column - 1), min(self.board.shape[1], column + 2)) # make sure it is not out of bounds.
                self.board[row_slice, col_slice] = EMPTY # set the grabbed cells to be empty
                self.__apply_gravity() # do a gravity simulation on the array
                player.special_disc_left -= 1
                return 

    def __apply_gravity(self):
        """Iterate over the board matrix multiple times until every cell is in it's lowest state."""
        while True:
            oldState = np.copy(self.board) # make a clone of the matrix, so we don't accidentally use a reference.
            for (row, column), cell in np.ndenumerate(self.board[:-1, :]): # loop over board, with the last row omitted.
                if self.board[row + 1, column] == EMPTY: # if slot below is empty
                    self.board[row, column] = EMPTY # set the current to empty
                    self.board[row + 1, column] = cell # set the slot below to what current was
            if np.array_equal(oldState, self.board): 
                break # nothing was changed on the board this iteration, break
            else:
                continue # there was something that moved, so we need to iterate again to make sure everything is settled.

    def __str__(self):
        """Creates an ascii representation of the board.
        
        Returns:
        A string that can be printed to the terminal.
        """
        string_repr = "\t\t"
        string_repr += colours.light_purple(colours.underline(" ".join(str(y) for y in range(1, BOARD_SIZE[1]+1)))) + "\n\t\t" # Underlined numbers
        for y in range(len(self.board)):
            row = self.board[y]
            for cell in row: # go over every cell
                if cell == OBSTACLE:
                    string_repr += colours.light_purple("◌") # draw light purple cell for obstacle
                elif cell == EMPTY:
                    string_repr += [colours.dark_gray("◌"), colours.dark_gray("○")][random.randint(0, 1)] # draw a random pattern for background (for aesthetics)
                for id, player in Player.players.items():
                    if cell == id:
                        string_repr += player.colour("○") # draw the player depending on their colour.

                string_repr += " "
            string_repr += "\n\t\t"
        string_repr += colours.light_purple("‾"*(2*BOARD_SIZE[1]-1)) # draw the bottom of the board, this is responsive to the board size.
        return string_repr.encode('utf8').decode(sys.stdout.encoding) # make sure to be using the utf-8 encoding as the circles do not work in some other encodings.

    def is_empty_slot_available(self):
        """Checks if the board has any empty spaces left.

        Returns:
        True if there is an empty slot available, else False.
        """
        return not np.all(self.board)
    
def validate_username_input(string, default):
    """Does a sanity check on the given user input

    Arguments:
    string -- unchecked user input string
    default -- the default value to fallback to, if the user inputs nothing.

    Returns:
    The given string or a default value in case it is empty.

    Raises:
    InputValidationException
    """
    if len(string) == 0: # Default name, e.g. green / red
        return default
    if len(string) > 15:
        raise InvalidInputException(string, "is too long of a username!")
    if len(string) < 3:
        raise InvalidInputException(string, "is too short of a username!")
    return string

def get_generic_choice_from_input(message, choices, default):
    """Get the user input by displaying the given message.
    This function guarantee a user response.
    
    Arguments:
    message -- The message to display when asking for input.
    choices -- The valid choices that the user can pick from.
    default -- The default return value, if the user does not pick an option.
    """

    while True:
        try:
            if type(choices) == list:
                formatted_choices = []
                for choice in choices:
                    first_letter = choice[0].upper() if choice.lower() == default.lower() else choice[0].lower() # capitalize if it is default
                    end_letters = choice[1:].lower() # everything other than first character should always be lowercase
                    formatted_choices.append(f"[{first_letter}]{end_letters}") # put first letter in brackets, to show that you can type just that letter to pick the option.
                prettified_choices = "/".join(formatted_choices) # seperate them by slashes

            elif type(choices) == range: # if it is a range
                prettified_choices = f"({choices.start}-{choices.stop})" # only display the start and end of the range.

            user_input = input(f"{message}:\n{prettified_choices}: ").lower() # display the choices to the user.
            if user_input == "": return default

            matches = list(filter(lambda choice: str(choice).startswith(user_input), choices))
            if len(matches) > 1:
                raise InvalidInputException(user_input, "is ambigious.")
            elif len(matches) == 1:
                return matches[0]
            else:
                raise InvalidInputException(user_input, "is not a valid option.")
        except InvalidInputException as e:
            print(e)
            continue # They inputted an invalid response, so they have to try again.
        
def get_move_from_player(player, move_time_limit=MOVE_TIME_LIMIT, move_begin_time=time.time()):
    """Gets user input to use as the player's move.
    
    Arguments:
    player -- The player object which is responsible for the move.

    Keyword Arguments:
    move_begin_time (default: now) -- how long ago the move began.
    move_time_limit (default: MOVE_TIME_LIMIT) -- the time they should after their move_begin_time before their turn is lost.

    Returns:
    move_type -- The type of move (string containing "n", "p" or "s", for normal, pop and special respectively.)
    move_column -- The column of the move.

    Raises:
    RanOutOfTimeException -- If the player runs out of the given time.
    """

    while True: # check if move starts with one of the three letters.
        remaining_time = f"{move_time_limit - (time.time() - move_begin_time):.1f}" # calculate the time remaining before player will lose their turn.
        move_type = input(f"{player}, You have {colours.yellow(remaining_time)} seconds left to select a move type.\n" + player.colour("([N]ormal, [p]op, [s]pecial): ")).strip()
        if time.time() - move_begin_time > move_time_limit: # check if they took longer than the given amount of time.
            raise RanOutOfTimeException # We need to do it this way since otherwise we would have to break out of a nested loop, which is ugly.
        if move_type == "":
            yield "n" # Default to [n]ormal if nothing was entered.
            break
        elif any([keyword.startswith(move_type.lower()) for keyword in ["normal", "popout", "special"]]): # check if input matches a keyword.
            yield move_type[0] # yeild the first character of the string instead of the whole input.
            # this would be cleaner if we were allowed enums, as we would set it to the enum for the move.
            break
    while True:
        try:
            remaining_time = f"{move_time_limit - (time.time() - move_begin_time):.1f}"
            move_column = input(f"{player}, You have {colours.yellow(remaining_time)} seconds left to select the column for your move.\n" + player.colour(f"(1-{BOARD_SIZE[1]}): ")).strip()
            if time.time() - move_begin_time > move_time_limit: # check if they took longer than the given amount of time.
                raise RanOutOfTimeException # Again, to exit out of a nested loop.
            if not move_column.isdigit():
                raise InvalidInputException(move_column, "is not a number.")
            elif move_column:
                move_column = int(move_column)-1 # cast to int to check against valid inputs, minus 1 because arrays start from 0.
                if move_column not in range(0, BOARD_SIZE[1]): # make sure it is a valid column.
                    raise InvalidInputException(move_column, f"is not in the range 1-{BOARD_SIZE[1]}.")
                else:
                    yield move_column # They must have input a valid number.
        except InvalidInputException as e:
            print(e)
        
def get_obstacle_size_from_players():
    """Gets the players to decide on the amount of rows and columns the obstacle should have.
    The obstacle can not be bigger than either of the bounds provided by the board.

    returns:
    obstacle_rows -- how tall the obstacle will be.
    obstalce_cols -- how wide the obstacle will be."""

    
    response = get_generic_choice_from_input("Would you like to define a custom size for the obstacle?", ["yes", "no"], "no")
    if response == "yes":
        yield get_generic_choice_from_input(colours.light_purple("How tall should the obstacle be?"), range(1, BOARD_SIZE[0]), OBSTACLE_SIZE[0])
        yield get_generic_choice_from_input(colours.light_purple("How tall wide the obstacle be?"), range(1, BOARD_SIZE[1]), OBSTACLE_SIZE[1])
    else:
        yield OBSTACLE_SIZE[0]
        yield OBSTACLE_SIZE[1]

def main():
    print("*"*60 + "\n If you do not see colour, please use a different terminal.\n" + "*"*60)
    board = Board(BOARD_SIZE) # Create the board.
    try:
        print(board)
    except UnicodeEncodeError:
        colours.red("Your terminal does not support unicode encoding, please use a different terminal.")
        sys.exit(1)

    Player(colours.lime) # Create Lime player.
    Player(colours.red) # Create Red player.
    # Player(colours.yellow) # Add a third player, this is fully supported and works as expected.


    connect_size = get_generic_choice_from_input("How many discs should you connect in a row to gain a point? (default 4)", range(3,5), 4)
    user_obstacle_dimention_input = get_obstacle_size_from_players()

    board.add_obstacle((next(user_obstacle_dimention_input), next(user_obstacle_dimention_input))) # Add an obstacle to the bottom of the board.
    print(board)

    while board.is_empty_slot_available(): # check if there is an empty slot left on the board.
        for player in Player.players.values():
            move_begin_time = time.time() # set the timer to start from here.
            while True:
                try:
                    user_input = get_move_from_player(player, MOVE_TIME_LIMIT, move_begin_time)
                    board.perform_move(player, move_type=next(user_input), column=next(user_input)) # Get row and column from user and perform a move with it.
                except RanOutOfTimeException as e:
                    print(e)
                    time.sleep(2) # give users time to read the exception.
                except IllegalMoveException as e:
                    print(e)
                    continue # if the user made an illegal move, repeat the process.
                break

            print(board)
            board.calculate_scores(connect_size) # calculate scores based on custom connect length
            if not board.is_empty_slot_available():
                break

    winning_player = max(Player.players.values(), key=lambda player: player.score) # get the player who wins by comparing the scores
    tied_players = filter(lambda player: player.score == winning_player.score, Player.players.values())
    tied_players = list(map(lambda player: str(player), tied_players))

    if len(tied_players) > 1:
        print(f"Game finished, tie between {", ".join(tied_players[:-1])} and {tied_players[-1]} at {winning_player.score} points.")
    else:
        print(f"Game finished, {winning_player} won with {winning_player.score}!")    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(colours.yellow("\nCTRL+C detected. Exiting..."))
        sys.exit(0)
