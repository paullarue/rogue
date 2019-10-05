import tcod
from game_states import GameStates

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys()
    elif game_state == GameStates.SHOW_INVENTORY:
        return handle_inventory_keys(key)

    return {}


def handle_player_turn_keys(key):
    # Get character of keypress
    key_char = chr(key.c)
    # Movement Keys including cardinal directions and diagonal directions
    if key.vk == tcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}

    elif key.vk == tcod.KEY_DOWN or key_char == 'j':
        return {'move': (0,1)}

    elif key.vk == tcod.KEY_LEFT or key_char == 'h'"":
        return {'move': (-1, 0)}

    elif key.vk == tcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1,0)}

    # Diagonal directions
    elif key_char == 'y':
        return {'move': (-1,-1)}

    elif key_char == 'u':
        return {'move': (1, -1)}

    elif key_char == 'b':
        return {'move': (-1, 1)}

    elif key_char == 'n':
        return {'move': (1, 1)}

    # "Grab" item from ground
    elif key_char == 'g':
        return {'pickup': True}

    # Show inventory
    elif key_char == 'i':
        return{'show_inventory': True}


    # Utility Keys
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Full-screen
        return {'fullscreen': true}

    elif key.vk == tcod.KEY_ESCAPE:
        # Esc: exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': true}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Full-screen
        return {'fullscreen': true}

    elif key.vk == tcod.KEY_ESCAPE:
        # Esc: exit the game
        return {'exit': True}

def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return{'exit': True}

    return {}

