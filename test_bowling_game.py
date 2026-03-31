"""
Unit Tests for BowlingGame
Test suite for verifying the correctness of the BowlingGame class.
"""

import unittest
from bowling_game import BowlingGame


class TestBowlingGame(unittest.TestCase):

    def setUp(self):
        """Create a fresh BowlingGame instance before each test."""
        self.game = BowlingGame()

    def roll_many(self, pins, times):
        """Helper method to roll the same number of pins multiple times."""
        for _ in range(times):
            self.game.roll(pins)

    def roll_spare(self):
        """Helper method to roll a spare (5 + 5)."""
        self.game.roll(5)
        self.game.roll(5)

    def roll_strike(self):
        """Helper method to roll a strike (10)."""
        self.game.roll(10)

    # ── TC-01: Gutter Game ─────────────────────────────────────────────
    def test_gutter_game(self):
        """TC-01: All gutter balls should score 0."""
        self.roll_many(0, 20)
        self.assertEqual(self.game.score(), 0)

    # ── TC-02: All Ones ────────────────────────────────────────────────
    def test_all_ones(self):
        """TC-02: Rolling 1 pin every ball for 20 rolls should score 20."""
        self.roll_many(1, 20)
        self.assertEqual(self.game.score(), 20)

    # ── TC-03: Single Spare ────────────────────────────────────────────
    def test_single_spare(self):
        """TC-03: A spare scores 10 plus the next ball as bonus."""
        self.roll_spare()        # Frame 1: 5+5 spare
        self.game.roll(3)        # Bonus ball = 3
        self.roll_many(0, 17)    # Rest of game
        self.assertEqual(self.game.score(), 16)

    # ── TC-04: Single Strike ───────────────────────────────────────────
    def test_single_strike(self):
        """TC-04: A strike scores 10 plus the next two balls as bonus."""
        self.roll_strike()       # Frame 1: strike
        self.game.roll(3)        # Frame 2 ball 1
        self.game.roll(4)        # Frame 2 ball 2
        self.roll_many(0, 16)    # Rest of game
        self.assertEqual(self.game.score(), 24)

    # ── TC-05: Perfect Game ────────────────────────────────────────────
    def test_perfect_game(self):
        """TC-05: 12 consecutive strikes should score 300."""
        self.roll_many(10, 12)
        self.assertEqual(self.game.score(), 300)

    # ── TC-06: All Spares ──────────────────────────────────────────────
    def test_all_spares(self):
        """TC-06: All spares (5+5) with final bonus ball of 5 should score 150."""
        self.roll_many(5, 21)
        self.assertEqual(self.game.score(), 150)

    # ── TC-07: Consecutive Strikes ─────────────────────────────────────
    def test_consecutive_strikes(self):
        """TC-07: Two consecutive strikes followed by 4,2 then gutter balls."""
        self.roll_strike()       # Frame 1: strike
        self.roll_strike()       # Frame 2: strike
        self.game.roll(4)        # Frame 3 ball 1
        self.game.roll(2)        # Frame 3 ball 2
        self.roll_many(0, 16)    # Rest of game
        # Frame 1: 10+10+4 = 24
        # Frame 2: 10+4+2  = 16
        # Frame 3: 4+2     = 6
        # Total = 46
        self.assertEqual(self.game.score(), 46)

    # ── TC-08: 10th Frame Strike ───────────────────────────────────────
    def test_tenth_frame_strike(self):
        """TC-08: Strike in 10th frame awards 2 bonus balls."""
        self.roll_many(0, 18)    # Frames 1-9: all gutter
        self.game.roll(10)       # 10th frame: strike
        self.game.roll(10)       # Bonus ball 1
        self.game.roll(10)       # Bonus ball 2
        self.assertEqual(self.game.score(), 30)

    # ── TC-09: 10th Frame Spare ────────────────────────────────────────
    def test_tenth_frame_spare(self):
        """TC-09: Spare in 10th frame awards 1 bonus ball."""
        self.roll_many(0, 18)    # Frames 1-9: all gutter
        self.game.roll(5)        # 10th frame ball 1
        self.game.roll(5)        # 10th frame ball 2 (spare)
        self.game.roll(3)        # Bonus ball
        self.assertEqual(self.game.score(), 13)

    # ── TC-10: Regular Game ────────────────────────────────────────────
    def test_regular_game(self):
        """TC-10: Regular game with no strikes or spares should score 72."""
        rolls = [3, 4, 2, 5, 1, 6, 4, 2, 8, 1,
                 7, 1, 5, 3, 2, 3, 4, 3, 2, 6]
        for pins in rolls:
            self.game.roll(pins)
        self.assertEqual(self.game.score(), 72)

    # ── TC-11: Mixed Game ──────────────────────────────────────────────
    def test_mixed_game(self):
        """TC-11: Mixed game with strikes, spares and open frames should score 190."""
        rolls = [10, 3, 6, 5, 5, 8, 1, 10,
                 10, 10, 9, 0, 7, 3, 10, 10, 8]
        for pins in rolls:
            self.game.roll(pins)
        self.assertEqual(self.game.score(), 190)

    # ── TC-12: Open Frame Only ─────────────────────────────────────────
    def test_open_frame_scores_both_balls(self):
        """TC-12: Open frame must add BOTH balls, not just the first."""
        self.game.roll(3)
        self.game.roll(4)
        self.roll_many(0, 18)
        self.assertEqual(self.game.score(), 7)

    # ── TC-13: roll() counter ─────────────────────────────────────────
    def test_roll_appends_and_increments(self):
        """TC-13: roll() should append pins to rolls list and increment counter."""
        self.game.roll(5)
        self.assertEqual(self.game.rolls, [5])
        self.assertEqual(self.game.current_roll, 1)

    # ── TC-14: Frame Count Boundary ───────────────────────────────────
    def test_only_ten_frames_counted(self):
        """TC-14: Extra rolls beyond 10 frames should not affect the score."""
        self.roll_many(1, 25)    # More rolls than a normal game
        self.assertEqual(self.game.score(), 20)

    # ── TC-15: Spare then 10th Frame Strike ───────────────────────────
    def test_spare_frame9_then_tenth_frame(self):
        """TC-15: Spare in frame 9, strike as bonus in frame 10."""
        self.roll_many(0, 16)    # Frames 1-8: gutter
        self.game.roll(5)        # Frame 9 ball 1
        self.game.roll(5)        # Frame 9 ball 2 (spare)
        self.game.roll(10)       # Frame 10 ball 1 (bonus for spare = 10)
        self.game.roll(2)        # Frame 10 ball 2
        self.game.roll(0)        # Frame 10 ball 3
        # Frame 9: 10 + 10 = 20
        # Frame 10: 10 + 2 + 0 = 12
        self.assertEqual(self.game.score(), 32)


if __name__ == '__main__':
    unittest.main()