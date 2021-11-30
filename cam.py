from mcdreforged.api.all import *
import re
import json
import math
from typing import NamedTuple


class Position(NamedTuple):
    x: float
    y: float
    z: float


f = open('C:/Users/whes1/Desktop/server/plugins/playerdata.json', 'r')
line = f.read()
Json = json.loads(line)

PLUGIN_METADATA = {
    'id': 'Free_Camera_whes1015',
    'version': '1.0.0',
    'name': 'Free_Camera'
}


def process_coordinate(text: str) -> Position:
    data = text[1:-1].replace('d', '').split(', ')
    data = [(x + 'E0').split('E') for x in data]
    assert len(data) == 3
    return Position(*[float(e[0]) * 10 ** int(e[1]) for e in data])


def on_info(server: PluginServerInterface, info: Info):
    global name
    if info.is_player and info.content == '!!cam':
        name = info.player
        if server.rcon_query('data get entity {} playerGameType'.format(name)).find('3') == -1:
            position = process_coordinate(re.search( r'\[.*]', server.rcon_query('data get entity {} Pos'.format(name))).group())
            Json[name+'X'] = position.x
            Json[name+'Y'] = position.y
            Json[name+'Z'] = position.z
            #Json[name+'RotX'] = server.rcon_query('data get entity {} Rotation[0]'.format( name)).replace("{} has the following entity data: ".format(name), "").replace('f', "")
            #Json[name+'RotY'] = server.rcon_query('data get entity {} Rotation[1]'.format(name)).replace("{} has the following entity data: ".format(name), "").replace('f', "")
            if server.rcon_query('data get entity {} Dimension'.format(name)).find('minecraft:the_nether') != -1:
                Json[name+'D'] = 'minecraft:the_nether'
            elif server.rcon_query('data get entity {} Dimension'.format(name)).find('minecraft:the_end') != -1:
                Json[name+'D'] = 'minecraft:the_end'
            elif server.rcon_query('data get entity {} Dimension'.format(name)).find('minecraft:overworld') != -1:
                Json[name+'D'] = 'minecraft:overworld'
            f = open('C:/Users/whes1/Desktop/server/plugins/playerdata.json', 'w')
            f.write(json.dumps(Json))
            f.close()
            server.execute('gamemode spectator {}'.format(name))
        else:
            server.execute('execute as {} in {} run teleport {} {} {}'.format( name, Json[name+'D'], Json[name+'X'], Json[name+'Y'], Json[name+'Z']))
            server.execute('gamemode survival {}'.format(name))
    elif info.is_player and info.content.startswith('!!tp'):
        data=info.content.split(' ')
        if server.rcon_query('data get entity {} playerGameType'.format(data[1])).find('3') != -1 and server.rcon_query('data get entity {} playerGameType'.format(data[2])).find('3') != -1:
            server.execute('tp {} {}'.format(data[1],data[2]))

def on_load(server, old):
    server.register_help_message('!!cam', '切換自由視角')
