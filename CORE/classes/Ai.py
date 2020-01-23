from typing import List
from copy import deepcopy
import itertools
from .GameState import GameState
from .Move import Move
from .Player import Player

# AI stuff I'll figure out later

class Branch:
  player_index: int
  generation: int
  state: GameState
  p_count: int
  pp_count: int
  move: Move
  nexts: set
  branch_building_function: callable
  sealed: bool

  def __init__(self, state, player_index, generation, move = None):
    self.generation = generation
    self.p_count = 0
    self.pp_count = 0
    self.player_index = player_index
    self.state = deepcopy(state)
    self.move = move
    self.nexts = set()
    self.sealed = False
  
  def __str__(self):
    string = ""
    for i in range(0, self.generation): string += ".."
    string += "| " + str(self.move) + " ||"
    string += "%3d|" % self.generation
    string += "%3d|" % self.pp_count
    string += "%3d|" % self.p_count
    string += "%3d|" % self.sealed
    string += "\n"
    if len(self.nexts) > 0: string += "\n"
    for subbranch in self.nexts:
      string += str(subbranch)
    if len(self.nexts) > 0: string += "\n"

    return string
  

  def add_subbranch(self, card_i, action_i, pawn_i, p2 = None, tg = []):
    move = Move(self.state, self.player_index, card_i, action_i, pawn_i, p2, tg)
    move.predict()
    if move.plausible:
      b = Branch(move.final, self.player_index, self.generation+1, move)
      self.nexts.add(b)
      b_sealed = deepcopy(b)
      b_sealed.sealed = True
      self.nexts.add(b_sealed)
      return (1, 1)
    else: return (1, 0)


class Tree:
  branch_building_function: callable
  p_count: int
  pp_count: int
  player_index: int
  trunc: Branch
  initial: GameState

  def __init__(self, initial, branch_building_function, player_index):
    self.p_count = 0
    self.pp_count = 0
    self.player_index = player_index
    self.branch_building_function = branch_building_function
    self.initial = deepcopy(initial)
    self.trunc = Branch(self.initial, self.player_index, 0)
  
  def compute(self, max_gen):
    gen_count = 1
    self.branch_building_function(self.trunc)
    self.p_count += self.trunc.p_count
    self.pp_count += self.trunc.pp_count

    crt_gen = self.trunc.nexts

    while len(crt_gen) > 0 and gen_count < max_gen:
      gen_count += 1

      new_gen = set()
      for branch in crt_gen:
        self.branch_building_function(branch)
        self.p_count += branch.p_count
        self.pp_count += branch.pp_count

        for subbranch in branch.nexts:
          new_gen.add(subbranch)

      crt_gen = new_gen
    
    print(self.p_count)
    print(self.pp_count)
    print("\n")

    to_remove = set()
    for branch in crt_gen:
      if not branch.sealed:
        to_remove.add(branch)
    
    for branch in to_remove:
      crt_gen.remove(branch)

    print(self.trunc)


    


def build_branches_no_sorting(branch:Branch):
  if branch.sealed: return
  p1 = branch.player_index
  initial = branch.state;

  for p2 in range(0, len(initial.players)):
    if p2 == p1: continue
    player = initial.players[p1]
    oppon = initial.players[p2]
    for card_i in range(0, len(player.hand)):
      card = player.hand[card_i]
      for action_i in range(0, len(card.core.actions)):
        if card.core.pawn_matters:
          for pawn_i in range(0, len(player.pawns)):
            targets_count = card.core.targets_count
            if targets_count > 0:
              target_groups = list(itertools.combinations(tuple(range(len(oppon.pawns))), targets_count))
              for tg in target_groups:
                p, pp = branch.add_subbranch(card_i, action_i, pawn_i, p2, tg)
                branch.p_count += p
                branch.pp_count += pp
            else:
              p, pp = branch.add_subbranch(card_i, action_i, pawn_i)
              branch.p_count += p
              branch.pp_count += pp
        else:
          p, pp = branch.add_subbranch(card_i, action_i, pawn_i)
          branch.p_count += p
          branch.pp_count += pp



class TurnSimulation:
  initial: GameState
  moves: List[Move]
  final: GameState
  score: int

  def __init__(self, initial:GameState, first_move:Move):
    self.initial = initial
    self.moves = []
    self.moves[0] = first_move
    self.score = 0


class Ai:
  player: Player
  possibilities: List[TurnSimulation]
  eval_alg: callable

  def __init__(self, player:Player, eval_alg:callable):
    self.player = player
    self.possibilities = []
    self.eval_alg = eval_alg
