"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""

class BowlingGame:
    def __init__(self):
        """Initialise a new bowling game with empty rolls list and zero roll counter."""
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins):
        """Record the number of pins knocked down in a single roll.
        
        Args:
            pins (int): Number of pins knocked down (0-10).
        """
        self.rolls.append(pins)
        self.current_roll += 1

    def score(self):
        """Calculate and return the total score for the game.
        
        Returns:
            int: The total score across all 10 frames.
        """
        score = 0
        frame_index = 0

        for frame in range(9):  # Frames 1-9
            if self._is_strike(frame_index):
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                # BUG FIX 1: was only adding rolls[frame_index], missing second ball
                score += self.rolls[frame_index] + self.rolls[frame_index + 1]
                frame_index += 2

        # BUG FIX 2: 10th frame was missing entirely (range(9) skipped it)
        # BUG FIX 3: 10th frame has special rules - up to 3 balls, no bonus calculation
        score += self.rolls[frame_index]
        score += self.rolls[frame_index + 1]
        if self._is_strike(frame_index) or self._is_spare(frame_index):
            score += self.rolls[frame_index + 2]

        return score

    def _is_strike(self, frame_index):
        """Check if the roll at frame_index is a strike.
        
        Args:
            frame_index (int): Index into the rolls list.
            
        Returns:
            bool: True if the roll is a strike, False otherwise.
        """
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        """Check if the two rolls at frame_index form a spare.
        
        Args:
            frame_index (int): Index into the rolls list.
            
        Returns:
            bool: True if the two rolls make a spare, False otherwise.
        """
        return (frame_index + 1 < len(self.rolls) and
                self.rolls[frame_index] + self.rolls[frame_index + 1] == 10)

    def _strike_bonus(self, frame_index):
        """Calculate the bonus for a strike (next two balls).
        
        Args:
            frame_index (int): Index of the strike roll.
            
        Returns:
            int: Sum of the next two rolls.
        """
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
        """Calculate the bonus for a spare (next one ball).
        
        Args:
            frame_index (int): Index of the first roll of the spare.
            
        Returns:
            int: The next roll after the spare.
        """
        return self.rolls[frame_index + 2]