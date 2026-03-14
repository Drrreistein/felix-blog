#!/usr/bin/env python3
"""
一键发布文章脚本
使用方法：python3 publish.py your-article.md
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 配置
TEMPLATE_DIR = Path(__file__).parent
ARTICLES_DIR = TEMPLATE_DIR / "articles"

def parse_markdown(filepath):
    """解析 Markdown 文件，提取标题、日期和内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 YAML frontmatter
    metadata = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
    
    # 如果没有 frontmatter，尝试从内容提取
    if 'title' not in metadata:
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break
    
    if 'date' not in metadata:
        metadata['date'] = datetime.now().strftime('%Y-%m-%d')
    
    return metadata, body

def generate_slug(title):
    """从标题生成 URL slug"""
    # 简单处理：转小写，空格转连字符
    slug = title.lower().replace(' ', '-').replace('?', '').replace('!', '')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug

def convert_markdown_to_html(markdown_text):
    """简单的 Markdown 到 HTML 转换"""
    html = markdown_text
    
    # 标题
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 粗体
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    
    # 代码块
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 引用
    html = re.sub(r'^> (.*$)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 段落
    paragraphs = html.split('\n\n')
    html = '\n'.join([f'<p>{p}</p>' if not p.strip().startswith('<') else p for p in paragraphs])
    
    return html

def generate_article_html(metadata, body, slug):
    """生成文章 HTML 页面"""
    title = metadata.get('title', 'Untitled')
    date = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = metadata.get('tags', '').split(',') if 'tags' in metadata else []
    
    # 转换 Markdown 为 HTML
    content_html = convert_markdown_to_html(body)
    
    # 格式化日期
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_en = date_obj.strftime('%B %d, %Y')
    date_zh = date_obj.strftime('%Y年%m月%d日')
    
    # 生成标签 HTML
    tags_html = '\n'.join([f'<span class="tag">{tag.strip()}</span>' for tag in tags if tag.strip()])
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-en="{title} - Your Name's Thoughts and Writings" data-zh="{title} - 你的名字 的思考与写作">{title} - Your Name's Thoughts and Writings</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Georgia:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- 顶部装饰条 -->
    <div class="top-decoration">
        <svg viewBox="0 0 1440 100" preserveAspectRatio="none">
            <path fill="#1e40af" fill-opacity="0.8" d="M0,40 C150,80 350,0 500,40 C650,80 850,0 1000,40 C1150,80 1350,0 1440,40 L1440,0 L0,0 Z"></path>
            <path fill="#3b82f6" fill-opacity="0.6" d="M0,60 C180,20 320,80 480,60 C640,40 820,90 980,60 C1140,30 1300,80 1440,60 L1440,0 L0,0 Z"></path>
            <path fill="#60a5fa" fill-opacity="0.4" d="M0,80 C160,50 280,90 440,80 C600,70 760,95 920,80 C1080,65 1280,85 1440,75 L1440,0 L0,0 Z"></path>
        </svg>
    </div>

    <!-- 头部区域 -->
    <header class="header">
        <div class="header-content">
            <div class="blog-identity">
                <div class="avatar-container">
                    <video autoplay muted loop playsinline class="avatar avatar-video">
                        <source src="Bark.mp4" type="video/mp4">
                    </video>
                </div>
                <h1 class="blog-title" data-en="Your Name's Thoughts and Writings" data-zh="你的名字 的思考与写作">Your Name's Thoughts and Writings</h1>
            </div>
            <nav class="navigation">
                <a href="index.html#blog" data-en="blog" data-zh="博客">blog</a>
                <a href="archive.html" data-en="archive" data-zh="归档">archive</a>
                <a href="projects.html" data-en="projects" data-zh="项目">projects</a>
                <a href="about.html" data-en="about" data-zh="关于">about</a>
            </nav>
            <button class="lang-switch" id="langSwitch">中文</button>
        </div>
    </header>

    <!-- 文章主体区 -->
    <main class="main-content">
        <article class="article">
            <h1 class="article-title article-title-full">{title}</h1>
            <p class="article-date">
                <span class="date-text" data-en="written on {date_en}" data-zh="写于 {date_zh}">written on {date_en}</span>
            </p>
            
            <div class="article-body">
                {content_html}
            </div>
            
            <!-- 标签区 -->
            <div class="article-tags">
                {tags_html}
            </div>
        </article>
    </main>

    <!-- 底部 -->
    <footer class="footer">
        <div class="footer-content">
            <p class="copyright" data-en="© 2026 Your Name. All rights reserved." data-zh="© 2026 你的名字。保留所有权利。">© 2026 Your Name. All rights reserved.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''
    
    return html_template

def main():
    if len(sys.argv) < 2:
        print("❌ 使用方法: python3 publish.py your-article.md")
        print("\n📝 Markdown 文件格式示例:")
        print("""
---
title: 文章标题
date: 2026-03-15
tags: Tag1, Tag2, Tag3
---

# 文章标题

这里是文章内容...

## 二级标题

更多内容...
""")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    
    if not md_file.exists():
        print(f"❌ 文件不存在: {md_file}")
        sys.exit(1)
    
    print(f"📄 正在处理: {md_file}")
    
    # 解析 Markdown
    metadata, body = parse_markdown(md_file)
    title = metadata.get('title', 'Untitled')
    slug = generate_slug(title)
    
    print(f"✓ 标题: {title}")
    print(f"✓ 日期: {metadata.get('date', 'today')}")
    print(f"✓ Slug: {slug}")
    
    # 生成 HTML
    html_content = generate_article_html(metadata, body, slug)
    
    # 保存文件
    output_file = TEMPLATE_DIR / f"article-{slug}.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"\n✅ 文章已生成: {output_file.name}")
    print(f"\n💡 下一步:")
    print(f"   1. 在主页 index.html 添加文章链接")
    print(f"   2. 在归档页 archive.html 添加文章")
    print(f"   3. git add . && git commit -m 'Add article: {title}'")

if __name__ == '__main__':
    main()
