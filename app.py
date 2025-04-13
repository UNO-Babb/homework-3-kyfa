from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)

# Constants
NUM_SQUARES = 60
players = {}
turn_order = ["red", "blue"]
current_turn = 0
winner = None

def reset_game():
    global players, current_turn, winner
    players = {color: 0 for color in turn_order}
    current_turn = 0
    winner = None

reset_game()

@app.route('/')
def board():
    if winner:
        return render_template('winner.html', winner=winner)
    return render_template('board.html', players=players, num_squares=NUM_SQUARES, current_player=turn_order[current_turn])

@app.route('/move')
def move():
    global current_turn, winner
    color = turn_order[current_turn]
    roll = random.randint(1, 6)
    new_position = players[color] + roll

    if new_position == NUM_SQUARES - 1:
        players[color] = new_position
        winner = color
    elif new_position < NUM_SQUARES:
        players[color] = new_position

    current_turn = (current_turn + 1) % len(turn_order)
    return redirect(url_for('board'))

@app.route('/restart')
def restart():
    reset_game()
    return redirect(url_for('board'))

if __name__ == '__main__':
    app.run(debug=True)
