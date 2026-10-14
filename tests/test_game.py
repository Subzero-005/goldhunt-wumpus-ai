import pytest

from app import app
from game_logic import Game


@pytest.mark.parametrize("size", [3, 5, 10])
def test_gold_is_always_reachable(size):
    for _ in range(50):
        game = Game(size)
        assert game.validate_path()
        assert game.gold_pos != [0, 0]
        assert game.grid[0][0] != "D"


def test_ai_reaches_gold_without_hitting_a_pit():
    for _ in range(50):
        game = Game(6)
        steps = game.run_ai_trace()
        assert steps[-1]["pos"] == game.gold_pos
        assert steps[-1]["status"] == "You Won - Found the Gold!"
        assert all(game.grid[x][y] != "D" for x, y in (s["pos"] for s in steps))


def test_player_cannot_leave_the_grid():
    game = Game(4)
    game.move_player("up")
    game.move_player("left")
    assert game.player_pos == [0, 0]


def test_unknown_direction_is_rejected():
    with pytest.raises(ValueError):
        Game(4).move_player("diagonal")


@pytest.fixture
def client():
    import app as app_module
    app_module.game = None
    return app.test_client()


def test_move_before_start_returns_400(client):
    assert client.post("/move", json={"direction": "up"}).status_code == 400
    assert client.get("/ai").status_code == 400


@pytest.mark.parametrize("size", [None, "abc", 1, 99])
def test_invalid_size_returns_400(client, size):
    assert client.post("/start", json={"size": size}).status_code == 400


def test_full_game_flow(client):
    res = client.post("/start", json={"size": 5})
    assert res.status_code == 200
    assert res.get_json()["grid"][0][0] == "player"
    assert client.post("/move", json={"direction": "right"}).status_code == 200
    assert client.get("/ai").get_json()["steps"]
