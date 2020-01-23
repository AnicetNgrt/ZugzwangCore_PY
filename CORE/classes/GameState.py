from typing import List
from .Player import Player
from .Board import Board

class Planned:
  ini_index: int
  pawn_index: int
  victim_index: int
  targets_index: List[int]
  play: callable

  def __init__(self, ini_index, pawn_index, play, victim_index = None, targets_index = []):
    self.ini_index = ini_index
    self.pawn_index = pawn_index
    self.victim_index = victim_index
    self.targets_index = targets_index
    self.play = play

class GameState:
  players: List[Player]
  board: Board
  planned: List[Planned]
  rules: dict
  turn: int
  step: int
  player_index: int

  def __init__(self, players:List[Player], board:Board, rules, turn:int, step:int, player_index:int):
    self.players = players
    self.board = Board
    self.rules = rules
    self.planned = []
    self.turn = turn
    self.step = int
    self.player_index = player_index
    
  def __str__(self):
    return "idk"