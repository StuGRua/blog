#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
node scripts/check-content.mjs
python3 scripts/check-release.py public
python3 scripts/release-receipt.py verify
# 只发布已构建、已预览的产物，不在部署阶段构建或访问知识库。
OLD_HEAD="$(git ls-remote origin refs/heads/gh-pages | cut -f1)"
[ -n "$OLD_HEAD" ]
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
cp -R public/. "$STAGE/"
python3 scripts/release-receipt.py verify "$STAGE"
cd "$STAGE"
git init -b gh-pages
git config user.name "RefactoringHero"
git config user.email "stug_iii@foxmail.com"
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M:%S')"
git remote add origin https://github.com/StuGRua/blog.git
git push --force-with-lease=refs/heads/gh-pages:"$OLD_HEAD" origin gh-pages
echo 'Published: https://stugrua.github.io/blog/'
