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
event_log = []

def save_log_to_file():
    with open("events.txt", "a") as file:
        file.write("==== New Game Session ====\n")
        for entry in event_log:
            file.write(entry + "\n")
        file.write("\n")


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
    global current_turn, winner, event_log
    color = turn_order[current_turn]
    roll = random.randint(1, 6)
    current_pos = players[color]
    new_pos = current_pos + roll

    log_entry = f"{color.title()} rolled a {roll}."

    if new_pos == NUM_SQUARES:
        players[color] = new_pos
        winner = color
        scoreboard[color] += 1
        log_entry += f" They landed exactly on square {NUM_SQUARES} and won the game!"
        event_log.append(log_entry)
        save_log_to_file()  # Save the session log to events.txt
    elif new_pos < NUM_SQUARES:
        for other_color in players:
            if other_color != color and players[other_color] == new_pos:
                players[other_color] = 1
                log_entry += f" They landed on {other_color.title()} and sent them back to start!"
        players[color] = new_pos
        log_entry += f" They moved to square {new_pos}."
    else:
        log_entry += f" They needed exactly {NUM_SQUARES - current_pos}, so they stayed in place."

    event_log.append(log_entry)
    current_turn = (current_turn + 1) % len(turn_order)
    return redirect(url_for('board'))


@app.route('/restart')
def restart():
    reset_game_state()
    event_log.clear()
    return redirect(url_for('board'))


if __name__ == '__main__':
    app.run(debug=True)
