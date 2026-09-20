#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/check-content.mjs
python3 scripts/check-release.py
mkdir -p .release
STAGE="$(mktemp -d "$PWD/.release/build.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
node quartz/bootstrap-cli.mjs build -d content -o "$STAGE/site"
cat > "$STAGE/site/robots.txt" <<'ROBOTS'
User-agent: *
Allow: /

Sitemap: https://stugrua.github.io/blog/sitemap.xml
ROBOTS
python3 scripts/check-release.py "$STAGE/site"
# 已存在的产物保留为本地备份，绝不合并进入本次产物。
if [ -e public ] || [ -L public ]; then
  BACKUP="$(mktemp -d "$PWD/.public-backup-XXXXXXXX")"
  mv public "$BACKUP/public"
fi
mv "$STAGE/site" public
python3 scripts/release-receipt.py write
echo '构建完成。预览 public 并审阅后，运行 ./deploy.sh 发布这份产物。'
