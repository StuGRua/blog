#!/bin/bash
set -e

BLOG_DIR="$(cd "$(dirname "$0")" && pwd)"
PUBLIC_DIR="$BLOG_DIR/public"

source ~/.nvm/nvm.sh
nvm use 22 > /dev/null 2>&1

echo "Building Quartz..."
cd "$BLOG_DIR"
npx quartz build

echo "Writing robots.txt..."
cat > "$PUBLIC_DIR/robots.txt" <<ROBOTS
User-agent: *
Allow: /

Sitemap: https://stugrua.github.io/blog/sitemap.xml
ROBOTS

echo "Deploying to gh-pages..."
cd "$PUBLIC_DIR"
git init
git checkout -b gh-pages
git config user.name "RefactoringHero"
git config user.email "stug_iii@foxmail.com"
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M:%S')"
git remote add origin https://github.com/StuGRua/blog.git
git push -f origin gh-pages

rm -rf "$PUBLIC_DIR/.git"
echo "Done! Site will be live at https://stugrua.github.io/blog/"
