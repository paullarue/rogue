import tcod
from game_states import GameStates


def kill_player(player):
    player.char = '%'
    player. color = tcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name

    return death_message

