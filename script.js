// 双语切换逻辑
class BlogI18n {
    constructor() {
        this.currentLang = 'en';
        this.init();
    }
    
    init() {
        // 从 localStorage 读取语言偏好
        const savedLang = localStorage.getItem('blog-language');
        if (savedLang) {
            this.currentLang = savedLang;
        }
        
        // 初始化页面
        this.updateAllText();
        this.bindEvents();
    }
    
    bindEvents() {
        const langSwitch = document.getElementById('langSwitch');
        if (langSwitch) {
            langSwitch.addEventListener('click', () => this.toggleLanguage());
        }
    }
    
    toggleLanguage() {
        this.currentLang = this.currentLang === 'en' ? 'zh' : 'en';
        localStorage.setItem('blog-language', this.currentLang);
        this.updateAllText();
    }
    
    updateAllText() {
        // 更新语言切换按钮文字
        const langSwitch = document.getElementById('langSwitch');
        if (langSwitch) {
            langSwitch.textContent = this.currentLang === 'en' ? '中文' : 'English';
        }
        
        // 更新 HTML lang 属性
        document.documentElement.lang = this.currentLang;
        
        // 更新所有带有 data-en 和 data-zh 属性的元素
        const elements = document.querySelectorAll('[data-en][data-zh]');
        elements.forEach(el => {
            const text = el.getAttribute(`data-${this.currentLang}`);
            if (text) {
                el.textContent = text;
            }
        });
        
        // 切换文章正文内容
        this.toggleArticleContent();
    }
    
    toggleArticleContent() {
        // 切换所有文章摘要的中英文内容
        const contentEnList = document.querySelectorAll('.content-en');
        const contentZhList = document.querySelectorAll('.content-zh');
        
        contentEnList.forEach(contentEn => {
            if (this.currentLang === 'en') {
                contentEn.style.display = 'block';
            } else {
                contentEn.style.display = 'none';
            }
        });
        
        contentZhList.forEach(contentZh => {
            if (this.currentLang === 'en') {
                contentZh.style.display = 'none';
            } else {
                contentZh.style.display = 'block';
            }
        });
    }
}

// 平滑滚动到锚点
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 160; // 顶部装饰条 + 导航栏高度
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// 导航栏活跃状态
function updateActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navigation a[href^="#"]');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// 阅读进度指示器
function updateReadingProgress() {
    const article = document.querySelector('.article');
    if (!article) return;
    
    const articleTop = article.offsetTop;
    const articleHeight = article.offsetHeight;
    const windowHeight = window.innerHeight;
    const scrollTop = window.pageYOffset;
    
    // 计算阅读进度
    const progress = Math.min(
        Math.max((scrollTop - articleTop + windowHeight) / articleHeight, 0),
        1
    );
    
    // 可以在这里添加进度条显示逻辑
    // console.log(`阅读进度: ${Math.round(progress * 100)}%`);
}

// 节流函数
function throttle(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        if (!timeout) {
            timeout = setTimeout(() => {
                timeout = null;
                func.apply(context, args);
            }, wait);
        }
    };
}

// 滚动事件监听
window.addEventListener('scroll', throttle(() => {
    updateReadingProgress();
}, 100));

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new BlogI18n();
    
    // 添加页面加载动画
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 50);
});

// 图片懒加载
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// 代码块复制功能
document.querySelectorAll('pre code').forEach(block => {
    const pre = block.parentElement;
    
    // 创建复制按钮
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.textContent = 'Copy';
    copyButton.style.cssText = `
        position: absolute;
        top: 8px;
        right: 8px;
        background: #e5e7eb;
        border: none;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.75rem;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.2s;
    `;
    
    // 设置 pre 为相对定位
    pre.style.position = 'relative';
    
    // 鼠标悬停时显示按钮
    pre.addEventListener('mouseenter', () => {
        copyButton.style.opacity = '1';
    });
    
    pre.addEventListener('mouseleave', () => {
        copyButton.style.opacity = '0';
    });
    
    // 复制功能
    copyButton.addEventListener('click', async () => {
        const code = block.textContent;
        try {
            await navigator.clipboard.writeText(code);
            copyButton.textContent = 'Copied!';
            setTimeout(() => {
                copyButton.textContent = 'Copy';
            }, 2000);
        } catch (err) {
            console.error('复制失败:', err);
        }
    });
    
    pre.appendChild(copyButton);
});

// 键盘快捷键
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Shift + L: 切换语言
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'L') {
        e.preventDefault();
        const langSwitch = document.getElementById('langSwitch');
        if (langSwitch) {
            langSwitch.click();
        }
    }
});

// 控制台欢迎信息
console.log('%c欢迎访问博客!', 'color: #2563eb; font-size: 20px; font-weight: bold;');
console.log('%c使用 Ctrl/Cmd + Shift + L 快速切换语言', 'color: #6b7280; font-size: 12px;');
