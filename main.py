#kernel32 = ctypes.windll.kernel32
#kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

import CORE as Zc
from CORE.functions import log
from aiohttp import web
import socketio
import random
import string

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
app.router.add_static('/static', 'public')

def randomString(stringLength=3):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))

def in_dict(dic, key):
  if key in dic:
    return True
  else:
    return False

CARDSET = Zc.cardsets["tournament"]["1v1_np"]

clients = {} # SID -> USERNAME
games_names = {} # SID -> GAME NAME
gamestates = {} # GAME NAME -> GAMESTATE
cardsets = {} # GAME NAME -> CARDSET
masters = {} # GAME NAME -> SID
rules = {} # GAME NAME -> RULES
boards = {} # GAME NAME -> BOARD
player_indexes = {} # SID -> PLAYER INDEX

# AUTH----------------------
@sio.event
async def connect(sid, environ):
  log(f'connect {sid}')
  clients[sid] = "anonymous"
  games_names[sid] = None

@sio.on("my name is")
async def my_name_is(sid, data):
  clients[sid] = data["name"]
  log(f'{sid} is {data["name"]}')

#---------------------------

@sio.on("create game")
async def create_game(sid, data):
  game_name = randomString()
  games_names[sid] = game_name


@sio.on("rules chosen")
async def rules_choosen(sid, data):
  category = data["cat"]
  element = data["el"]
  game_name = games_names[sid]
  rules[game_name] = Zc.rules[category][element]

  sending = {}
  for cat in Zc.boards.keys():
    sending[cat] = {}
    for el in Zc.boards[cat].keys():
      sending[cat][el] = Zc.boards[cat][el].__str__(color=False)

  if masters[game_name] != sid: return
  await sio.emit("available boards", {"boards":sending}, room=sid)


@sio.on("board chosen")
async def board_chosen(sid, data):
  category = data["cat"]
  element = data["el"]
  game_name = games_names[sid]
  boards[game_name] = Zc.boards[category][element]
  if masters[game_name] != sid: return

  

  await sio.emit("game created", {"game_name":game_name}, room=game_name)
  log(f'game \"{game_name}\" successfuly configured by {clients[sid]}')


async def leave_game(sid):
  if games_names[sid] == None: return
  game_name = games_names[sid]
  sio.leave_room(sid, game_name)
  log(f'game \"{game_name}\" left by {clients[sid]}')
  await sio.emit("player left", data=clients[sid], room=game_name) # TODO
  if masters[games_names[sid]] == sid:
    await abort_game(sid, games_names[sid]) 
  games_names[sid] = None


async def abort_game(sid, game_name):
  log(f'game \"{game_name}\" aborted by {clients[sid]}')
  await sio.emit("game aborted", data=game_name, room=game_name) # TODO
  for client in games_names: 
    if games_names[client] == game_name and masters[game_name] != client:
      await leave_game(client)


@sio.on("join game")
async def join_game(sid, data):
  game_name = data
  await leave_game(sid)
  games_names[sid] = game_name
  sio.enter_room(sid, game_name)
  await sio.emit("player joined", data=clients[sid], room=game_name) # TODO
  log(f'game \"{game_name}\" joined by {clients[sid]}')


@sio.event
async def disconnect(sid):
  await leave_game(sid)

  log(f'{clients[sid]} just disconnected ')
  del clients[sid]
  del games_names[sid]

if __name__ == '__main__':
  web.run_app(app)