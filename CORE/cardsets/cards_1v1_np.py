import CORE.classes as classes
from CORE.enums import CardKinds as kinds
from CORE.functions import pawn_next_to_pawn, eject_pawn, kill_pawn, universal_displacement_card_function
from typing import Tuple, Dict
from copy import deepcopy
  

CARDS:Dict[str, classes.CardData] = {}

# -------------------------------- CONTACT
c = classes.CardData()

c.name = "Contact"
c.desc = ""
c.pawn_matters = True
c.kind = kinds.ATTACK
c.targets_count = 1
c.hand_cost = 0
c.max_turn = 999
c.max_global = 999

def play(action:classes.Action,initial:classes.GameState,maker_index:int,pawn_index:int,victim_index:int,targets_index:int) -> Tuple[bool, classes.GameState]:

  final = deepcopy(initial)

  if victim_index is None or len(targets_index) == 0: return (False, final)

  p1 = final.players[maker_index].pawns[pawn_index]
  p2 = final.players[victim_index].pawns[targets_index[0]]

  success = pawn_next_to_pawn(p1, p2)
  if not success: return (False, final)

  success = kill_pawn(final, victim_index, targets_index[0])
  return (success, final)
  
c.actions = [classes.Action(play, 1)]
CARDS["Contact"] = deepcopy(c)

# -------------------------------- SUBLIME
c = classes.CardData()

c.name = "Sublime"
c.desc = ""
c.pawn_matters = False
c.targets_count = 0
c.kind = kinds.MODIFIER
c.hand_cost = 1
c.max_turn = 1
c.max_global = 1

def play(action:classes.Action,initial:classes.GameState,maker_index:int,pawn_index:int,victim_index:int,targets_index:int) -> Tuple[bool, classes.GameState]:

  final = deepcopy(initial)

  for l in range(0, len(final.board.mat)):
    for c in range(0, len(final.board.mat[l])):
      if final.board.mat[l][c].is_corner:
        final.board.mat[l][c].whitelist = []
        eject_pawn(final, c, l)

      if final.board.mat[l][c].is_border:
        final.board.mat[l][c].whitelist = [final.players[maker_index].name]
  
  return (True, final)

c.actions = [classes.Action(play, 1)]
CARDS["Sublime"] = deepcopy(c)

# -------------------------------- MOVETEST
c = classes.CardData()

c.name = "Movetest"
c.desc = ""
c.pawn_matters = True
c.kind = kinds.DISPLACEMENT
c.targets_count = 0
c.hand_cost = 0
c.max_turn = 999
c.max_global = 999
c.actions = []
translations = ["HHG","HHD","DDH","DDB","BBD","BBG","GGB","GGH"]

for t in translations:
  action = classes.Action(universal_displacement_card_function, 1)
  action.translation = deepcopy(t)
  c.actions.append(action)

CARDS['Movetest'] = deepcopy(c)

# -------------------------------- MOVETEST(1)
c = classes.CardData()

c.name = "Movetest(1)"
c.desc = ""
c.pawn_matters = True
c.kind = kinds.DISPLACEMENT
c.targets_count = 0
c.hand_cost = 0
c.max_turn = 999
c.max_global = 999
c.actions = []
translations = ["HHG","HHD"]

for t in translations:
  action = classes.Action(universal_displacement_card_function, 1)
  action.translation = deepcopy(t)
  c.actions.append(action)

CARDS['Movetest(1)'] = deepcopy(c)