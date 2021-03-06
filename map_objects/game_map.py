import tcod
from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from entity import Entity

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialise_tiles()

    def initialise_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        # Dungeon Generation here

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Randomise room sizes
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)

            # Randomise positions
            x = randint(0, map_width - width - 1)
            y = randint(0, map_height - height - 1)

            # Generate a new room
            new_room = Rect(x, y, width, height)

            # Stop if room intersects
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # Create the room if it doesn't intersect, store the centre variable
                self.create_room(new_room)
                (new_x, new_y) = new_room.centre()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].centre()

                    # Randomise tunnel generation
                    if randint(0, 1) == 1:
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.create_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room)

                rooms.append(new_room)
                num_rooms += 1



    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_horizontal_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_vertical_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)
        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'w', tcod.red, "wraith")
                else:
                    monster = Entity(x, y, 'g', tcod.blue, "ghost", blocks = True)

                entities.append(monster)
