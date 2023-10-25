#
# AI Player for use in Connect Four  
#

import random
from Connect4 import *

class AIPlayer(Player):
    """ subclass of Player class that represents an intelligent computer player;
        Inherits from Player """
    
    def __init__(self, checker, tiebreak, lookahead):
        """ contructs a AI player Object with checker, num_moves,
            tiebreak, and lookahead attributes 
        """
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
         
    def __repr__(self):
        """ Overrides Player __repr__ method;
            returns a string representing an AIPlayer Ojbect """
        return super().__repr__() + " ("  + self.tiebreak + ", " + str(self.lookahead) + ")"
       
    def max_score_column(self, scores):
        """ takes a list scores and returns the index of the column with a max score """   
        max_score = max(scores)
        max_score_indices = []
        for i in range(len(scores)):
            if scores[i] == max_score:
                max_score_indices += [i]
        if self.tiebreak == "LEFT":
            return max_score_indices[0]
        elif self.tiebreak == "RIGHT":
            return max_score_indices[-1]
        return random.choice(max_score_indices)
    
    def scores_for(self, b):
        """ returns a list of scores that represents the 
            scores for each column in board b """
        scores = [' '] * b.width
        for col in range(b.width):
            if not b.can_add_to(col):
                scores[col] = -1
            elif b.is_win_for(self.checker):
                scores[col] = 100
            elif b.is_win_for(self.opponent_checker()):
                scores[col] = 0
            elif self.lookahead == 0:
                scores[col] = 50
            else:
                b.add_checker(self.checker, col)
                opponent = AIPlayer(self.opponent_checker(), self.tiebreak, self.lookahead - 1)
                opp_scores = opponent.scores_for(b)
                if max(opp_scores) == 0:
                    scores[col] = 100
                elif max(opp_scores) == 100:
                    scores[col] = 0
                else: scores[col] = 50
                b.remove_checker(col)
        return scores
    
    def next_move(self, b):
        """ overrides Player next_move method; returns 
            self AIPlayer's judgement of best possible move""" 
        self.num_moves += 1
        return self.max_score_column(self.scores_for(b))  
                


