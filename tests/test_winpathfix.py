"""Testes do WinPathFix: coleta de renomes em diretorio."""

import os
import tempfile
import unittest

from winpathfix import fixer
from winpathfix import cli


class TestWinPathFix(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmpdir = self.tmp.name

    def test_collect_renames_empty_for_clean_dir(self):
        open(os.path.join(self.tmpdir, "ok_renome.txt"), "w").write("x")
        self.assertEqual(fixer.collect_renames(self.tmpdir), [])

    def test_collect_renames_blocks_traversal(self):
        self.assertEqual(fixer.sanitize_name("../../evil.txt"), "evil.txt")


if __name__ == "__main__":
    unittest.main()
