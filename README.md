# 悬浮猫图书馆

Quartz 博客。`content/` 是独立的公开副本，构建和部署不读取私有知识库。

## 准备文章

在本目录运行，明确列出相对于来源目录的每个文件：

```bash
python3 scripts/copy-content.py --source /path/to/private-notes 'articles/example.md'
# 审阅清单、正文差异及附件后，使用同一文件列表执行复制：
python3 scripts/copy-content.py --source /path/to/private-notes 'articles/example.md' --apply
```

不自动发现来源目录、不根据 publish/tag 筛选、不自动复制链接或嵌入的笔记。
现有 publish 字段只是历史元数据，即使是 false 也不阻止公开；进入 content 即表示公开。
博客首页独立维护，不复制知识库索引。保留文章路径和 aliases 可维持旧 URL。

## 构建、预览、发布

需要 Node.js 22+、npm、Python 3 及已安装依赖（首次 `npm ci`）。

```bash
npm run content:check
npm run build
python3 -m http.server 8080 --directory public
# 在浏览器预览并审阅后，另一个终端运行：
./deploy.sh
```

构建使用全新临时目录，成功后替换 public，并记录文件 SHA-256。
部署验证内容及产物未变化，只上传本次产物，不重新复制或构建。
部署保留既有 gh-pages 分支无父提交发布方式，使用 force-with-lease 防止覆盖并发更新；只有显式执行 deploy.sh 才会推送。

检查阻止软链接、隐藏文件、未允许类型、缺失/歧义本地引用、原始 HTML，
并扫描部分内部域名、本机路径及凭证特征。它不能代替对正文和图片的人工审阅。
当前允许 md/png/jpg/jpeg/webp/gif/avif；PDF、SVG 等须专门审阅后调整规则。
`quartz/static` 额外受 `scripts/static-manifest.json` 的文件名和 SHA-256 清单约束；新增或修改资源先审阅再更新清单。
构建后扫描产物类型、敏感特征和静态资源哈希；部署再校验实际上传副本。
不支持的链接写法应转换为标准 Markdown 或明确的 Wiki 链接。

移除公开文件后须重新构建、预览及部署。旧 public 备份仅保存在本地并被 Git 忽略，
不能作为发布输入。重新部署不等于清除远端 Git 历史或第三方缓存。

## 验证

```bash
python3 scripts/test-isolation.py
```
