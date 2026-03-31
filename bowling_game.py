"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""

class BowlingGame:
    def __init__(self):
        # Initialize a new game with 10 frames
        # Each frame has up to 2 rolls (except the 10th frame which can have 3)
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins):
        
        self.rolls.append(pins)
        self.current_roll += 1

    def score(self):
        
        score = 0
        frame_index = 0

        for frame in range(9):
            if self._is_strike(frame_index):
                # Strike
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                # Spare
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                # Open frame
                score += self.rolls[frame_index]
                frame_index += 2

        return score

    def _is_strike(self, frame_index):
        
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        
        return frame_index + 1 < len(self.rolls) and self.rolls[frame_index] + self.rolls[frame_index + 1] == 10

    def _strike_bonus(self, frame_index):
       
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
       
        return self.rolls[frame_index + 2]