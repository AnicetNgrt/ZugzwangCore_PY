from typing import List, Tuple
from .Case import Case
from .Player import Player
from CORE.enums import Locations as locs

class Board:
  mat: List[List[Case]]
  width: int
  height: int

  def __init__(self, walkables:List[List[bool]], locations:List[List[int]], players:List[Player]):
    self.mat = []
    
    height = len(walkables)
    if height == 0 or len(locations) != height: return
    width = len(walkables[0])
    if width == 0 or len(locations[0]) != width: return

    self.height = height
    self.width = width

    whitelist = [p.name for p in players]

    for l in range(0, height):
      self.mat.append([])
      for c in range(0, width):
        case = Case(whitelist, walkables[l][c], locations[l][c])
        self.mat[l].append(case)


    pawns = []
    for player in players:
      for pawn in player.pawns:
        pawns.append(pawn)
    
    for pawn in pawns:
      c, l = pawn.crd
      if c > width: c %= width
      if l > height: l %= height

      tries = 0
      while self.mat[l][c].has_pawn:
        if tries == width*height: break
        tries += 1
        c += 1
        if c == width:
          l += 1
          l %= height
        c %= width
      if tries == width*height: break

      self.mat[l][c].has_pawn = True
      self.mat[l][c].pawn_owner_index = pawn.owner_index
      self.mat[l][c].pawn_index = pawn.pawn_index
    
    self.compute_borders_corners()


  def case_next_to_case(self, crd1:Tuple[int, int], crd2:Tuple[int, int]) -> bool:
    is_next_to = False
    c1, r1 = crd1
    c2, r2 = crd2

    for i in range(1, 8, 2):
      trans_c, trans_r = locs.TRANSLATIONS[i]
      if c1 + trans_c == c2 and r1 + trans_r == r2:
        is_next_to = True
        break

    return is_next_to


  def compute_borders_corners(self):
    for l in range(0, self.height):
      for c in range(0, self.width):
        if self.mat[l][c].walkable:
          neighboor_count = 0
          for i in range(1, 8, 2):
            trans_c, trans_r = locs.TRANSLATIONS[i]
            try:
              w = self.mat[l+trans_r][c+trans_c].walkable
              if w: neighboor_count += 1
            except IndexError:
              pass
          
          if 0 < neighboor_count <= 2: self.mat[l][c].is_corner = True
          if neighboor_count == 3: self.mat[l][c].is_border = True


  def __str__(self, color=True) -> str:
    string = ""
    l = 0
    if color:
      for line in self.mat:
        l += 1
        c = 0
        for case in line:
          c += 1
          if case.has_pawn:
            char = str(case.pawn_owner_index)+str(case.pawn_index)
            string += '\033[42m\033[30m'+char+'\033[0m'
          elif case.is_border:
            if (c+l)%2 == 0: string += '\033[45m  \033[0m'
            else: string += '\033[41m  \033[0m'
          elif case.is_corner:
            string += '\033[40m  \033[0m'
          elif case.walkable:
            if (c+l)%2 == 0: string += '\033[47m  \033[0m'
            else: string += '\033[43m  \033[0m'
          else: string += '..'
        string += '\n'
    else:
      for line in self.mat:
        l += 1
        c = 0
        for case in line:
          c += 1
          if case.has_pawn:
            char = str(case.pawn_owner_index)+str(case.pawn_index)
            string += char
          elif case.walkable:
            if (c+l)%2 == 0: string += '▓▓'
            else: string += '██'
          else: string += '░░'
        string += '\n'

    return string  