#!/usr/bin/env python3
"""
博客发布和部署脚本
支持双语 Markdown 文件（中文.md + 英文.md）

使用方法:
1. 单语文章: python3 deploy.py article.md
2. 双语文章: python3 deploy.py article-zh.md article-en.md
3. 部署到服务器: python3 deploy.py --deploy
"""

import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
TEMPLATE_DIR = Path(__file__).parent
SERVER_IP = "47.253.217.45"
SERVER_USER = "admin"
SERVER_PATH = "/var/www/blog"

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
    slug = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace('，', '').replace('。', '')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug[:50]  # 限制长度

def convert_markdown_to_html(markdown_text):
    """简单的 Markdown 到 HTML 转换"""
    html = markdown_text
    
    # 标题
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'', html, flags=re.MULTILINE)  # 移除 h1，因为模板中已有标题
    
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
    
    # 列表
    html = re.sub(r'^- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 段落
    paragraphs = html.split('\n\n')
    result = []
    in_list = False
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(p)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if not p.startswith('<'):
                result.append(f'<p>{p}</p>')
            else:
                result.append(p)
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def generate_bilingual_article_html(metadata_zh, body_zh, metadata_en, body_en, slug):
    """生成双语文章 HTML 页面"""
    title_zh = metadata_zh.get('title', '无标题')
    title_en = metadata_en.get('title', 'Untitled')
    date = metadata_zh.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = metadata_zh.get('tags', '').split(',') if 'tags' in metadata_zh else []
    
    # 转换 Markdown 为 HTML
    content_zh = convert_markdown_to_html(body_zh)
    content_en = convert_markdown_to_html(body_en)
    
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
    <title data-en="{title_en} - Felix Xu's Thoughts and Writings" data-zh="{title_zh} - 磊 的思考与写作">{title_en} - Felix Xu's Thoughts and Writings</title>
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
                <div class="avatar-container"><video autoplay muted loop playsinline class="avatar avatar-video"><source src="Bark.mp4" type="video/mp4"></video></div>
                <h1 class="blog-title" data-en="Felix Xu's Thoughts and Writings" data-zh="磊 的思考与写作">Felix Xu's Thoughts and Writings</h1>
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
            <h1 class="article-title article-title-full" data-en="{title_en}" data-zh="{title_zh}">{title_en}</h1>
            <p class="article-date">
                <span class="date-text" data-en="written on {date_en}" data-zh="写于 {date_zh}">written on {date_en}</span>
            </p>
            
            <div class="article-body">
                <div class="content-en">
{content_en}
                </div>
                
                <div class="content-zh" style="display: none;">
{content_zh}
                </div>
            </div>
            
            <!-- 标签区 -->
            <div class="article-tags">
{tags_html}
            </div>
        </article>

        <!-- 文章导航 -->
        <div class="article-nav">
            <a href="index.html#blog" class="nav-prev" data-en="← Back to Blog" data-zh="← 返回博客">← Back to Blog</a>
        </div>
    </main>

    <!-- 底部 -->
    <footer class="footer">
        <div class="footer-content">
            <p class="copyright" data-en="© 2026 Felix Xu. All rights reserved." data-zh="© 2026 磊。保留所有权利。">© 2026 Felix Xu. All rights reserved.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''
    
    return html_template

def deploy_to_server():
    """部署到服务器"""
    print("🚀 开始部署到服务器...")
    
    # 要上传的文件
    files_to_upload = [
        "index.html", "about.html", "archive.html", "projects.html",
        "styles.css", "script.js", "Bark.mp4"
    ]
    
    # 添加所有文章文件
    for f in TEMPLATE_DIR.glob("article-*.html"):
        files_to_upload.append(f.name)
    
    # 使用 scp 上传文件
    for file in files_to_upload:
        local_path = TEMPLATE_DIR / file
        if local_path.exists():
            print(f"  📤 上传 {file}...")
            cmd = f"scp '{local_path}' {SERVER_USER}@{SERVER_IP}:{SERVER_PATH}/"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  ❌ 上传失败: {file}")
                print(f"     错误: {result.stderr}")
        else:
            print(f"  ⚠️ 文件不存在: {file}")
    
    print("✅ 部署完成！")
    print(f"🌐 访问地址: http://{SERVER_IP}")

def main():
    if len(sys.argv) < 2:
        print("""📖 使用方法:

1. 发布双语文章:
   python3 deploy.py article-zh.md article-en.md

2. 仅部署到服务器（不上传新文章）:
   python3 deploy.py --deploy

3. 发布单语文章:
   python3 deploy.py article.md

💡 Markdown 文件格式示例:
---
title: 文章标题
date: 2026-03-15
tags: Tag1, Tag2, Tag3
---

# 文章标题

这里是文章内容...
""")
        sys.exit(1)
    
    # 仅部署模式
    if sys.argv[1] == '--deploy':
        deploy_to_server()
        sys.exit(0)
    
    # 处理 Markdown 文件
    if len(sys.argv) == 3:
        # 双语模式
        zh_file = Path(sys.argv[1])
        en_file = Path(sys.argv[2])
        
        if not zh_file.exists() or not en_file.exists():
            print("❌ 文件不存在")
            sys.exit(1)
        
        print(f"📄 处理中文: {zh_file}")
        print(f"📄 处理英文: {en_file}")
        
        metadata_zh, body_zh = parse_markdown(zh_file)
        metadata_en, body_en = parse_markdown(en_file)
        
        title_zh = metadata_zh.get('title', '无标题')
        slug = generate_slug(title_zh)
        
        print(f"✓ 中文标题: {title_zh}")
        print(f"✓ 英文标题: {metadata_en.get('title', 'Untitled')}")
        print(f"✓ 日期: {metadata_zh.get('date', 'today')}")
        print(f"✓ Slug: {slug}")
        
        # 生成 HTML
        html_content = generate_bilingual_article_html(metadata_zh, body_zh, metadata_en, body_en, slug)
        output_file = TEMPLATE_DIR / f"article-{slug}.html"
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"\n✅ 文章已生成: {output_file.name}")
        
    else:
        # 单语模式
        md_file = Path(sys.argv[1])
        if not md_file.exists():
            print(f"❌ 文件不存在: {md_file}")
            sys.exit(1)
        
        print(f"📄 处理: {md_file}")
        metadata, body = parse_markdown(md_file)
        title = metadata.get('title', 'Untitled')
        slug = generate_slug(title)
        
        print(f"✓ 标题: {title}")
        print(f"✓ 日期: {metadata.get('date', 'today')}")
        print(f"✓ Slug: {slug}")
        
        # 生成 HTML（使用原有模板）
        from publish import generate_article_html
        html_content = generate_article_html(metadata, body, slug)
        output_file = TEMPLATE_DIR / f"article-{slug}.html"
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"\n✅ 文章已生成: {output_file.name}")
    
    print("\n💡 下一步:")
    print("   1. 在主页 index.html 添加文章链接")
    print("   2. 在归档页 archive.html 添加文章")
    print("   3. 运行: python3 deploy.py --deploy")
    print("   4. git add . && git commit -m 'Add new article'")

if __name__ == '__main__':
    main()
