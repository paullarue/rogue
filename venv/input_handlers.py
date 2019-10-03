import tcod

def handle_keys(key):
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

    elif key_char == 'g':
        return {'pickup': True}


    # Utility Keys
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Full-screen
        return {'fullscreen': true}

    elif key.vk == tcod.KEY_ESCAPE:
        # Esc: exit the game
        return {'exit': True}

    # No key was pressed
    return {}

