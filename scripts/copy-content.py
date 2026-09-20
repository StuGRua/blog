#!/usr/bin/env python3
"""只复制显式列出的文件；默认预览，--apply 才写入。不读取 publish/tag。"""
import argparse
import difflib
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', required=True, type=Path)
parser.add_argument('--apply', action='store_true')
parser.add_argument('files', nargs='+', help='相对 source 的具体文件路径，不支持目录或通配符')
args = parser.parse_args()
root = args.source.absolute()
dest = Path(__file__).resolve().parents[1] / 'content'

def no_links(p):
    for part in [p, *p.parents]:
        if part.is_symlink():
            raise SystemExit(f'禁止软链接: {part}')

pending = []
for name in args.files:
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or any(x.startswith('.') for x in rel.parts):
        raise SystemExit(f'禁止越界/隐藏路径: {name}')
    src, dst = root / rel, dest / rel
    no_links(src)
    no_links(dst)
    if not src.is_file() or src.suffix.lower() not in {'.md', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif'}:
        raise SystemExit(f'不是允许的文章/附件文件: {name}')
    print(f'{"更新" if dst.exists() else "新增"}: {name}')
    if src.suffix == '.md':
        before = dst.read_text() if dst.exists() else ''
        print(''.join(difflib.unified_diff(before.splitlines(True), src.read_text().splitlines(True), fromfile='公开副本', tofile=name)))
    else:
        print(f'附件 {src.stat().st_size} bytes；需人工审阅图片内容')
    pending.append((src, dst))
if args.apply:
    for src, dst in pending:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print('复制完成；运行 npm run content:check 和 npm run build，审阅后再发布。')
else:
    print('仅预览；审阅上述差异后使用 --apply。不会自动复制引用文件。')
