from CORE.classes import Board
import os

def init_board_from_file(path:str, players=[]):
  walkables = []
  locations = []

  f = open(path, "r")
  fl = f.readlines()
  i = 0
  l = 0
  line = fl[0]

  while line != "STOP\n" and i < len(fl)-1:
    locations.append([])
    for c in line:
      if c in {'0','1','2','3','4','5','6','7','8'}:
        locations[l].append(ord(c)-48)
      else:
        locations[l].append(8)
    l += 1
    i += 1
    line = fl[i]
  
  l = 0
  i += 1
  line = fl[i]

  while line != "STOP\n" and i < len(fl)-1:  
    walkables.append([])
    for c in line:
      if c == '.':
        walkables[l].append(True)
      else:
        walkables[l].append(False)
    l += 1
    i += 1
    line = fl[i]

  return Board(walkables, locations, players)

t15x10 = os.path.join(os.path.dirname(__file__), "board_test.txt")

boards = {
  "tournament": {
    "15x10": init_board_from_file(t15x10)
  }
}