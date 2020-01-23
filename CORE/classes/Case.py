from typing import List

class Case:
  whitelist: List[str]
  location: int
  walkable: bool
  is_border: bool
  is_corner: bool
  has_pawn: bool
  pawn_owner_index: int
  pawn_index: int

  def __init__(self, whitelist:List[str], walkable:bool, location:int):
    self.whitelist = whitelist
    self.is_border = False
    self.is_corner = False
    self.walkable = walkable
    self.location = location
    self.has_pawn = False
    self.pawn_owner_index = None
    self.pawn_index = None