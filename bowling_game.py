"""
Bowling Game Implementation
A module for calculating bowling game scores according to standard
ten-pin bowling rules.
"""


class BowlingGame:
    """Represents a single game of ten-pin bowling.
    
    A game consists of 10 frames. In each frame the bowler has up to
    two chances to knock down 10 pins. The 10th frame allows up to
    three balls if a strike or spare is bowled.
    
    Attributes:
        rolls (list): A list of integers recording pins knocked down per roll.
        current_roll (int): Tracks how many rolls have been made.
    
    Example:
        >>> game = BowlingGame()
        >>> for _ in range(12):
        ...     game.roll(10)
        >>> game.score()
        300
    """

    MAX_FRAMES = 10
    MAX_PINS = 10

    def __init__(self):
        """Initialise a new bowling game with an empty rolls list."""
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
        """Calculate and return the total score for the completed game.

        Iterates through the first 9 frames applying strike and spare
        bonuses, then handles the 10th frame separately due to its
        special bonus ball rules.

        Returns:
            int: The total score across all 10 frames.
        """
        total = 0
        frame_index = 0

        for _ in range(self.MAX_FRAMES - 1):  # Frames 1-9
            if self._is_strike(frame_index):
                total += self.MAX_PINS + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                total += self.MAX_PINS + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                total += self._frame_score(frame_index)
                frame_index += 2

        # 10th frame
        total += self._tenth_frame_score(frame_index)

        return total

    def _is_strike(self, frame_index):
        """Return True if the roll at frame_index is a strike.

        Args:
            frame_index (int): Index into the rolls list.

        Returns:
            bool: True if strike, False otherwise.
        """
        return (frame_index < len(self.rolls) and
                self.rolls[frame_index] == self.MAX_PINS)

    def _is_spare(self, frame_index):
        """Return True if the two rolls at frame_index form a spare.

        Args:
            frame_index (int): Index of the first roll of the frame.

        Returns:
            bool: True if spare, False otherwise.
        """
        return (frame_index + 1 < len(self.rolls) and
                self.rolls[frame_index] + self.rolls[frame_index + 1] == self.MAX_PINS)

    def _frame_score(self, frame_index):
        """Return the sum of the two rolls in an open frame.

        Args:
            frame_index (int): Index of the first roll of the frame.

        Returns:
            int: Total pins for the two rolls.
        """
        return self.rolls[frame_index] + self.rolls[frame_index + 1]

    def _strike_bonus(self, frame_index):
        """Return the bonus for a strike (sum of next two rolls).

        Args:
            frame_index (int): Index of the strike roll.

        Returns:
            int: Sum of the next two rolls.
        """
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
        """Return the bonus for a spare (the next single roll).

        Args:
            frame_index (int): Index of the first roll of the spare.

        Returns:
            int: The roll immediately after the spare.
        """
        return self.rolls[frame_index + 2]

    def _tenth_frame_score(self, frame_index):
        """Calculate and return the score for the 10th frame.

        The 10th frame awards a third ball if the bowler scores a
        strike or spare, allowing a maximum of 30 points in the frame.

        Args:
            frame_index (int): Index of the first roll of the 10th frame.

        Returns:
            int: Total score for the 10th frame including any bonus ball.
        """
        frame_total = self.rolls[frame_index] + self.rolls[frame_index + 1]
        if self._is_strike(frame_index) or self._is_spare(frame_index):
            frame_total += self.rolls[frame_index + 2]
        return frame_total