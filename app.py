import copy
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ====================================== AI FUNCTIONS ==========================================

# returns an array of numbers that represents the index of the blank elements
def print_board(state):
    for i in range(0, len(state), 3):
        print(" ".join(state[i:i+3]))

def identify_blank_spaces(state):
    blank_spaces = []
    for i, element in enumerate(state):
        if element == " ":
            blank_spaces.append(i)
    return blank_spaces

# returns an array of possible states
def possible_states(state, player):
    possible_states = [] # will contain the possible states
    blank_spaces = identify_blank_spaces(state)
    for index in blank_spaces:
        new_state = copy.deepcopy(state)
        new_state[index] = player
        possible_states.append(new_state)
    return possible_states

# returns the player character if there's a winner
# returns 0 if draw
# returns none if there is no winner yet
def utility(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] and board[i] != " ":
            return board[i]
    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return board[i]
    # Check diagonals
    if board[0] == board[4] == board[8] and board[0] != " ":
        return board[0]
    if board[2] == board[4] == board[6] and board[2] != " ":
        return board[2]
    # Check for a draw
    if " " not in board:
        return 0
    # No winner yet
    return "None"

def check_min_max(board):
    count_x = board.count("X")
    count_o = board.count("O")
    if count_x == count_o:
        return "max"
    elif count_o < count_x:
        return "min"

def maxValue(state, alpha, beta):
    m = -999999
    best_move = None
    successors = possible_states(state, "X")
    for s in successors:
        print_board(s)
        print()
        # comparing the utility values of different states and updating m and best_move when a better move is found
        v, _ = value(s, alpha, beta)
        if v > m:
            m = v
            best_move = s
        if v >= beta:
            return m, best_move
        if m > alpha:
            alpha = m
    return m, best_move

def minValue(state, alpha, beta):
    m = 999999
    best_move = None
    successors = possible_states(state, "O")
    for s in successors:
        print_board(s)
        print()
        # comparing the utility values of different states and updating m and best_move when a better move is found
        v, _ = value(s, alpha, beta)
        if v < m:
            m = v
            best_move = s
        if v <= alpha:
            return m, best_move
        if m < beta:
            beta = m
    return m, best_move

def value(state, alpha, beta):
    condition = utility(state)
    if condition == "None":
        if check_min_max(state) == "max":
            print("Possible States (Max):")
            return maxValue(state, alpha, beta)
        else:
            print("Possible States (Min):")
            return minValue(state, alpha, beta)
    else:
        if condition == 0:
            print("Draw\n")
            return 0, None
        elif condition == "X":
            print("Winner: X\n")
            return 1, None
        elif condition == "O":
            print("Winner: O\n")
            return -1, None

# ====================================== GUI FUNCTIONS ==========================================

def create_player_selection_window():
    def on_choose_change(event):
        selected_value = choose.get()
        label_result.config(text=f"You chose: {selected_value}")

    def choose_button_click():
        selected_value = choose.get()
        label_result.config(text=f"You chose: {selected_value}")
        root.withdraw()  # Hide the player selection window
        show_tic_tac_toe(root, selected_value)

    # Create the main window
    root = tk.Tk()
    root.title("Player Selection")

    # Create a label and a dropdown for player selection
    label_choose = tk.Label(root, text="Choose:")
    label_choose.pack(pady=10)

    choose = ttk.Combobox(root, values=["X", "O"])
    choose.pack()
    choose.set("X")  # Set default value to X

    # Bind the dropdown selection event to the on_choose_change function
    choose.bind("<<ComboboxSelected>>", on_choose_change)

    # Create a label to display the chosen value
    label_result = tk.Label(root, text="You chose: X")
    label_result.pack(pady=10)

    # Create a button to trigger the print and hide the dropdown and button
    button_choose = tk.Button(root, text="Choose", command=choose_button_click)
    button_choose.pack(pady=10)

    root.mainloop()

