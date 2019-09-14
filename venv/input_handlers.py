import tcod

def handle_keys(key):
    # Movement Keys
    if key.vk == tcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0,1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1,0)}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Full-screen
        return {'fullscreen': true}

    elif key.vk == tcod.KEY_ESCAPE:
        # Esc: exit the game
        return {'exit': True}

    # No key was pressed
    return {}

