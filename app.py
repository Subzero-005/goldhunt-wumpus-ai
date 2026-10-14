
from flask import Flask, render_template, request, jsonify
from game_logic import Game

MIN_SIZE, MAX_SIZE = 3, 15

app = Flask(__name__)
game = None


def no_game():
    return jsonify({"error": "Start a game first"}), 400

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global game
    data = request.get_json(silent=True) or {}
    try:
        size = int(data.get('size'))
    except (TypeError, ValueError):
        return jsonify({"error": f"Grid size must be a number between {MIN_SIZE} and {MAX_SIZE}"}), 400
    if not MIN_SIZE <= size <= MAX_SIZE:
        return jsonify({"error": f"Grid size must be between {MIN_SIZE} and {MAX_SIZE}"}), 400
    game = Game(size)
    return jsonify({"status": "started", "grid": game.get_visible_grid(), "player": game.player_pos})

@app.route('/move', methods=['POST'])
def move():
    if game is None:
        return no_game()
    direction = (request.get_json(silent=True) or {}).get('direction')
    try:
        game.move_player(direction)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"grid": game.get_visible_grid(), "player": game.player_pos, "status": game.status})

@app.route('/ai')
def run_ai():
    if game is None:
        return no_game()
    steps = game.run_ai_trace()
    return jsonify({"steps": steps})


if __name__ == '__main__':
    app.run(debug=True)
