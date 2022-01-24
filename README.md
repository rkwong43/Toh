# Toh

WORK IN PROGRESS \
Last Edited: 5/1/2020

_NOTE: Meant to be run on Python 3.7 or any compatible version with Pygame_

**DOWNLOAD A DEMO [HERE.](https://drive.google.com/file/d/1IG5TXE3D65jzQhSIlu_q3-AKYB8aY6KX/view?usp=sharing)**
Currently the demo is only compatible with Windows operating systems. Unpack the .zip and run the .exe.

**SOURCE CODE:** [https://github.com/rkwong43/Toh](https://github.com/rkwong43/Toh)

**GITHUB PAGES:** [https://rkwong43.github.io/Toh/](https://rkwong43.github.io/Toh/)

**CONTROLS:** Menu navigation using WASD or arrow keys, select using Space. Go backwards a menu using Esc.

Personal project using self-taught Python and the Pygame library. Is currently under development.

* Features decoupled views, models, controllers, and artificial intelligence for behavior of enemies.
* Has a collision detection algorithm for detecting when projectiles and ships intersect.
* Supports different frame rates (default=60) while keeping the same gameplay.
* Controller and main allow for restarting the game upon end.
* Menu is implemented in the form of a tree structure.
* Unique algorithms for different enemy types and projectiles such as homing missiles.
* Pixel art and effects created by myself, Roger Kwong.
* In-game music created by [Scott Buckley](https://www.scottbuckley.com.au/) and used under the Creative Commons Attribution International 4.0 license. Current tracks used are [Undertow](https://www.scottbuckley.com.au/library/undertow/) and [Endurance](https://www.scottbuckley.com.au/library/?s=endurance).
* Backgrounds and sound effects are temporary until custom ones are created.

 As of now, all weapons and ships are permanently unlocked for the player for demo purposes.

## Current Game Features

Describes the current gameplay features inside the game.

* Difficulty Settings:
  * Difficulty affects the rate at which enemies spawn, their statistics such as health, shielding, and movement speed, their fire rate, and the amount of experience required to level up.
* Survival
  * Classic:
    * Survive against hordes of enemy ships.
    * Every type of enemy in the game is featured inside Classic.
    * Leveling up will increase the player's health, shield, shield regeneration, fire rate, and weapon damage. Level thresholds are dependent on score and is doubled every level.
    * Every weapon is available for use.
    * Types of enemies spawned are chosen randomly based on an assigned combat rating and the total combat rating allowed for the current wave.
    * Every wave, the total combat rating is reset and increased by a certain amount.
  * Heaven:
    * Survive against hordes of difficult enemy ships.
    * Every larger enemy ship is featured in Heaven Survival.
    * Leveling is the same as in Classic.
    * Every weapon is available for use.
    * Enemy spawning is the same as in Classic.
  * Fate:
    * Classic survival but with a twist.
    * Weapon randomized every few waves.
    * Same scoring system and spawning as in Classic.
  * Onslaught:
    * Classic survival but enemies are much more difficult.
    * Allied ships spawn throughout the game.
    * Enemies will target the closest allied ship or the player.
    * Same scoring system and spawning as in Classic.
* Challenge
  * Titan Slayer:
    * Duel against a large Titan enemy ship with the base weapons.
    * All weapons are available for use.
    * Score is not relevant, game victory returns the time taken to destroy the Titan.
    * Difficulty affects the health and fire rate of the Titan and its turrets.
  * Mandible Madness:
    * Fight against waves of Mandibles and Motherships.
    * Final score is calculated based on time taken.
    * Final wave includes two mini-bosses.
  * Spectral:
    * Fight against waves of hidden enemies.
    * Time based game mode, so final score is based on how quickly the player completes every wave.
* Tutorial
  * Leads the player through basic controls (WASD or arrows to move, SPACE to shoot).
  * Gives the player a sample enemy to destroy.
  * Introduces the concept of health, shield, and how each increase or regenerate.
  * Informs the player that ESC can be used to pause, and if paused, BACKSPACE will exit the game to the title screen.
* Hangar
  * Consists of ships, weapons, and enemies to view.
  * Each page displays the selected entity and limited stats on its base form.
  * Uses a smaller model to simulate firing of shown weapons of the player and the selected enemy.

## Future Features

Features currently under development or planned for the future.

* Implementing global high scores and user accounts (MongoDB, Heroku, Flask?, MLab).
* Multiplayer and mouse support for aiming or local multiplayer.
* Expanding on enemy artificial intelligence.
* Streamlined creation for enemies and players.
* Adding or creating a custom ship for the player.
* Adding a story mode with chapters.
* Adding a constant progression system (for release of game)
* Locking weapons until unlocked (for final release of game)
* Writing high scores and statistics to a file.
* Adding settings for modifying resolution, frame rate, and sound/music volume.
* More game modes, enemies, and weapons!

## How to Add Ships

    * Create sprites for the animated, base, damaged, and shielded images, placing them into
    a spritesheet.
    * Create an ID for them, name the spritesheet ID.png.
    * Place the images into the images folder under resources.
    * Add the ID to their respective enum.
    * Create a class for the new ship, extending the Ship class, or Enemy class if the
    new ship is an enemy.
    * Add the ship's stats to the ship_stats.py file.
    * If enemy ship, alter the enemy_generator.py file and add the new ID to the
    dictionary of IDs : classes.
