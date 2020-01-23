from typing import Tuple

class Pawn:
  alive: bool
  exiled: bool
  crd: Tuple[int, int]
  char: chr
  owner_index: int
  pawn_index: int

  def __init__(self, crd: Tuple[int, int], index:int, owner_index:int, char: chr):
    self.alive = True
    self.exiled = False
    self.crd = crd
    self.chr = char
    self.pawn_index = index
    self.owner_index = owner_index