#!/usr/bin/env python3
"""Validate static inputs and generated output before recording or deploying a build."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'scripts/static-manifest.json'
SENSITIVE = re.compile(rb'(?:[a-z0-9-]+\.)*bilibili\.co\b|/Users/|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:ghp_|github_pat_)[A-Za-z0-9_]+', re.I)

def inventory(base):
    if base.is_symlink() or not base.is_dir():
        raise SystemExit(f'必须为真实目录: {base}')
    result = {}
    for p in base.rglob('*'):
        rel = p.relative_to(base)
        if p.is_symlink() or any(x.startswith('.') for x in rel.parts):
            raise SystemExit(f'禁止软链接或隐藏路径: {rel}')
        if p.is_file():
            data = p.read_bytes()
            if SENSITIVE.search(data):
                raise SystemExit(f'发现敏感特征: {rel}')
            result[rel.as_posix()] = hashlib.sha256(data).hexdigest()
        elif not p.is_dir():
            raise SystemExit(f'禁止特殊文件: {rel}')
    return result

approved = json.loads(MANIFEST.read_text())
if inventory(ROOT / 'quartz/static') != approved:
    raise SystemExit('静态资源清单或内容变化，必须逐项审阅并更新 static-manifest.json')
if len(sys.argv) > 1:
    output = Path(sys.argv[1])
    files = inventory(output)
    extensions = {'.html', '.css', '.js', '.json', '.xml', '.webp', '.png', '.jpg', '.jpeg', '.gif', '.avif', '.ico'}
    for name, digest in files.items():
        if name.startswith('static/') and name != 'static/contentIndex.json' and approved.get(name[7:]) != digest:
            raise SystemExit(f'未审阅的静态产物: {name}')
        if Path(name).suffix not in extensions and name != 'robots.txt':
            raise SystemExit(f'未允许的产物: {name}')
        if any(x in name for x in ['待归档', 'personal_knowledge', '.public-backup', 'AGENTS.md']):
            raise SystemExit(f'私有路径出现在产物中: {name}')
    if not {'index.html', 'robots.txt', 'sitemap.xml'} <= files.keys():
        raise SystemExit('缺少必需产物')
print('静态资源/产物边界检查通过')
