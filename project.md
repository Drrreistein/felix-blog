---
type: project
id: project-blog-001
created: 2026-03-21
status: active
tags: [blog, writing, personal-brand]
---

# 个人博客（felix-blog）

## 基本信息
- **博客名称**：Felix Xu's Thoughts and Writings（磊 的思考与写作）
- **网址**：https://felix-blogs.vercel.app/
- **GitHub**：https://github.com/Drrreistein/felix-blog
- **本地路径**：`vault/01-projects/个人博客/`
- **托管平台**：Vercel（CI/CD 自动部署）

## 内容方向
- AI 与技术趋势
- 编程与软件工程
- 个人成长与方法论
- 偶尔：生活、阅读、项目

## 发布流程
1. 在 `drafts/` 中撰写文章
2. 使用 `skills/blog/scripts/publish.sh` 发布
3. 自动生成 HTML、更新 index.html 和 archive.html
4. 自动 git commit（可选自动 push）

## 目录结构
```
个人博客/
├── drafts/          # 博客草稿（发布前在此撰写）
├── published/       # 已发布存档
├── repo/            # GitHub 仓库镜像
│   ├── index.html
│   ├── archive.html
│   ├── article-*.html
│   ├── publish.py
│   └── ...
└── publish.sh       # 发布脚本（见 skills/blog/）
```

## 文章格式要求
```markdown
---
title: 文章标题
date: 2026-03-21
tags: AI, Technology
lang: zh  # 或 en，或 bilingual
---

# 文章标题

正文内容...
```

## 注意事项
- 中英双语文章：lang 写 bilingual，title 写成 `{en} | {zh}` 格式
- 文章slug自动从标题生成
- 标签影响文章分类和 SEO
