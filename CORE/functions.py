import CORE.classes as classes
from CORE.enums import Locations as locs
from typing import Tuple
from copy import deepcopy
from datetime import datetime
import pytz

def log(string):
  tz = pytz.timezone('Europe/Paris')
  paris_now = datetime.now(tz)
  s = str(paris_now.hour) + ":"
  s += str(paris_now.minute) + ":"
  s += str(paris_now.second) + "> "
  print(s+string)

def pawn_next_to_pawn(p1:classes.Pawn, p2:classes.Pawn) -> bool:
  is_next_to = False
  c1, r1 = p1.crd
  c2, r2 = p2.crd

  for i in range(1, 8, 2):
    trans_c, trans_r = locs.TRANSLATIONS[i]
    if c1 + trans_c == c2 and r1 + trans_r == r2:
      is_next_to = True
      break

  return is_next_to


def translate_pawn(state:classes.GameState, owner_index:int, pawn_index:int, trans:str) -> bool:
  player = state.players[owner_index]
  pawn = player.pawns[pawn_index]
  new_crd = deepcopy(pawn.crd)
  width = state.board.width
  height = state.board.height

  for char in trans:
    #print(char)
    new_c, new_r = new_crd
    if char == 'H': new_r = (new_r - 1) % height
    if char == 'B': new_r = (new_r + 1) % height
    if char == 'G': new_c = (new_c - 1) % width
    if char == 'D': new_c = (new_c + 1) % width
    case = state.board.mat[new_r][new_c]
    while not case.walkable:
      if char == 'H': new_r = (new_r - 1) % height
      if char == 'B': new_r = (new_r + 1) % height
      if char == 'G': new_c = (new_c - 1) % width
      if char == 'D': new_c = (new_c + 1) % width
      case = state.board.mat[new_r][new_c]
    new_crd = (new_c, new_r)

  #print(pawn.crd)
  #print(new_crd)

  return move_pawn_to(state, owner_index, pawn_index, new_crd)


def move_pawn_to(state:classes.GameState, owner_index:int, pawn_index:int, crd:Tuple[int, int]) -> bool:
  player = state.players[owner_index]
  pawn = player.pawns[pawn_index]
  c, r = crd
  if state.board.mat[r][c].has_pawn: return False
  if not state.board.mat[r][c].walkable: return False
  
  if pawn.crd != None:
    ic, ir = pawn.crd
    state.board.mat[ir][ic].has_pawn = False

  pawn.crd = crd
  state.board.mat[r][c].has_pawn = True
  state.board.mat[r][c].pawn_index = pawn.pawn_index
  state.board.mat[r][c].pawn_owner_index = pawn.owner_index
  return True


def kill_pawn(state:classes.GameState, owner_index:int, pawn_index:int) -> bool:
  player = state.players[owner_index]
  pawn = player.pawns[pawn_index]
  pawn.alive = False
  c, r = pawn.crd
  case = state.board.mat[r][c]
  case.has_pawn = False
  return True


def eject_pawn(state:classes.GameState, case_col:int, case_row:int) -> bool:
  case = state.board.mat[case_row][case_col]

  if not case.has_pawn: return False

  shift:int

  if case.location == locs.CENTER: return False
  else: shift = (case.location + 4) % 8
  
  found = False
  i = 0

  while not found and i < 8:  
    shift_c, shift_r = locs.TRANSLATIONS[(i + shift) % 8]
    c = case_col + shift_c
    r = case_row + shift_r
    found = move_pawn_to(state, case.pawn_owner_index, case.pawn_index, (c, r))
    i += 1
  
  return found

def universal_displacement_card_function(action:classes.Action,initial:classes.GameState,maker_index:int,pawn_index:int,victim_index:int,targets_index:int) -> Tuple[bool, classes.GameState]:

  final = deepcopy(initial)
  success = translate_pawn(final, maker_index, pawn_index, action.translation)
 
  return (success, final)