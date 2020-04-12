from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.game_id import GameID
from src.utils.ids.gamemode_id import GameModeID

"""Holds the descriptions for all the game modes or menu options in the game.
"""
descriptions = {
    # Difficulties
    DifficultyID.EASY: ["Enemy quality, fire rate, and spawning are decreased.",
                        " Destroy all who oppose you."],
    DifficultyID.NORMAL: ["The enemy strikes with ferocity.", "Stand strong and take them down."],
    DifficultyID.HARD: ["Enemy quality, fire rate, and spawning are increased.",
                        "Their endless onslaught will wear down any pilot.", "The way the game is meant to be played."],
    # Game modes
    GameID.TUTORIAL: ["Learn the minimum to survive out in space."],
    GameID.SURVIVAL: ["Survive against endless waves of increasing difficulty."],
    GameID.CHALLENGE: ["Missions for the true elite."],
    GameID.STORY: ["Experience the start of the war. Currently not available"],
    GameID.HANGAR: ["View the database of enemies, ships, and weapons available."],
    GameID.SETTINGS: ["Configure your settings. Currently not available."],
    # Survival
    GameModeID.CLASSIC: ["Survive against endless waves of enemies."],
    GameModeID.HEAVEN: ["Take on the enemy's most elite warships."],
    GameModeID.MANDIBLE_MADNESS: ["Uh oh, you've provoked a hive of bees."],
    GameModeID.FATE: ["It's up to fate whether you survive."],
    # Challenge
    GameModeID.TITAN_SLAYER: ["Duel a massive Titan warship alone. Prepare for death."]
}
