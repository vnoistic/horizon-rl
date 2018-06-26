import tcod

from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap

def main():
    # Defines
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 3
    max_rooms = 7

    colours = {
        'dark_wall': tcod.Color(5, 0, 25),
        'dark_ground': tcod.Color(150, 150, 150)
    }

    # Set custom font
    font_path = 'arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    window_title = 'Roguelike!'
    fullscreen = False

    # Track player
    player = Entity(int(screen_width/2), int(screen_height/2), "@", tcod.white)
    npc = Entity(int(screen_width/ 2 - 5), int(screen_height/2), "@", tcod.yellow)
    entities = [npc, player]

    tcod.console_set_custom_font(font_path, font_flags)
    tcod.console_init_root(screen_width, screen_height, window_title, fullscreen)

    console = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not (tcod.console_is_window_closed()):
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        render_all(console, entities, game_map, screen_width, screen_height, colours)

        tcod.console_flush()
        clear_all(console, entities)

        # Input handler
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == "__main__":
    main()