def show_tic_tac_toe(root, player_choice):
    tic_tac_toe_window = tk.Tk()
    tic_tac_toe_window.title("Tic Tac Toe")

    # Create buttons for the Tic Tac Toe grid
    buttons = []
    for i in range(9):
        row, col = divmod(i, 3)
        button = tk.Button(tic_tac_toe_window, text=current_state[i], width=5, height=2,
                           command=lambda i=i: on_button_click(root, i, buttons, player_choice, tic_tac_toe_window))
        button.grid(row=row, column=col)
        buttons.append(button)

    tic_tac_toe_window.protocol("WM_DELETE_WINDOW", lambda: on_tic_tac_toe_close(root, tic_tac_toe_window))

    def on_tic_tac_toe_close(root, tic_tac_toe_window):
        tic_tac_toe_window.destroy()
        root.deiconify()  # Show the player selection window again

    # Determine who plays first
    if player_choice == "O":
        # AI plays first with a randomized move
        ai_first_move = random.choice(range(9))
        buttons[ai_first_move]["text"] = "X"
        current_state[ai_first_move] = "X"
        print_current_state()

        # Check for a winner or draw after the AI's initial move
        winner = check_winner(buttons)
        if winner:
            messagebox.showinfo("Winner!", f"Player {winner} wins!")
            reset_board(buttons)  # Reset the board after a win
            tic_tac_toe_window.withdraw()
            root.deiconify()  # Show the player selection window again
        elif check_draw(buttons):
            messagebox.showinfo("Draw!", "It's a draw!")
            reset_board(buttons)  # Reset the board after a draw
            tic_tac_toe_window.withdraw()
            root.deiconify()  # Show the player selection window again

    tic_tac_toe_window.mainloop()

def on_button_click(root, index, buttons, current_player, tic_tac_toe_window):
    if buttons[index]["text"] == " ":
        buttons[index]["text"] = current_player
        current_state[index] = current_player  # Update current_state based on the move
        print_current_state()  # Print the updated current_state to the terminal
        winner = check_winner(buttons)
        
        if winner:
            messagebox.showinfo("Winner!", f"Player {winner} wins!")
            reset_board(buttons)  # Reset the board after a win
            tic_tac_toe_window.withdraw()
            root.deiconify()  # Show the player selection window again
        elif check_draw(buttons):
            messagebox.showinfo("Draw!", "It's a draw!")
            reset_board(buttons)  # Reset the board after a draw
            tic_tac_toe_window.withdraw()
            root.deiconify()  # Show the player selection window again
        else:
            alpha = -999999
            beta = 999999
            # Call the value function to get the result
            result, best_move = value(current_state, alpha, beta)

            print("After clicked state:")
            print_board(current_state)
            print()

            if best_move is not None:
                print("Best Move:")
                print_board(best_move)

                # Update UI with AI's move (best move)
                update_ui_with_ai_move(buttons, best_move)

                # Check for a winner or draw after the AI's move
                winner = check_winner(buttons)
                if winner:
                    messagebox.showinfo("Winner!", f"Player {winner} wins!")
                    reset_board(buttons)  # Reset the board after a win
                    tic_tac_toe_window.withdraw()
                    root.deiconify()  # Show the player selection window again
                elif check_draw(buttons):
                    messagebox.showinfo("Draw!", "It's a draw!")
                    reset_board(buttons)  # Reset the board after a draw
                    tic_tac_toe_window.withdraw()
                    root.deiconify()  # Show the player selection window again

def update_ui_with_ai_move(buttons, ai_move):
    for i, value in enumerate(ai_move):
        if value != current_state[i]:
            buttons[i]["text"] = value
            current_state[i] = value
            
def print_current_state():
    # Print the current_state to the terminal
    print("\nCurrent State:")
    for i in range(0, 9, 3):
        print(" ".join(current_state[i:i + 3]))

def reset_board(buttons):
    global current_player
    current_player = "X"
    for button in buttons:
        button["text"] = " "

def check_winner(buttons):
    for line in winning_combinations:
        a, b, c = line
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != " ":
            return buttons[a]["text"]
    return None

def check_draw(buttons):
    for button in buttons:
        if button["text"] == " ":
            return False
    return True

def reset_board(buttons):
    global current_player, current_state
    current_player = "X"
    for i in range(9):
        buttons[i]["text"] = " "
        current_state[i] = " "

# ===========================================================================================

# Define winning combinations
winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]

current_state = [
    " ", " ", " ",
    " ", " ", " ",
    " ", " ", " "
]

current_player = "X"

# Call the function to create the player selection window
create_player_selection_window()