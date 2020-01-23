from typing import List
from copy import deepcopy
from .GameState import GameState

class Move:
  initial: GameState
  maker_index: int
  card_index: int
  action_index: int
  pawn_index: int
  victim_index: int
  targets_index: List[int]
  plausible: bool
  final: GameState
  
  def __init__(self, initial:GameState, maker_index:int, card_index:int, action_index:int, pawn_index:int, victim_index:int = None, targets_index:List[int] = []):
    self.initial = deepcopy(initial)
    self.final = deepcopy(initial)
    self.maker_index = maker_index
    self.card_index = card_index
    self.action_index = action_index
    self.pawn_index = pawn_index
    self.victim_index = victim_index
    self.targets_index = targets_index
    self.plausible = False

    if not 0 <= maker_index < len(self.initial.players): return
    maker = self.initial.players[maker_index]
    if not 0 <= card_index < len(maker.hand): return   
    card = maker.hand[card_index]
    if not 0 <= action_index < len(card.core.actions): return
    action = card.core.actions[action_index]
    if not maker.actions >= action.cost: return
    if card.turn_play_count >= card.core.max_turn: return
    if card.total_play_count >= card.core.max_global: return  
    if not 0 <= pawn_index < len(maker.pawns): return
    if not (victim_index == None):
      if not 0 <= victim_index < len(initial.players): return    
      victim = self.initial.players[victim_index]
      for i in targets_index:
        if not 0 <= i < len(victim.pawns): return 
    self.plausible = True
  

  def __str__(self):
    string = ""
    if 0 <= self.maker_index < len(self.final.players): string += "Ap: " + str(self.final.players[self.maker_index].actions) + " | "

    string += "Mi: " + str(self.maker_index) + " | "
    string += "Ci: " + str(self.card_index) + " | "
    string += "Ai: " + str(self.action_index) + " | "
    string += "Pi: " + str(self.pawn_index) + " | "
    string += "OK: " + str(self.plausible)
    return string


  def predict(self):
    if not self.plausible: return
    
    maker = self.initial.players[self.maker_index]
    card = maker.hand[self.card_index]
    action = card.core.actions[self.action_index]

    self.plausible, self.final = action(self.initial, self.maker_index, self.pawn_index, self.victim_index, self.targets_index)

    new_maker = self.final.players[self.maker_index]
    new_card = new_maker.hand[self.card_index]

    new_maker.actions -= action.cost

    if new_maker.actions == 0:
      new_maker.actions = self.final.rules["max actions"]
      for i in range(0, len(new_maker.hand)):
        new_maker.hand[i].turn_play_count = 0
      
    else:
      new_card.turn_play_count += 1
    
    new_card.total_play_count += 1