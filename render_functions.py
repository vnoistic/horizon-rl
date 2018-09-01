import tcod

def render_all (console, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colours):
    # Calls draw_entity for all objects in entities
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(console, x, y, colours.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, colours.get('light_ground'), tcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(console, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    for entity in entities:
        draw_entity(console, entity, fov_map)

    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

def clear_all (console, entities):
    # Calls clear_entity for all objects in entities
    for entity in entities:
        clear_entity(console, entity)

def draw_entity(console, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
    # Set colour of the character to the entity colour and puts the entity on the console
        tcod.console_set_default_foreground(console, entity.colour)
        tcod.console_put_char(console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity (console, entity):
    # Puts a blank character at the location of an entity
    tcod.console_put_char(console, entity.x, entity.y, " ", tcod.BKGND_NONE)
