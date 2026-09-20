#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
receipt = root / '.release' / 'receipt.json'

def snapshot():
    result = {}
    for name in ['content', 'public']:
        base = Path(sys.argv[2]) if name == 'public' and len(sys.argv) > 2 else root / name
        if base.is_symlink() or not base.is_dir():
            raise SystemExit(f'{name} 必须为真实目录')
        for p in sorted(base.rglob('*')):
            if p.is_symlink():
                raise SystemExit(f'禁止软链接: {p}')
            if p.is_file():
                result[name + '/' + p.relative_to(base).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result

current = snapshot()
if sys.argv[1] == 'write':
    receipt.parent.mkdir(exist_ok=True)
    receipt.write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n')
else:
    if not receipt.exists() or current != json.loads(receipt.read_text()):
        raise SystemExit('内容或产物发生变化，请重新构建并审阅后再发布')
    print('发布文件与本次构建记录一致')
