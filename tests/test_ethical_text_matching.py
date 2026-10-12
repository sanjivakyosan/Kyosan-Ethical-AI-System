"""Tests for word-boundary keyword matching."""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ethical_text_matching import contains_word, contains_any_word


class TestEthicalTextMatching(unittest.TestCase):
    def test_kill_not_in_skill(self):
        self.assertFalse(contains_word('I improved my skill today', 'kill'))

    def test_kill_as_word(self):
        self.assertTrue(contains_word('How to kill weeds in the garden', 'kill'))

    def test_war_not_in_award(self):
        self.assertFalse(contains_word('She won an award', 'war'))

    def test_crisis_any_word(self):
        terms = ['crisis', 'refugee', 'attack']
        self.assertTrue(contains_any_word('attack in refugee crisis', terms))
        self.assertFalse(contains_any_word('skill building workshop', terms))


if __name__ == '__main__':
    unittest.main()
