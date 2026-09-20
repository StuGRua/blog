#!/usr/bin/env python3
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Isolation(unittest.TestCase):
    def test_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            content = base / 'content'
            content.mkdir()
            (content / 'index.md').write_text('# Public\n')
            def check(ok):
                p = subprocess.run(['node', str(ROOT / 'scripts/check-content.mjs'), str(content)], capture_output=True)
                self.assertEqual(p.returncode == 0, ok, p.stderr.decode())
            check(True)
            private = base / 'private.md'
            private.write_text('PRIVATE')
            link = content / 'leak.md'
            link.symlink_to(private)
            check(False)
            link.unlink()
            (content / 'index.md').write_text('[[private]]')
            check(False)
            (content / 'index.md').write_text('[missing][id]\n\n[id]: missing.md')
            check(False)
            (content / 'index.md').write_text('# Public')
            (content / 'leak.pdf').write_bytes(b'private')
            check(False)
            (content / 'leak.pdf').unlink()
            check(True)

    def test_explicit_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            (base / 'scripts').mkdir()
            shutil.copy2(ROOT / 'scripts/copy-content.py', base / 'scripts/copy-content.py')
            src = base / 'private'
            src.mkdir()
            (src / 'article.md').write_text('---\npublish: false\n---\nPUBLIC')
            (src / 'secret.md').write_text('---\npublish: true\n---\nSECRET')
            command = ['python3', str(base / 'scripts/copy-content.py'), '--source', str(src), 'article.md']
            subprocess.run(command, check=True, capture_output=True)
            self.assertFalse((base / 'content').exists())
            subprocess.run(command + ['--apply'], check=True, capture_output=True)
            self.assertEqual([p.name for p in (base / 'content').iterdir()], ['article.md'])
            (src / 'article.md').write_text('CHANGED')
            self.assertIn('PUBLIC', (base / 'content/article.md').read_text())

    def test_static_and_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            for name in ['scripts', 'quartz/static', 'public']:
                (base / name).mkdir(parents=True)
            shutil.copy2(ROOT / 'scripts/check-release.py', base / 'scripts/check-release.py')
            (base / 'scripts/static-manifest.json').write_text('{}')
            for name in ['index.html', 'robots.txt', 'sitemap.xml']:
                (base / 'public' / name).write_text('public')
            command = ['python3', str(base / 'scripts/check-release.py'), str(base / 'public')]
            def check(ok):
                result = subprocess.run(command, capture_output=True)
                self.assertEqual(result.returncode == 0, ok, result.stderr.decode())
            check(True)
            (base / 'secret.txt').write_text('fixture')
            link = base / 'quartz/static/leak.txt'
            link.symlink_to(base / 'secret.txt')
            check(False)
            link.unlink()
            (base / 'quartz/static/unapproved.png').write_bytes(b'fixture')
            check(False)
            (base / 'quartz/static/unapproved.png').unlink()
            (base / 'public/leak.pdf').write_bytes(b'fixture')
            check(False)
            (base / 'public/leak.pdf').unlink()
            (base / 'public/index.html').write_text('https://internal.bilibili.co')
            check(False)

    def test_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            for name in ['scripts', 'content', 'public']:
                (base / name).mkdir()
            shutil.copy2(ROOT / 'scripts/release-receipt.py', base / 'scripts/release-receipt.py')
            (base / 'content/index.md').write_text('public')
            (base / 'public/index.html').write_text('public')
            command = ['python3', str(base / 'scripts/release-receipt.py')]
            subprocess.run(command + ['write'], check=True)
            subprocess.run(command + ['verify'], check=True, capture_output=True)
            (base / 'public/stale.pdf').write_text('private')
            self.assertNotEqual(subprocess.run(command + ['verify'], capture_output=True).returncode, 0)

if __name__ == '__main__':
    unittest.main()
