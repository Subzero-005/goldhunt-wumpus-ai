# Gold Hunt – Wumpus World Game with a BFS Agent

A browser grid game based on the classic *Wumpus World* AI problem. You start in the top-left corner of a hidden map and look for the gold without falling into a pit. Squares next to a pit show a warning, so you can work out where the danger is. If you get stuck, press **Run AI** and a breadth-first-search agent walks the shortest safe path to the gold, one step at a time.

## Features

- Random maps of any size from 3×3 to 15×15. Every map is checked with BFS so the gold can always be reached safely.
- Fog of war: you only see the squares you've visited and the ones next to them.
- Warning squares next to pits, like the "breeze" percepts in Wumpus World.
- A BFS agent that finds and animates the shortest path that avoids pits.
- A Flask JSON API behind a plain HTML/CSS/JS front end.

## Tech stack

Python · Flask · vanilla JavaScript · pytest

## Running it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open http://127.0.0.1:5000, choose a grid size and press **Start Game**.

## API

| Method | Endpoint | Body | Returns |
|---|---|---|---|
| POST | `/start` | `{"size": 6}` | the visible grid and player position |
| POST | `/move` | `{"direction": "up" \| "down" \| "left" \| "right"}` | the updated grid and game status |
| GET | `/ai` | – | the step-by-step path the BFS agent takes to the gold |

## Tests

```bash
pip install pytest
python -m pytest
```

The tests check that every generated map can be solved, that the agent never steps on a pit, that the player can't leave the grid, and that the API rejects bad input.
