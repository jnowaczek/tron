import random

import pytest
import sys

from littlepython import Compiler

from CYLGame import GameLanguage, GameRunner
from CYLGame.Player import Room
from game import Tron as Game


def get_fuzzing_seeds(new_seed_count=100):
    previous_bad_seeds = []
    return previous_bad_seeds + [random.randint(0, sys.maxsize) for _ in range(new_seed_count)]


@pytest.mark.parametrize("seed", get_fuzzing_seeds())
@pytest.mark.parametrize("playback", [False, True])
def test_run_for_score(seed, playback):
    # Make default player bot
    compiler = Compiler()
    bot = Game.default_prog_for_bot(GameLanguage.LITTLEPY)
    prog = compiler.compile(bot)
    prog.name = "Mock"

    # get computer players
    players = []
    for _ in range(Game.get_number_of_players() - 1):
        players += [Game.default_prog_for_computer()()]
    room = Room([prog] + players, seed=seed)

    runner = GameRunner(Game)
    runner.run(room, playback=playback)
