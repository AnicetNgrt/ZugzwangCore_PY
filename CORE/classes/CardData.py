from typing import List
from .Action import Action

class CardData:
  name: str
  desc: str
  kind: int
  pawn_matters: bool
  targets_count: int
  siblings: [str]
  max_global: int
  max_turn: int
  hand_cost: int
  actions: List[Action]
  memory: object

  def __init__(self):
    self.memory = lambda:None
