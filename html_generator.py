#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from jinja2 import Template
import logging
from config import Config

class HTMLGenerator:
    """HTML日报页面生成器"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
        self.config.ensure_directories()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/html_generator.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_daily_report(self, articles, summary):
        """生成日报HTML页面"""
        try:
            # 准备数据
            report_data = self.prepare_report_data(articles, summary)
            
            # 生成HTML内容
            html_content = self.render_template(report_data)
            
            # 保存HTML文件
            filename = self.save_html_file(html_content)
            
            self.logger.info(f"日报生成成功: {filename}")
            return html_content, filename
            
        except Exception as e:
            self.logger.error(f"日报生成失败: {str(e)}")
            raise
    
    def prepare_report_data(self, articles, summary):
        """准备报告数据"""
        current_date = datetime.now().strftime('%Y年%m月%d日')
        start_date, end_date = self.config.get_date_range()
        
        # 按期刊分组文章
        journals = {}
        for article in articles:
            journal_name = article['journal']
            if journal_name not in journals:
                journals[journal_name] = []
            journals[journal_name].append(article)
        
        # 统计信息
        total_articles = len(articles)
        journal_count = len(journals)
        
        return {
            'current_date': current_date,
            'start_date': start_date,
            'end_date': end_date,
            'summary': summary,
            'journals': journals,
            'total_articles': total_articles,
            'journal_count': journal_count,
            'articles': articles
        }
    
    def render_template(self, data):
        """渲染HTML模板"""
        template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学术期刊日报 - {{ current_date }}</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --background-color: #ffffff;
            --text-color: #2c3e50;
            --border-color: #e0e0e0;
            --accent-color: #e74c3c;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #1a1a1a;
                --text-color: #ffffff;
                --border-color: #444444;
                --primary-color: #3498db;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            transition: all 0.3s ease;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border-color);
        }
        
        .header h1 {
            color: var(--primary-color);
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .date {
            color: var(--secondary-color);
            font-size: 1.2em;
            font-weight: 300;
        }
        
        .header .stats {
            margin-top: 15px;
            font-size: 1.1em;
            color: var(--text-color);
            opacity: 0.8;
        }
        
        .summary-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .summary-section h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .summary-content {
            font-size: 1.1em;
            line-height: 1.8;
            text-align: justify;
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
        }
        
        .summary-content::-webkit-scrollbar {
            width: 6px;
        }
        
        .summary-content::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }
        
        .summary-content::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }
        
        .summary-content::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        
        .journals-section {
            margin-bottom: 40px;
        }
        
        .journals-section h2 {
            font-size: 2em;
            color: var(--primary-color);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .journal-card {
            background: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .journal-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .journal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .journal-name {
            font-size: 1.5em;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        .article-count {
            background: var(--secondary-color);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .articles-list {
            list-style: none;
        }
        
        .article-item {
            padding: 15px 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .article-item:last-child {
            border-bottom: none;
        }
        
        .article-title {
            font-size: 1.1em;
            font-weight: 500;
            margin-bottom: 5px;
            color: var(--text-color);
        }
        
        .article-title a {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .article-title a:hover {
            color: var(--secondary-color);
        }
        
        .article-meta {
            font-size: 0.9em;
            color: var(--text-color);
            opacity: 0.7;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            color: var(--text-color);
            opacity: 0.7;
            font-size: 0.9em;
        }
        
        .toc {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
            max-width: 250px;
            display: none;
        }
        
        .toc h3 {
            margin-bottom: 10px;
            color: var(--primary-color);
        }
        
        .toc ul {
            list-style: none;
        }
        
        .toc li {
            margin-bottom: 5px;
        }
        
        .toc a {
            color: var(--text-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .toc a:hover {
            color: var(--secondary-color);
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .summary-section {
                padding: 20px;
            }
            
            .journal-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .article-count {
                margin-top: 10px;
            }
            
            .toc {
                display: none !important;
            }
        }
        
        .highlight {
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 2px 5px;
            border-radius: 3px;
        }
        
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--secondary-color);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 1.5em;
            opacity: 0;
            transition: opacity 0.3s ease;
            cursor: pointer;
        }
        
        .back-to-top.visible {
            opacity: 1;
        }
    </style>
</head>
<body>
    <a href="#" class="back-to-top" id="backToTop">↑</a>
    
    <div class="container">
        <div class="header">
            <h1>📚 学术期刊日报</h1>
            <div class="date">{{ current_date }}</div>
            <div class="stats">
                覆盖 {{ journal_count }} 种期刊，共 {{ total_articles }} 篇文章
                <br>时间范围：{{ start_date }} 至 {{ end_date }}
            </div>
        </div>
        
        <section class="summary-section">
            <h2>🎯 今日导览摘要</h2>
            <div class="summary-content">
                {{ summary | replace('\\n', '<br>') }}
            </div>
        </section>
        
        <section class="journals-section">
            <h2>📖 期刊文章详情</h2>
            
            {% for journal_name, journal_articles in journals.items() %}
            <div class="journal-card" id="journal-{{ loop.index }}">
                <div class="journal-header">
                    <h3 class="journal-name">{{ journal_name }}</h3>
                    <span class="article-count">{{ journal_articles|length }} 篇文章</span>
                </div>
                <ul class="articles-list">
                    {% for article in journal_articles %}
                    <li class="article-item">
                        <div class="article-title">
                            <a href="{{ article.link }}" target="_blank" rel="noopener">
                                {{ article.title }}
                            </a>
                        </div>
                        <div class="article-meta">
                            发布日期：{{ article.date }} 
                            {% if article.abstract %}
                            • 摘要：{{ article.abstract }}
                            {% endif %}
                        </div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </section>
        
        <footer class="footer">
            <p>生成时间：{{ current_date }} {{ now().strftime('%H:%M:%S') }}</p>
            <p>本日报由AutoDLD系统自动生成，数据来源于各学术期刊官方网站</p>
        </footer>
    </div>

    <script>
        // 返回顶部功能
        const backToTop = document.getElementById('backToTop');
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        backToTop.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // 暗色模式支持
        function updateColorScheme() {
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.body.classList.toggle('dark-mode', isDark);
        }
        
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateColorScheme);
        updateColorScheme();
        
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>
        """
        
        # 添加当前时间函数到模板上下文
        from datetime import datetime as dt
        data['now'] = dt.now
        
        template = Template(template_str)
        return template.render(**data)
    
    def save_html_file(self, html_content):
        """保存HTML文件"""
        current_date = datetime.now().strftime('%Y%m%d')
        filename = f"daily_report_{current_date}.html"
        filepath = os.path.join(self.config.PATHS['base_dir'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_email_html(self, articles, summary):
        """生成邮件专用的HTML内容（简化版）"""
        current_date = datetime.now().strftime('%Y年%m月%d日')
        start_date, end_date = self.config.get_date_range()
        
        # 按期刊分组文章
        journals = {}
        for article in articles:
            journal_name = article['journal']
            if journal_name not in journals:
                journals[journal_name] = []
            journals[journal_name].append(article)
        
        email_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学术期刊日报 - {{ current_date }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin-bottom: 10px; }
        .summary { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
        .journal { margin-bottom: 20px; border-left: 4px solid #3498db; padding-left: 15px; }
        .journal h3 { color: #2c3e50; margin-bottom: 10px; }
        .article { margin-bottom: 10px; }
        .article a { color: #2980b9; text-decoration: none; }
        .footer { text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>学术期刊日报</h1>
        <p>{{ current_date }} | {{ journals|length }}种期刊，{{ articles|length }}篇文章</p>
    </div>
    
    <div class="summary">
        <h2>今日摘要</h2>
        <p>{{ summary | replace('\\n', '<br>') }}</p>
    </div>
    
    {% for journal_name, journal_articles in journals.items() %}
    <div class="journal">
        <h3>{{ journal_name }} ({{ journal_articles|length }}篇)</h3>
        {% for article in journal_articles %}
        <div class="article">
            • <a href="{{ article.link }}">{{ article.title }}</a>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
    
    <div class="footer">
        <p>生成时间：{{ current_date }} | AutoDLD系统自动生成</p>
    </div>
</body>
</html>
        """
        
        from jinja2 import Template
        template = Template(email_template)
        return template.render(
            current_date=current_date,
            journals=journals,
            articles=articles,
            summary=summary
        )

if __name__ == "__main__":
    # 测试HTML生成器
    generator = HTMLGenerator()
    
    # 模拟测试数据
    test_articles = [
        {
            'title': '测试文章标题1',
            'journal': 'Nature Machine Intelligence',
            'link': 'https://example.com/article1',
            'date': '2024-09-28',
            'abstract': '这是测试文章的摘要'
        },
        {
            'title': '测试文章标题2',
            'journal': 'Medical Image Analysis',
            'link': 'https://example.com/article2',
            'date': '2024-09-27',
            'abstract': ''
        }
    ]
    
    test_summary = "这是测试摘要内容，用于验证HTML生成功能。摘要应该具有整体感，能够提炼出研究趋势和热点话题。"
    
    html_content, filename = generator.generate_daily_report(test_articles, test_summary)
    print(f"HTML文件已生成: {filename}")
    print(f"HTML内容长度: {len(html_content)} 字符")
