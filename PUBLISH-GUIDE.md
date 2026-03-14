# 如何发布新文章

## 🚀 超简单方法（推荐）

### 步骤 1: 准备 Markdown 文件

创建一个 Markdown 文件，格式如下：

```markdown
---
title: 文章标题
date: 2026-03-15
tags: Tag1, Tag2, Tag3
---

# 文章标题

这里是文章内容...

## 二级标题

更多内容...

### 三级标题

列表、代码块、链接等都支持：
- 列表项 1
- 列表项 2

`行内代码` 和代码块：

\`\`\`python
print("Hello, World!")
\`\`\`

[链接文字](https://example.com)

**粗体** 和 *斜体*

> 引用块
```

### 步骤 2: 运行发布脚本

```bash
python3 publish.py your-article.md
```

### 步骤 3: 手动更新索引

生成的文章页面会自动创建，但需要手动添加到主页和归档页：

1. **主页 (index.html)**: 在文章列表中添加新条目
2. **归档页 (archive.html)**: 在相应月份添加新文章

### 步骤 4: Git 提交

```bash
git add .
git commit -m "Add article: 文章标题"
```

## 📝 支持的 Markdown 语法

- ✅ 标题（# ## ###）
- ✅ 段落
- ✅ 链接 `[text](url)`
- ✅ 粗体 `**text**`
- ✅ 斜体 `*text*`
- ✅ 代码块 ` ```language ` 
- ✅ 行内代码 `` `code` ``
- ✅ 引用 `> text`
- ✅ 列表 `- item`

## 💡 提示

- 日期格式：`YYYY-MM-DD`（如 2026-03-15）
- 标签用逗号分隔：`Tag1, Tag2, Tag3`
- 文章标题会自动生成 URL slug
- 生成的文件名：`article-{slug}.html`

## 🎯 完整示例

```bash
# 1. 创建文章
cat > my-article.md << 'EOF'
---
title: My New Article
date: 2026-03-15
tags: Tutorial, Python
---

# My New Article

This is my new article...
EOF

# 2. 生成 HTML
python3 publish.py my-article.md

# 3. 更新 index.html 和 archive.html
# （手动添加链接）

# 4. 提交
git add .
git commit -m "Add article: My New Article"
```

## ⚡ 未来改进计划

- [ ] 自动更新主页和归档页
- [ ] 支持双语 Markdown
- [ ] 自动生成文章导航（上一篇/下一篇）
- [ ] 更完善的 Markdown 解析
