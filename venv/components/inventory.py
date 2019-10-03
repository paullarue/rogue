import tcod
from game_messages import Message

# Component for inventory
class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.item) >= self.capacity:
            # Cant carry more than inventory capacity
            results.append({
                'item_added': None,
                'message': Message('You cannot carry more, your inventory is full', tcod.yellow)
            })
        else:
            # success!
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), tcod.blue)
            })

            self.items.append(item)

        return results