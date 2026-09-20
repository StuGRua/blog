import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { unified } from "unified"
import matter from "gray-matter"
import remarkParse from "remark-parse"
import remarkFrontmatter from "remark-frontmatter"
import { visit } from "unist-util-visit"

const root = path.resolve(process.argv[2] ?? fileURLToPath(new URL("../content", import.meta.url)))
const allowed = new Set([".md", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"])
const files = []
function walk(p) {
  const s = fs.lstatSync(p)
  if (s.isSymbolicLink()) throw new Error(`禁止软链接: ${p}`)
  if (s.isDirectory()) {
    for (const n of fs.readdirSync(p)) {
      if (n.startsWith(".")) throw new Error(`禁止隐藏文件/目录: ${p}/${n}`)
      walk(path.join(p, n))
    }
  } else {
    if (!s.isFile() || !allowed.has(path.extname(p).toLowerCase()))
      throw new Error(`未允许的文件类型: ${p}`)
    files.push(p)
  }
}
walk(root)
if (!files.includes(path.join(root, "index.md"))) throw new Error("缺少博客首页 index.md")
function checkLink(raw, from) {
  if (/^(https?:\/\/|mailto:|tel:|#)/i.test(raw)) return
  if (/^[a-z][a-z\d+.-]*:|^\/\//i.test(raw)) throw new Error(`不支持的链接协议: ${from}: ${raw}`)
  const target = decodeURIComponent(raw.split(/[?#]/)[0]).replaceAll("\\", "/")
  if (!target) return
  if (target.split("/").includes("..") || target.startsWith("/Users/"))
    throw new Error(`禁止越界引用: ${from}: ${raw}`)
  const rel = target.replace(/^\//, "")
  const candidates = [path.resolve(path.dirname(from), target), path.join(root, rel)]
  const matches = files.filter(
    (f) =>
      candidates.includes(f) ||
      candidates.includes(f.replace(/\.md$/, "")) ||
      (!rel.includes("/") && (path.basename(f) === rel || path.basename(f, ".md") === rel)),
  )
  if (matches.length !== 1) throw new Error(`引用缺失或歧义: ${from}: ${raw}`)
}
for (const f of files.filter((f) => f.endsWith(".md"))) {
  const text = fs.readFileSync(f, "utf8")
  if (
    /(?:info|git|aistudio|cloud)\.bilibili\.co\b|\/Users\/|-----BEGIN .*PRIVATE KEY-----|\b(?:ghp_|github_pat_)[A-Za-z0-9_]+/.test(
      text,
    )
  )
    throw new Error(`发现内部地址、本机路径或凭证特征，请审阅: ${f}`)
  const metadata = matter(text).data
  for (const key of ["alias", "aliases", "permalink", "tags", "tag"]) {
    for (const value of [metadata[key] ?? []].flat()) {
      const v = String(value)
      if (v.startsWith("/") || v.includes("..") || /[\\<>:\x00-\x1f]/.test(v))
        throw new Error(`不安全的元数据路径: ${f}: ${key}`)
    }
  }
  const tree = unified().use(remarkParse).use(remarkFrontmatter, ["yaml"]).parse(text)
  const definitions = new Set()
  visit(tree, "definition", (n) => definitions.add(n.identifier))
  visit(tree, (n) => {
    if (["link", "image", "definition"].includes(n.type)) checkLink(n.url, f)
    if (["linkReference", "imageReference"].includes(n.type) && !definitions.has(n.identifier))
      throw new Error(`引用定义缺失: ${f}`)
    if (n.type === "html") throw new Error(`公开正文暂不允许原始 HTML，请转换为 Markdown: ${f}`)
    if (n.type === "text")
      for (const m of n.value.matchAll(/\[\[([^\]]+)\]\]/g)) checkLink(m[1].split("|")[0], f)
  })
}
console.log(
  `公开内容检查通过：${files.length} 个文件；附件允许 png/jpg/jpeg/webp/gif/avif，其他类型需单独审阅并调整规则。`,
)
