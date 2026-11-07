"""Testes do ZipFix: sanitização e reescrita/extração de nomes em ZIP."""

import os
import shutil
import tempfile
import unittest
import zipfile

from zipflix import fixer


class TestFixer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmpdir = self.tmp.name

    def _make_zip(self, path):
        entries = {
            "docs/relatorio-final.txt": b"conteudo final\n",
            "docs/relatorio com acento-ãã.txt": b"acentos\n",
            "emoji-🚀-teste.txt": b"emoji\n",
            "invalid|name*.txt": b"invalido\n",
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in entries.items():
                info = zipfile.ZipInfo(filename=name, date_time=(2026, 11, 7, 12, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, data)

    def test_sanitize_name(self):
        self.assertEqual(fixer.sanitize_name("docs/relatorio-ãã.txt"), "docs/relatorio-ãã.txt")
        self.assertEqual(fixer.sanitize_name("invalid|name*.txt"), "invalidname.txt")
        self.assertEqual(fixer.sanitize_name("bad:char*|name?.txt"), "badcharname.txt")

    def test_fix_zip_rewrites_names(self):
        src = os.path.join(self.tmpdir, "entrada.zip")
        dst = os.path.join(self.tmpdir, "saida.zip")
        self._make_zip(src)
        results = fixer.fix_zip(src, dst)
        self.assertTrue(len(results) > 0)
        with zipfile.ZipFile(dst, "r") as zf:
            names = zf.namelist()
        self.assertIn("docs/relatorio-final.txt", names)
        self.assertIn("docs/relatorio com acento-ãã.txt", names)
        self.assertIn("emoji-🚀-teste.txt", names)
        self.assertIn("invalidname.txt", names)
        self.assertNotIn("invalid|name*.txt", names)

    def test_extract_zip_sanitizes(self):
        src = os.path.join(self.tmpdir, "entrada2.zip")
        dest = os.path.join(self.tmpdir, "destino")
        self._make_zip(src)
        count = fixer.extract_zip(src, dest)
        self.assertEqual(count, 4)
        self.assertTrue(os.path.exists(os.path.join(dest, "emoji-🚀-teste.txt")))


if __name__ == "__main__":
    unittest.main()
