# AI Challenge: Werewolves VS Vampires

## Installation guide
All you have to do is run this command to install the needed librairies:
```
pip install -r requirements.txt
```

## File Content:

The testKit folder contains the file provided to all groups and it contains the server launcher, map generator and game settings.

All our code is in Python folder:
* state.py: defines the class State and the representation of the game and positions.
* Heuristic.py: Calculates the heuristic as explained in our project report
* Alpha_beta.py: Implements alpha-beta algorithm

* tcpServer/echo_client.py: Handle the communication with the server
* Action.py: Defines the class Action that represents the mouvement to be played.
* config.py: Contains our strategy parameters. Mainly the number of steps that we foresee in the future and the maximum number of possible plays that the algorithm takes into account at each level.
* main.py: launches the game (connecting to server and playing)
* constraint_programming.py: a method that we tried but did NOT use finally.
* possible_plays.py: given a certain map and certain situation, it gives the possible plays to do in the next round.
* possible_plays_improved.py: the names explains it all.



