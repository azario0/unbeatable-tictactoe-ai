import random
import math
import time
import matplotlib.pyplot as plt # Keep for simulations if run separately
import numpy as np # Keep for simulations if run separately

# --- 1. Game Environment Setup (Unchanged from previous version) ---
EMPTY = ' '
# AI_PLAYER = 'O' # These will be dynamic in the API
# HUMAN_PLAYER = 'X'

def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    """Checks if the given player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_board_full(board):
    """Checks if the board is full (tie)."""
    return EMPTY not in board

def get_available_moves(board):
    """Returns a list of indices of available (empty) moves."""
    return [i for i, spot in enumerate(board) if spot == EMPTY]

def make_move(board, move, player):
    """Makes a move on the board. Returns a new board state."""
    if 0 <= move < 9 and board[move] == EMPTY:
        new_board = board[:]
        new_board[move] = player
        return new_board
    return None

# --- 2. Minimax Algorithm Implementation (Unchanged) ---
memo = {}

def minimax(board, depth, is_maximizing_player, alpha, beta, ai_player_symbol, human_player_symbol):
    board_tuple = tuple(board)
    if board_tuple in memo: # Check memoization
        return memo[board_tuple]

    if check_winner(board, ai_player_symbol):
        result = 10 - depth
        memo[board_tuple] = result # Store in memo
        return result
    if check_winner(board, human_player_symbol):
        result = depth - 10
        memo[board_tuple] = result # Store in memo
        return result
    if is_board_full(board):
        memo[board_tuple] = 0 # Store in memo
        return 0

    available_moves = get_available_moves(board)

    if is_maximizing_player:
        max_eval = -math.inf
        for move_idx in available_moves:
            new_board = make_move(board, move_idx, ai_player_symbol)
            eval_score = minimax(new_board, depth + 1, False, alpha, beta, ai_player_symbol, human_player_symbol)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        memo[board_tuple] = max_eval # Store in memo
        return max_eval
    else:
        min_eval = math.inf
        for move_idx in available_moves:
            new_board = make_move(board, move_idx, human_player_symbol)
            eval_score = minimax(new_board, depth + 1, True, alpha, beta, ai_player_symbol, human_player_symbol)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        memo[board_tuple] = min_eval # Store in memo
        return min_eval

# --- 3. AI Player Function (Unchanged) ---
def find_best_move(board, ai_player_symbol, human_player_symbol):
    best_score = -math.inf
    best_move = -1
    available_moves = get_available_moves(board)
    random.shuffle(available_moves) # Add some randomness for equally good moves

    # Critical: Clear memo before a new top-level search for a move,
    # or ensure memoization handles context properly if not cleared.
    # For API/standalone calls, clearing is safer.
    memo.clear() 
                                     
    for move_idx in available_moves:
        new_board = make_move(board, move_idx, ai_player_symbol)
        # Depth starts at 0 for the next state, opponent is not maximizing
        move_score = minimax(new_board, 0, False, -math.inf, math.inf, ai_player_symbol, human_player_symbol)

        if move_score > best_score:
            best_score = move_score
            best_move = move_idx
            
    if best_move == -1 and available_moves: # Fallback if all moves are losing, pick one
        return random.choice(available_moves)
    return best_move

# --- Simulation and Interactive Play (Original functions, will be called conditionally) ---
def random_move_agent(board, player_symbol):
    available_moves = get_available_moves(board)
    if available_moves:
        return random.choice(available_moves)
    return -1

def simulate_games_main(num_games, ai_starts_first, ai_player_char='O', opponent_char='X'):
    # (This is the simulate_games function from your original script)
    ai_wins = 0
    opponent_wins = 0
    ties = 0
    print(f"Simulating {num_games} games. AI ({ai_player_char}) vs Random Agent ({opponent_char}). AI starts first: {ai_starts_first}")
    for i in range(num_games):
        board = [EMPTY] * 9
        current_player_is_ai = ai_starts_first
        game_over = False
        if (i + 1) % (num_games // 10 if num_games >=10 else 1) == 0:
            print(f"  Simulating game {i+1}/{num_games}...")
        while not game_over:
            if current_player_is_ai:
                move = find_best_move(board, ai_player_char, opponent_char)
                board = make_move(board, move, ai_player_char)
                if check_winner(board, ai_player_char):
                    ai_wins += 1
                    game_over = True
            else:
                move = random_move_agent(board, opponent_char)
                if move != -1:
                    board = make_move(board, move, opponent_char)
                    if check_winner(board, opponent_char):
                        opponent_wins += 1
                        game_over = True
            if not game_over and is_board_full(board):
                ties += 1
                game_over = True
            current_player_is_ai = not current_player_is_ai
    return ai_wins, opponent_wins, ties

def run_simulations_and_charts():
    print("Step 1-3: Game Logic and Minimax AI are defined.")
    print("\nStep 4: Simulating games to evaluate AI performance...")
    NUM_SIMULATIONS = 50 # Reduced for quicker demo
    AI_PLAYER_SYMBOL_SIM = 'O'
    RANDOM_AGENT_SYMBOL_SIM = 'X'

    ai_wins_first, opp_wins_first, ties_first = simulate_games_main(NUM_SIMULATIONS // 2, True, AI_PLAYER_SYMBOL_SIM, RANDOM_AGENT_SYMBOL_SIM)
    ai_wins_second, opp_wins_second, ties_second = simulate_games_main(NUM_SIMULATIONS // 2, False, AI_PLAYER_SYMBOL_SIM, RANDOM_AGENT_SYMBOL_SIM)

    total_ai_wins = ai_wins_first + ai_wins_second
    total_opp_wins = opp_wins_first + opp_wins_second
    total_ties = ties_first + ties_second
    total_games = NUM_SIMULATIONS

    print("\n--- Simulation Results ---")
    print(f"Total Games Played: {total_games}")
    print(f"AI ({AI_PLAYER_SYMBOL_SIM}) Wins: {total_ai_wins} ({total_ai_wins/total_games*100:.2f}%)")
    print(f"Random Agent ({RANDOM_AGENT_SYMBOL_SIM}) Wins: {total_opp_wins} ({total_opp_wins/total_games*100:.2f}%)")
    print(f"Ties: {total_ties} ({total_ties/total_games*100:.2f}%)")
    if total_games > 0:
        accuracy = (total_ai_wins + total_ties) / total_games
        print(f"\nMinimax AI 'Unbeatability' (Wins + Ties vs Random): {accuracy*100:.2f}%")

    labels = [f'AI ({AI_PLAYER_SYMBOL_SIM}) Wins', f'Random ({RANDOM_AGENT_SYMBOL_SIM}) Wins', 'Ties']
    sizes_total = [total_ai_wins, total_opp_wins, total_ties]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes_total, labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral', 'lightgreen'])
    ax.axis('equal')
    ax.set_title(f'Overall Performance ({total_games} games)')
    plt.show()

def play_game_interactive():
    # (This is the play_game function from your original script)
    board = [EMPTY] * 9
    human_first_input = input("Do you want to start first? (yes/no): ").strip().lower()
    human_turn = human_first_input == 'yes'

    if human_turn:
        human_symbol = 'X'
        ai_symbol = 'O'
        print("You are X, AI is O. You start.")
    else:
        human_symbol = 'O'
        ai_symbol = 'X'
        print("You are O, AI is X. AI starts.")
    print_board(board)
    game_over = False
    while not game_over:
        if human_turn:
            valid_move = False
            while not valid_move:
                try:
                    move = int(input(f"Your turn ({human_symbol}). Enter move (0-8): "))
                    if 0 <= move <= 8 and board[move] == EMPTY:
                        board = make_move(board, move, human_symbol)
                        valid_move = True
                    else:
                        print("Invalid move. Spot taken or out of bounds. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 8.")
        else:
            print(f"AI's turn ({ai_symbol})...")
            time.sleep(0.5)
            ai_move = find_best_move(board, ai_symbol, human_symbol)
            board = make_move(board, ai_move, ai_symbol)
            print(f"AI chose move: {ai_move}")
        print_board(board)
        if check_winner(board, human_symbol):
            print("Congratulations! You won!")
            game_over = True
        elif check_winner(board, ai_symbol):
            print("AI wins! Better luck next time.")
            game_over = True
        elif is_board_full(board):
            print("It's a tie!")
            game_over = True
        human_turn = not human_turn

# +++ NEW: Flask API Implementation +++
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/predict_move', methods=['POST'])
def predict_move_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        board_input = data.get('board')
        ai_symbol = data.get('ai_symbol')
        opponent_symbol = data.get('opponent_symbol')

        # --- Input Validation ---
        if not board_input or not isinstance(board_input, list) or len(board_input) != 9:
            return jsonify({"error": "Invalid 'board' provided. Must be a list of 9 strings."}), 400
        if not all(isinstance(s, str) for s in board_input): # Ensure all elements are strings
            return jsonify({"error": "Board elements must be strings (e.g., 'X', 'O', ' ')."}), 400
        if not ai_symbol or not isinstance(ai_symbol, str) or len(ai_symbol) != 1:
            return jsonify({"error": "Invalid 'ai_symbol' provided. Must be a single character string."}), 400
        if not opponent_symbol or not isinstance(opponent_symbol, str) or len(opponent_symbol) != 1:
            return jsonify({"error": "Invalid 'opponent_symbol' provided. Must be a single character string."}), 400
        if ai_symbol == opponent_symbol:
            return jsonify({"error": "'ai_symbol' and 'opponent_symbol' cannot be the same."}), 400
        
        # Normalize board: ensure only ai_symbol, opponent_symbol, or EMPTY are present
        current_board = []
        for spot in board_input:
            if spot == ai_symbol:
                current_board.append(ai_symbol)
            elif spot == opponent_symbol:
                current_board.append(opponent_symbol)
            else: # Treat anything else (e.g. "", null from JSON, or other chars) as EMPTY
                current_board.append(EMPTY)


        # --- Game State Checks Before AI Moves ---
        if check_winner(current_board, ai_symbol):
            return jsonify({
                "board": current_board, "ai_move_index": None, "status": "game_over",
                "message": f"Game already over. AI ({ai_symbol}) had already won.",
                "game_over": True, "winner": ai_symbol
            }), 200
        if check_winner(current_board, opponent_symbol):
            return jsonify({
                "board": current_board, "ai_move_index": None, "status": "game_over",
                "message": f"Game already over. Opponent ({opponent_symbol}) had already won.",
                "game_over": True, "winner": opponent_symbol
            }), 200
        if is_board_full(current_board): # Check if board is full and no winner
            return jsonify({
                "board": current_board, "ai_move_index": None, "status": "game_over",
                "message": "Game already over. It's a tie.",
                "game_over": True, "winner": "tie"
            }), 200
        if not get_available_moves(current_board): # Should be caught by is_board_full
             return jsonify({
                "board": current_board, "ai_move_index": None, "status": "game_over",
                "message": "Board is full, no moves possible. It's a tie.",
                "game_over": True, "winner": "tie"
            }), 200


        # --- AI Makes a Move ---
        ai_move_index = find_best_move(current_board, ai_symbol, opponent_symbol)

        if ai_move_index == -1 : # Should only happen if no available moves, handled above.
             # This case suggests an issue if reached when moves are available
             return jsonify({"error": "AI could not determine a move, board might be in an unexpected state.", 
                             "board": current_board}), 500

        new_board_state = make_move(current_board, ai_move_index, ai_symbol)
        if new_board_state is None: # Should not happen if ai_move_index is valid
            return jsonify({"error": "AI generated an invalid move index.", "board": current_board, "ai_move_index_attempted": ai_move_index}), 500


        # --- Check Game State After AI's Move ---
        game_over_after_ai = False
        winner_after_ai = None
        message_after_ai = f"AI ({ai_symbol}) moved to position {ai_move_index}."

        if check_winner(new_board_state, ai_symbol):
            game_over_after_ai = True
            winner_after_ai = ai_symbol
            message_after_ai = f"AI ({ai_symbol}) moved to {ai_move_index} and won!"
        elif is_board_full(new_board_state): # Check for tie only if AI didn't win
            game_over_after_ai = True
            winner_after_ai = "tie" # Represent tie as 'tie'
            message_after_ai = f"AI ({ai_symbol}) moved to {ai_move_index}. It's a tie!"

        return jsonify({
            "board": new_board_state, # Use "board" to be consistent with input
            "ai_move_index": ai_move_index,
            "status": "success",
            "message": message_after_ai,
            "game_over": game_over_after_ai,
            "winner": winner_after_ai # Will be ai_symbol, 'tie', or None
        }), 200

    except Exception as e:
        # Log the exception for debugging
        app.logger.error(f"Error in /predict_move: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500


if __name__ == "__main__":
    # To run simulations and interactive play:
    # python your_script_name.py interactive
    # python your_script_name.py simulate
    #
    # To run the Flask API server:
    # python your_script_name.py api
    # OR (if no arg given, default to API):
    # python your_script_name.py

    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'interactive':
            print("Starting interactive game mode...")
            play_game_interactive()
        elif sys.argv[1] == 'simulate':
            print("Starting simulation mode...")
            run_simulations_and_charts()
        elif sys.argv[1] == 'api':
            print("Starting Flask API server for Tic-Tac-Toe AI on http://127.0.0.1:5000/predict_move ...")
            app.run(debug=True, port=5000) # Use a different port if 5000 is common
        else:
            print(f"Unknown command: {sys.argv[1]}. Use 'interactive', 'simulate', or 'api'.")
    else:
        # Default action: run the API server
        print("No mode specified, starting Flask API server by default.")
        print("Starting Flask API server for Tic-Tac-Toe AI on http://127.0.0.1:5000/predict_move ...")
        app.run(debug=True, port=5000)