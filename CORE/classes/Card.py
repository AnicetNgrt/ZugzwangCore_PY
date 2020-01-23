from .CardData import CardData

class Card:
  core: CardData
  turn_play_count: int
  total_play_count: int

  def __init__(self, core:CardData):
    self.core = core
    self.total_play_count = 0
    self.turn_play_count = 0

  def __str__(self):
    string = ""
    string += self.core.name + " | "
    string += "turn: " + str(self.turn_play_count) + "/" + str(self.core.max_turn) + " | "
    string += "game: " + str(self.total_play_count) + "/" + str(self.core.max_global) + " | "
    return string