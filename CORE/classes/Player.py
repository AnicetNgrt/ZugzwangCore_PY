from typing import List
from .Pawn import Pawn
from .Card import Card
from CORE.enums import CardKinds

class Player:
  name: str
  pawns: List[Pawn]
  hand: List[Card]
  actions: int

  def __init__(self, name:str, pawns:List[Pawn], hand:List[Card], rules):
    self.name = name
    self.pawns = pawns
    self.hand = hand
    self.actions = rules["max actions"]

  def hand_effect_area(self):
    for card in self.hand:
      if card.core.kind != CardKinds.DISPLACEMENT: continue
      for action in card.core.actions:
        pass

  def __str__(self):
    string = self.name
    string += "\nCARDS:\n---------\n"
    for c in range(0, len(self.hand)):
      string += str(c)+" | "+str(self.hand[c])+"\n"
    
    return string