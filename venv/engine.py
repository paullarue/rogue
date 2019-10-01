import tcod
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from game_states import GameStates
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog
from render_functions import clear_all, render_all, RenderOrder
from map_objects.game_map import GameMap
from setuptools.command.easy_install import easy_install


def main():

    # Game and map constants
    screen_width = 80
    screen_height = 50

    # HP Bar paramters
    bar_width = 20

    # Panel for bars
    panel_height = 7
    panel_y = screen_height - panel_height

    # Message bar
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Map size
    map_width = 80
    map_height = 43

    # Room parameters
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

    fighter_component = Fighter(hp=30,defense=2,power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order = RenderOrder.ACTOR, fighter = fighter_component)
    entities = [player]


    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'tcodtutorial revised', False,renderer=tcod.RENDERER_SDL2)
    con = tcod.console.Console(screen_width , screen_height)
    
    panel = tcod.console.Console(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, colors)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move

            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen((not tcod.console_is_fullscreen()))

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)


        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                # If entity has 'ai', i.e. can move or attack etc, get
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()