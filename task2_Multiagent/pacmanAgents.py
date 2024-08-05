# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
import random
import game
import util

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()
import random
from pacman import Directions
from game import Agent
from game import Actions

class MonteCarloPacmanAgent(Agent):
   def __init__(self, optimal_distance=5):
       super().__init__()
       self.optimal_distance = optimal_distance

   def getAction(self, gameState):
       legal_actions = gameState.getLegalActions()
       legal_actions.remove(Directions.STOP)  # Виключаємо зупинку
       safe_actions = []

       for action in legal_actions:
           next_pos = self.getNextPosition(gameState, action)
           if self.is_safe(next_pos, gameState):
               safe_actions.append(action)

       if safe_actions:
           return random.choice(safe_actions)
       else:
           return random.choice(legal_actions)

   def getNextPosition(self, gameState, action):
       x, y = gameState.getPacmanPosition()
       dx, dy = Actions.directionToVector(action)
       return int(x + dx), int(y + dy)

   def is_safe(self, position, gameState):
       ghost_positions = gameState.getGhostPositions()
       for ghost_pos in ghost_positions:
           if self.distance(position, ghost_pos) < self.optimal_distance:
               return False
       return True

   def distance(self, pos1, pos2):
       return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

