import tcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                monster.fighter.attack(target)
