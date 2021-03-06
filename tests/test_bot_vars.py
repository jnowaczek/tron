from CYLGame.Player import Prog
from pytest_mock import mocker

from game import Tron, Bike


class MockProg(Prog):
    def __init__(self):
        self.key = None
        self.state = {}
        self.options = {}
        self.last_state = None
        self.name = "Mock"

    def run(self, state=None, **kwargs):
        self.last_state = state
        state = dict(self.state)
        state["move"] = ord(self.key)
        return state


def make_tron_map(game, *taken_spots):
    map_array = []
    for w in range(0, game.MAP_WIDTH):
        width_arr = []
        for h in range(0, game.MAP_HEIGHT):
            width_arr.append(game.OPEN)
        map_array.append(list(width_arr))
    for spot in taken_spots:
        map_array[spot[0]][spot[1]] = game.TAKEN
    return map_array


def make_tron_sensors(game, player, default=None, **kargs):
    if default is None:
        default = game.OPEN
    d = {}
    for i in range(player.NUM_OF_SENSORS):
        d["s{}".format(i+1)] = default
    d.update(kargs)
    return d


def test_start_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"
    vars = game.get_vars(player)
    correct_vars = {**make_tron_sensors(game, player, default=0),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x, y))}

    assert vars == correct_vars


def test_start_vars_2(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 4, 5
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"
    vars = game.get_vars(player)
    correct_vars = {**make_tron_sensors(game, player, default=0),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x, y))}

    assert vars == correct_vars


def test_move_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 4, 5
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_wall_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": -1}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.WALL),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_wall2_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": -1}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.WALL),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_wall3_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 1, 1
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": -1,
                  "s2x": -1, "s2y": 0}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.OPEN, s2=game.TAKEN),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_wall4_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, game.MAP_HEIGHT-2
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": -1,
                  "s2x": -1, "s2y": 0}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.OPEN, s2=game.TAKEN),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_wall5_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, game.MAP_HEIGHT-1
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "d"  # move right
    prog.state = {"s1x": 0, "s1y": 1,
                  "s2x": -1, "s2y": 0}

    player.run_turn(None)
    game.do_turn()
    vars = game.get_vars(player)

    correct_vars = {**make_tron_sensors(game, player, default=game.TAKEN, s1=game.WALL),
                    "height": game.MAP_HEIGHT,
                    "width": game.MAP_WIDTH,
                    "map": make_tron_map(game, (x+1, y), (x, y))}

    assert vars == correct_vars


def test_crash_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 0, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "a"  # move left

    player.run_turn(None)
    game.do_turn()
    assert player.derezzed
    assert game.get_map_array() == make_tron_map(game)  # make sure the player has been removed from the map.


def test_crash_with_path_vars(mocker):
    game = Tron(None)
    mocker.patch.object(game, 'place_bike')
    x, y = 1, 0
    prog = MockProg()

    game.init_board()
    game.place_bike.return_value = Bike((x, y), chr(239), prog, game.get_move_consts())
    player = game.create_new_player(prog)
    game.start_game()
    prog.key = "a"  # move left
    player.run_turn(None)
    game.do_turn()
    prog.key = "a"  # move left
    player.run_turn(None)
    game.do_turn()
    assert player.derezzed
    assert game.get_map_array() == make_tron_map(game)  # make sure the player has been removed from the map.
