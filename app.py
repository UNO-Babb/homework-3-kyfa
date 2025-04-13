from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)

# Constants
NUM_SQUARES = 60
turn_order = ["red", "blue"]
players = {}
current_turn = 0
winner = None
scoreboard = {color: 0 for color in turn_order}

def reset_game_state():
    global players, current_turn, winner
    players = {color: 1 for color in turn_order}  # Start on square 1
    current_turn = 0
    winner = None

reset_game_state()

@app.route('/')
def board():
    if winner:
        return render_template('winner.html', winner=winner, scoreboard=scoreboard)
    return render_template('board.html',
                           players=players,
                           num_squares=NUM_SQUARES,
                           current_player=turn_order[current_turn])

@app.route('/move')
def move():
    global current_turn, winner
    color = turn_order[current_turn]
    roll = random.randint(1, 6)
    current_pos = players[color]
    new_pos = current_pos + roll

    if new_pos == NUM_SQUARES:
        players[color] = new_pos
        winner = color
        scoreboard[color] += 1
    elif new_pos < NUM_SQUARES:
        # Check if any other player is on that square
        for other_color in players:
            if other_color != color and players[other_color] == new_pos:
                players[other_color] = 1  # Send them back to start
        players[color] = new_pos
    # else: rolled too high, no move

    current_turn = (current_turn + 1) % len(turn_order)
    return redirect(url_for('board'))

@app.route('/restart')
def restart():
    reset_game_state()
    return redirect(url_for('board'))

if __name__ == '__main__':
    app.run(debug=True)
