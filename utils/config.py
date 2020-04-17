
from src.utils import score_storage
from src.utils.ids.player_id import PlayerID
from src.utils.ids.weapon_id import WeaponID

"""Defines global variables to be used across all of the game.
"""

display_width = 1024
display_height = 720
ship_size = 90
game_fps = 60
game_title = 'Tears Over Heaven'

# Player ship and weapon chosen:
try:
    player_ship = PlayerID(score_storage.data["PILOT"]["SHIP"])
    weapon = WeaponID(score_storage.data["PILOT"]["WEAPON"])
    player_name = score_storage.data["PILOT"]["NAME"]
except KeyError:
    score_storage.construct_data()
    player_ship = PlayerID(score_storage.data["PILOT"]["SHIP"])
    weapon = WeaponID(score_storage.data["PILOT"]["WEAPON"])
    player_name = score_storage.data["PILOT"]["NAME"]
