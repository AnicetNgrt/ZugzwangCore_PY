from typing import Tuple

class Action:
  play: callable
  cost: int

  def __init__(self, play:callable, cost:int):
    self.play = play
    self.cost = cost

  def __call__(
    self,
    initial:object,
    maker_index:int,
    pawn_index:int,
    victim_index:int,
    targets_index:int,
    more:dict
  ) -> Tuple[bool, object]:
    
    return self.play(self, initial, maker_index, pawn_index, victim_index, targets_index, more)