# client_app/client_app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests # To make requests to your API
import os

app = Flask(__name__)
# It's good practice to set the secret key from an environment variable
# For development, you can use a hardcoded string, but change it for production
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_very_secure_default_secret_key_for_dev')

API_BASE_URL = "http://127.0.0.1:5000" # Your API server address
EMPTY_CELL = ' ' # Consistent with your API

# --- Helper Functions ---
def check_local_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_local_board_full(board):
    return EMPTY_CELL not in board

# --- Routes ---
@app.route('/', methods=['GET'])
def index():
    session.clear() # Clear session on new visit to start fresh
    return render_template('start.html')

@app.route('/start', methods=['POST'])
def start_game():
    player_symbol_choice = request.form.get('player_symbol')
    if player_symbol_choice == 'X':
        session['player_symbol'] = 'X'
        session['ai_symbol'] = 'O'
        session['turn'] = 'player' # Player X starts
    else:
        session['player_symbol'] = 'O'
        session['ai_symbol'] = 'X'
        session['turn'] = 'ai' # AI X starts

    session['board'] = [EMPTY_CELL] * 9
    session['game_over'] = False
    session['winner'] = None
    session['game_message'] = f"Game started. You are {session['player_symbol']}."

    if session['turn'] == 'ai':
        return redirect(url_for('ai_turn_handler')) # Immediately go to AI's turn

    return redirect(url_for('game_board'))

@app.route('/game')
def game_board():
    if 'board' not in session:
        return redirect(url_for('index'))

    return render_template('game.html',
                           board=session['board'],
                           player_symbol=session['player_symbol'],
                           ai_symbol=session['ai_symbol'],
                           turn=session['turn'],
                           game_over=session['game_over'],
                           winner=session['winner'],
                           game_message=session.get('game_message', ''))

@app.route('/move/<int:cell_index>')
def player_move(cell_index):
    if 'board' not in session or session['game_over'] or session['turn'] != 'player':
        flash("Invalid move or not your turn.", "error")
        return redirect(url_for('game_board'))

    board = session['board']
    player_symbol = session['player_symbol']

    if 0 <= cell_index < 9 and board[cell_index] == EMPTY_CELL:
        board[cell_index] = player_symbol
        session['board'] = board # Update session

        if check_local_winner(board, player_symbol):
            session['game_over'] = True
            session['winner'] = player_symbol
            session['game_message'] = f"Congratulations! You ({player_symbol}) won!"
        elif is_local_board_full(board):
            session['game_over'] = True
            session['winner'] = "tie"
            session['game_message'] = "It's a tie!"
        else:
            session['turn'] = 'ai'
            session['game_message'] = f"You played at {cell_index}. AI's turn."
            return redirect(url_for('ai_turn_handler')) # AI's turn
    else:
        flash("Invalid cell choice.", "error")

    return redirect(url_for('game_board'))


@app.route('/ai_turn')
def ai_turn_handler():
    if 'board' not in session or session['game_over'] or session['turn'] != 'ai':
        return redirect(url_for('game_board'))

    api_payload = {
        "board": session['board'],
        "ai_symbol": session['ai_symbol'],
        "opponent_symbol": session['player_symbol']
    }

    try:
        response = requests.post(f"{API_BASE_URL}/predict_move", json=api_payload, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        api_data = response.json()

        if api_data.get("error"):
            flash(f"API Error: {api_data['error']}", "error")
            session['game_message'] = f"Error from AI: {api_data['error']}"
            # Potentially let player try again or reset
        else:
            session['board'] = api_data['board']
            ai_move_idx = api_data.get('ai_move_index')
            
            if api_data.get("game_over"):
                session['game_over'] = True
                session['winner'] = api_data.get("winner") # 'X', 'O', or 'tie'
                if session['winner'] == session['ai_symbol']:
                    session['game_message'] = f"AI ({session['ai_symbol']}) moved to {ai_move_idx} and won!"
                elif session['winner'] == "tie":
                    session['game_message'] = f"AI ({session['ai_symbol']}) moved. It's a tie!"
                else: # Should not happen if API is correct, but as a fallback
                    session['game_message'] = f"Game over. Winner: {session['winner']}"
            else:
                session['game_message'] = f"AI ({session['ai_symbol']}) moved to {ai_move_idx}. Your turn."
            
            session['turn'] = 'player' # Switch back to player's turn

    except requests.exceptions.RequestException as e:
        flash(f"Could not connect to Tic-Tac-Toe API: {e}", "error")
        session['game_message'] = "Error: Could not reach AI. Please try again later."
        # Don't change turn, allow player to potentially trigger AI again or reset
        # Or, could set game_over = True
    
    return redirect(url_for('game_board'))


@app.route('/reset')
def reset_game():
    session.clear()
    flash("Game has been reset.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Flask Client App for Tic-Tac-Toe on http://127.0.0.1:5001 ...")
    app.run(debug=True, port=5001) # Run on a different port than the API