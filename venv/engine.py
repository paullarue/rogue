import tcod
from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from game_states import GameStates
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog, Message
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

    # Entity limits
    max_monsters_per_room = 3
    max_items_per_room = 2

    colors = {
        'dark_wall': tcod.Color(0,0,100),
        'dark_ground': tcod.Color(50,50,150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200,180,50)
    }

    fighter_component = Fighter(hp=30,defense=2,power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order = RenderOrder.ACTOR,
                    fighter = fighter_component, inventory=inventory_component)
    entities = [player]


    tcod.console_set_custom_font('Bisasam_24x24.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)

    tcod.console_init_root(screen_width, screen_height, 'tcodtutorial revised', False,renderer=tcod.RENDERER_SDL2)
    con = tcod.console.Console(screen_width , screen_height)
    
    panel = tcod.console.Console(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player,
                      entities, max_monsters_per_room, max_items_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, mouse, colors, game_state)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')

        player_turn_results = []


        # Move and/or attack action
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
        # Picking up an item
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.',tcod.yellow))


        # Open inventory
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            print(item.name)

        # Exit game
        if exit:
            if game_state == GameStates.SHOW_INVENTORY:
                # Escape from inventory menu back to game
                game_state = previous_game_state
            else:
                return True

        # Set to fullscreen
        if fullscreen:
            tcod.console_set_fullscreen((not tcod.console_is_fullscreen()))

        ## PROCESS PLAYER'S TURN
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN



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