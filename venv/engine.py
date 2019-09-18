import tcod
from input_handlers import handle_keys
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap



def main():

        # Game and map constants
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

        # FoV Variables
    fov_algoritm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': tcod.Color(0,0,100),
        'dark_ground': tcod.Color(50,50,150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200,180,50)
    }


    player = Entity(0, 0, '@', tcod.white)
    entities = [player]


    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'tcodtutorial revised', False)
    con = tcod.console_new(screen_width , screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x +dx, player.y +dy):
                player.move(dx,dy)
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen((not tcod.console_is_fullscreen()))

if __name__ == '__main__':
    main()