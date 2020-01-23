class CardKinds:
  MODIFIER = 0
  TRAP = 1
  DISPLACEMENT = 2
  ATTACK = 3

class Locations:
  TOPLEFT = 0
  TOP = 1
  TOPRIGHT = 2
  RIGHT = 3
  BOTTRIGHT = 4
  BOTT = 5
  BOTTLEFT = 6
  LEFT = 7
  CENTER = 8
  
  TRANSLATIONS = [
    (-1, -1), (0, -1), (1, -1), (1, 0),
    (1, 1), (0, 1), (-1, 1), (-1, 0)
  ]

