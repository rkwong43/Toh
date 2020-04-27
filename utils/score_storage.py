import json
import random
import string

from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.gamemode_id import GameModeID
from src.utils.ids.player_id import PlayerID
from src.utils.ids.weapon_id import WeaponID

data = {}


def construct_data():
    letters = string.ascii_letters
    random.seed()
    random_letter = random.choice(letters)
    random_number = str(random.randint(100, 999))
    data["PILOT"] = {"NAME": "Pilot-" + random_letter + random_number,
                     "WEAPON": WeaponID.GUN.value,
                     "SHIP": PlayerID.CITADEL.value}
    scores = {}
    for game_mode in GameModeID:
        not_attempted = {"SHIP": PlayerID.CITADEL.value, "WEAPON": WeaponID.GUN.value, "SCORE": 0}
        results = {}
        for difficulty in DifficultyID:
            results[difficulty.value] = not_attempted.copy()
        scores[int(game_mode.value)] = results
    data["SCORES"] = scores
    with open("data.json", "w") as outfile:
        json.dump(data, outfile)


read = False
while not read:
    try:
        with open('data.json') as f:
            data = json.load(f)
            read = True
            f.close()
    except FileNotFoundError:
        construct_data()

"""Writes and reads scores and the pilot name from a file."""


def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)
        f.close()


"""Checks all the existing gamemodes and adds them if they do not exist.
"""


def update_gamemodes():
    for gamemode in GameModeID:
        try:
            test = data["SCORES"][gamemode.value]["SHIP"]
        except KeyError:
            data["SCORES"][int(gamemode.value)] = {"SHIP": PlayerID.CITADEL.value, "WEAPON": WeaponID.GUN.value, "SCORE": 0}
    save_data()
