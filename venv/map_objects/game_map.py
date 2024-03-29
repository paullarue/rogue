import tcod
from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from components.fighter import Fighter
from components.ai import BasicMonster
from components.item import Item
from entity import Entity
from render_functions import RenderOrder
from item_functions import heal


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player,
                 entities, max_monsters_per_room, max_items_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size , room_max_size)
            h = randint(room_min_size , room_max_size)

            # random position without leaving boundaries of map
            x = randint(0 , map_width - w -1)
            y = randint(0, map_height - h -1)

            # new rect object hits that yeet lol
            new_room = Rect(x, y, w, h)

            # See if other rooms intersect with this new room
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else: # No intersections, room is valid
                # "Paint" rooms tiles
                self.create_room(new_room)

                # Get center coords
                (new_x , new_y) = new_room.center()

                if num_rooms == 0:
                    # First new room, "spawn player"
                    player.x = new_x
                    player.y = new_y
                else: # All rooms after the first, connect to previous room with tunnel
                    # Get center coords of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Flip a coin
                    if randint(0,1):
                        # First move horizonatally, then vertically
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                    else:
                    # Or first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                # Append new room to the list
                rooms.append(new_room)
                num_rooms += 1




    def create_room(self, room):
        # Creates a room by making tiles in a rectangle passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1,x2), max(x1,x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1,y2), max(y1,y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # Places monsters inside rooms
    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # Spawn monsters
        for i in range(number_of_monsters):
            # Choose random location within room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # 80% chance to spawn an orc
                if randint(0, 100)< 80:
                    fighter_component = Fighter(hp=10, defense = 0, power =3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                # 20% chance to spawn a troll
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai = ai_component)
                entities.append(monster)

        # Spawn items
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item(use_function=heal, amount=4)
                item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)

                entities.append(item)


    def is_blocked(self,x,y):
        if self.tiles[x][y].blocked:
            return True
        return False


