import tcod

from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from fov_functions import initialise_fov, recompute_fov
from game_states import GameStates

def main():
    # defines.
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 3
    max_rooms = 20

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colours = {
        'dark_wall': tcod.Color(5, 0, 25),
        'light_wall': tcod.Color(5, 0, 40),

        'dark_ground': tcod.Color(150, 150, 150),
        'light_ground': tcod.Color(200, 200, 50)
    }

    # Set custom font
    font_path = 'arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    window_title = 'Roguelike!'
    fullscreen = False

    # Track player
    player = Entity(0, 0, '@', tcod.black, "Player", blocks = True)
    entities = [player]

    tcod.console_set_custom_font(font_path, font_flags)
    tcod.console_init_root(screen_width, screen_height, window_title, fullscreen)

    console = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialise_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYER_TURN

    while not (tcod.console_is_window_closed()):
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(console, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colours)

        fov_recompute = False
        tcod.console_flush()
        clear_all(console, entities)

        # Input handler
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    print('You slap the ' + target.name + ' much to its annoyance.')

                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The '+ entity.name + ' contemplates life.')
            game_state = GameStates.PLAYER_TURN

if __name__ == "__main__":
    main()
