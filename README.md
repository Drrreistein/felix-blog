# 双语博客主页

这是一个支持中英文切换的现代博客主页模板，具有清晰的排版和优雅的交互体验。

## 项目结构

```
/Users/a1-6/WorkBuddy/20260313105301/
├── index.html          # 主页面文件
├── styles.css          # 样式文件
├── script.js           # JavaScript交互逻辑
├── articles.json       # 示例文章数据
└── README.md           # 项目说明文档
```

## 功能特性

### 1. 页面结构

- **顶部装饰条**: 蓝调抽象波浪图案，固定在页面顶部
- **头部区域**: 包含头像、博客标题和导航栏
- **文章主体区**: 最大宽度限制，居中显示，**以卡片形式展示最新5篇文章摘要**
- **底部区域**: 极简版权信息

### 1.1 文章卡片布局

主页采用卡片式布局展示文章：

- **卡片数量**: 显示最新5篇文章
- **卡片内容**: 标题、日期、摘要（中英文）、标签、"阅读更多"按钮
- **交互效果**: 鼠标悬停时卡片上浮、边框高亮、阴影增强
- **响应式**: 完美适配桌面端和移动端

### 2. 视觉设计

- **配色方案**: 深蓝色 (#1a365d) 标题，蓝色 (#2563eb) 链接
- **字体**: Georgia (标题) + Inter (正文)
- **排版**: 行高 1.7，清晰的段落间距
- **代码块**: 浅灰背景，等宽字体，支持复制功能

### 3. 双语支持

- **语言切换**: 点击右上角按钮或使用快捷键 `Ctrl/Cmd + Shift + L`
- **持久化**: 自动保存语言偏好到 localStorage
- **动态切换**: 标题、导航、日期、正文全部支持双语

### 4. 交互功能

- **平滑滚动**: 点击导航链接平滑滚动到目标位置
- **代码复制**: 鼠标悬停代码块显示复制按钮
- **阅读进度**: 自动计算并显示阅读进度
- **响应式设计**: 完美适配桌面端和移动端

## 使用方法

### 本地预览

1. 直接在浏览器中打开 `index.html` 文件
2. 或使用本地服务器:
   ```bash
   cd /Users/a1-6/WorkBuddy/20260313105301
   python3 -m http.server 8080
   ```
   然后访问 `http://localhost:8080`

### 自定义内容

#### 修改博客标题和头像

在 `index.html` 中找到以下部分并修改:

```html
<div class="blog-identity">
    <img src="your-avatar-url" alt="Avatar" class="avatar">
    <h1 class="blog-title">Your Name's Thoughts and Writings</h1>
</div>
```

#### 添加新文章

在 `index.html` 的 `<main class="main-content">` 区域添加新的文章卡片:

```html
<article class="article-card">
    <div class="article-header">
        <h2 class="article-title">
            <a href="article.html?id=your-article-id" data-en="Article Title" data-zh="文章标题">Article Title</a>
        </h2>
        <p class="article-date">
            <span class="date-text" data-en="written on March 10, 2026" data-zh="写于 2026年03月10日">written on March 10, 2026</span>
        </p>
    </div>
    
    <div class="article-excerpt">
        <div class="content-en">
            <p>English excerpt here...</p>
        </div>
        <div class="content-zh" style="display: none;">
            <p>中文摘要在这里...</p>
        </div>
    </div>
    
    <div class="article-footer">
        <div class="article-tags">
            <span class="tag">Tag1</span>
            <span class="tag">Tag2</span>
        </div>
        <a href="article.html?id=your-article-id" class="read-more" data-en="Read more →" data-zh="阅读更多 →">Read more →</a>
    </div>
</article>
```

#### 修改导航链接

在 `index.html` 中找到 `<nav class="navigation">` 并修改链接:

```html
<nav class="navigation">
    <a href="#blog" data-en="blog" data-zh="博客">blog</a>
    <a href="#archive" data-en="archive" data-zh="归档">archive</a>
    <!-- 添加更多链接 -->
</nav>
```

## 技术栈

- **HTML5**: 语义化标签，结构清晰
- **CSS3**: Flexbox布局，CSS变量，响应式设计
- **JavaScript (ES6+)**: 类、箭头函数、异步操作
- **Google Fonts**: Inter 和 Georgia 字体

## 浏览器兼容性

- Chrome/Edge (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- 移动浏览器 (iOS Safari, Chrome Mobile)

## 性能优化

- 字体预连接 (`preconnect`)
- 图片懒加载 (Intersection Observer)
- 节流滚动事件
- CSS变量减少重复代码

## 自定义样式

在 `styles.css` 中修改 CSS 变量可以快速更改主题颜色:

```css
:root {
    --primary-blue: #2563eb;    /* 主要蓝色 */
    --dark-blue: #1a365d;        /* 深蓝色 */
    --text-color: #1f2937;       /* 正文颜色 */
    --light-gray: #6b7280;       /* 浅灰色 */
    --bg-gray: #f3f4f6;          /* 背景灰色 */
}
```

## 开发建议

1. **SEO优化**: 为每个文章页面创建独立的 HTML 文件
2. **路由设计**: 可以使用 `/en/` 和 `/zh/` 前缀区分语言版本
3. **内容管理**: 集成 Markdown 解析器动态渲染文章内容
4. **评论系统**: 集成 Disqus 或其他评论服务
5. **分析工具**: 添加 Google Analytics 或其他分析工具

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
