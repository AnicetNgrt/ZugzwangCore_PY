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

names = set()
games_names = set()

clients = {} # SID -> USERNAME
players_games = {} # SID -> GAME NAME
gamestates = {} # GAME NAME -> GAMESTATE
cardsets = {} # GAME NAME -> CARDSET
masters = {} # GAME NAME -> SID
rules = {} # GAME NAME -> RULES
boards = {} # GAME NAME -> BOARD
joinable = {} # GAME NAME -> IS JOINABLE
players = {} # SID -> LIST OF PLAYERS
gamestates = {} # GAME NAME -> GAMESTATE
cardsets = {} # GAME NAME -> CARDSET
masters = {} # GAME NAME -> SID
rules = {} # GAME NAME -> RULES
boards = {} # GAME NAME -> BOARD
joinable = {} # GAME NAME -> IS JOINABLE
players = {} # SID -> LIST OF PLAYERS

# AUTH----------------------
@sio.event
async def connect(sid, environ):
  log(f'connect {sid}')
  clients[sid] = "anon "+randomString()
  while clients[sid] in names:
    clients[sid] = "anon "+randomString()
  
  names.add(clients[sid])
  players_games[sid] = None

@sio.on("my name is")
async def my_name_is(sid, data):
  if data["name"] in names:
    await sio.emit("failure", {
      "nature":"name refused",
      "reason":"name already taken"
    }, room=sid) # TODO
    return
  names.add(data["name"])
  names.remove(clients[sid])
  clients[sid] = data["name"]
  log(f'{sid} is {data["name"]}')

#---------------------------

@sio.on("create game")
async def create_game(sid, data):
  game_name = randomString()
  while game_name in games_names:
    game_name = randomString()
  
  games_names.add(game_name)
  players_games[sid] = game_name
  masters[game_name] = sid
  joinable[game_name] = False


@sio.on("rules chosen")
async def rules_choosen(sid, data):
  category = data["cat"]
  element = data["el"]
  game_name = players_games[sid]
  rules[game_name] = Zc.rules[category][element]
  rule = rules[game_name]

  max_player = rule["player per team"] * rule["team count"]
  players[game_name] = []
  for i in range(0, max_player):
    players[game_name].append(None)

  sending = {}
  for cat in Zc.boards.keys():
    sending[cat] = {}
    for el in Zc.boards[cat].keys():
      sending[cat][el] = Zc.boards[cat][el].__str__(color=False)

  if masters[game_name] != sid: return
  await sio.emit("available boards", {"boards":sending}, room=sid)


@sio.on("board chosen")
async def board_chosen(sid, data):
  game_name = players_games[sid]
  if masters[game_name] != sid: return

  category = data["cat"]
  element = data["el"]
  boards[game_name] = Zc.boards[category][element]
  cardsets[game_name] = CARDSET
  joinable[game_name] = True
  join_game(sid, game_name)

  await sio.emit("game created", {"game_name":game_name}, room=game_name)
  log(f'game \"{game_name}\" successfuly configured by {clients[sid]}')


async def leave_game(sid):
  if players_games[sid] == None: return
  game_name = players_games[sid]
  if not in_dict(joinable, game_name): return

  if in_dict(players, game_name):
    for i in range(0, len(players[game_name])):
      p_sid = players[game_name][i]
      if p_sid == sid: players[game_name][i] = None

  sio.leave_room(sid, game_name)
  log(f'game \"{game_name}\" left by {clients[sid]}')
  await sio.emit("player left", data=clients[sid], room=game_name) # TODO

  if masters[players_games[sid]] == sid:
    await abort_game(sid, players_games[sid])
  players_games[sid] = None


async def abort_game(sid, game_name):
  if not in_dict(masters, game_name): return
  log(f'game \"{game_name}\" ended by {clients[sid]}')
  
  await sio.emit("game ended", data=game_name, room=game_name) # TODO
  for client in players_games: 
    if players_games[client] == game_name and masters[game_name] != client:
      await leave_game(client)
  
  if in_dict(gamestates, game_name): del gamestates[game_name]
  if in_dict(cardsets, game_name): del cardsets[game_name]
  if in_dict(rules, game_name): del rules[game_name]
  if in_dict(boards, game_name): del boards[game_name]
  if in_dict(rules, game_name): del rules[game_name]
  if in_dict(masters, game_name): del masters[game_name]
  if in_dict(joinable, game_name): del joinable[game_name]
  games_names.remove(game_name)


@sio.on("join game")
async def join_game(sid, data):
  game_name = data
  if not in_dict(joinable, game_name):
    await sio.emit("failure", {
      "nature":"can't join game \""+game_name+"\"",
      "reason":"game doesn't exist"
      }, room=sid) # TODO
    return

  if not joinable[game_name]:
    await sio.emit("failure", {
      "nature":"can't join game \""+game_name+"\"",
      "reason":"game is not ready yet"
      }, room=sid) # TODO
    return

  joined = False
  for i in range(0, players[game_name]):
    if players[game_name][i] == None:
      players[game_name][i] = sid
      joined = True
  
  if joined == False:
    await sio.emit("failure", {
      "nature":"can't join game \""+game_name+"\"",
      "reason":"game is full"
      }, room=sid) # TODO
    return

  await leave_game(sid)

  players_games[sid] = game_name
  sio.enter_room(sid, game_name)
  await sio.emit("player joined", {"name":clients[sid]}, room=game_name) # TODO
  log(f'game \"{game_name}\" joined by {clients[sid]}')


@sio.event
async def disconnect(sid):
  await leave_game(sid)
  names.remove(clients[sid])
  log(f'{clients[sid]} just disconnected ')
  del clients[sid]
  del players_games[sid]

if __name__ == '__main__':
  web.run_app(app)