"""Tests for token caps and conversation path safety."""
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_security import (
    DEFAULT_MAX_TOKENS,
    MAX_TOKENS_CAP,
    clamp_max_tokens,
    conversation_file_path,
)


class TestApiSecurity(unittest.TestCase):
    def test_clamp_default_and_cap(self):
        self.assertEqual(clamp_max_tokens(None), DEFAULT_MAX_TOKENS)
        self.assertEqual(clamp_max_tokens('nope'), DEFAULT_MAX_TOKENS)
        self.assertEqual(clamp_max_tokens(0), DEFAULT_MAX_TOKENS)
        self.assertEqual(clamp_max_tokens(1000), 1000)
        self.assertEqual(clamp_max_tokens(150000), MAX_TOKENS_CAP)

    def test_conversation_id_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(conversation_file_path(tmp, '../secret'))
            self.assertIsNone(conversation_file_path(tmp, 'conv_1/../../etc/passwd'))
            self.assertIsNone(conversation_file_path(tmp, 'notes'))

    def test_conversation_id_accepts_generated_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = conversation_file_path(tmp, 'conv_1710000000')
            self.assertEqual(os.path.basename(path), 'conv_1710000000.json')
            self.assertEqual(os.path.dirname(path), os.path.realpath(tmp))


if __name__ == '__main__':
    unittest.main()
