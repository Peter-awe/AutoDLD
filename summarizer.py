#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
from config import Config

class DeepSeekSummarizer:
    """使用DeepSeek API生成摘要"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/summarizer.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_summary(self, articles):
        """为文章列表生成整体摘要"""
        if not articles:
            return "今日未发现新的学术文章更新。"
        
        # 准备输入文本
        input_text = self.prepare_input_text(articles)
        
        try:
            # 调用DeepSeek API
            summary = self.call_deepseek_api(input_text)
            self.logger.info("摘要生成成功")
            return summary
            
        except Exception as e:
            self.logger.error(f"摘要生成失败: {str(e)}")
            # 如果API调用失败，生成一个简单的摘要
            return self.generate_fallback_summary(articles)
    
    def prepare_input_text(self, articles):
        """准备输入文本"""
        # 按期刊分组文章
        journals = {}
        for article in articles:
            journal_name = article['journal']
            if journal_name not in journals:
                journals[journal_name] = []
            journals[journal_name].append(article)
        
        # 构建输入文本
        input_text = "以下是过去7天内各学术期刊的最新文章标题列表：\n\n"
        
        for journal_name, journal_articles in journals.items():
            input_text += f"【{journal_name}】期刊：\n"
            for i, article in enumerate(journal_articles, 1):
                input_text += f"{i}. {article['title']}\n"
            input_text += "\n"
        
        input_text += """
请根据以上文章标题，生成一段300-500字的中文摘要，要求：
1. 摘要应具有整体感，能够提炼出当日新闻的主要趋势、关注焦点或舆论动向
2. 不要机械复述标题，要进行概括与串联，风格自然流畅
3. 分析各期刊的关注重点和研究方向
4. 指出可能的研究趋势和热点话题
5. 语言简洁明了，逻辑清晰

请直接输出摘要内容，不要包含任何额外的说明或格式标记。
"""
        
        return input_text
    
    def call_deepseek_api(self, input_text):
        """调用DeepSeek API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.DEEPSEEK_API_KEY}'
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的学术期刊分析助手，擅长从多个学术期刊的文章标题中提炼研究趋势和热点话题。"
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ],
            "temperature": self.config.SUMMARY_CONFIG['temperature'],
            "max_tokens": self.config.SUMMARY_CONFIG['max_length'],
            "stream": False
        }
        
        response = requests.post(
            self.config.DEEPSEEK_API_URL,
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        summary = result['choices'][0]['message']['content'].strip()
        
        # 确保摘要长度在要求范围内
        summary = self.adjust_summary_length(summary)
        
        return summary
    
    def adjust_summary_length(self, summary):
        """调整摘要长度"""
        # 计算中文字符数
        chinese_chars = len([c for c in summary if '\u4e00' <= c <= '\u9fff'])
        
        min_chars = self.config.SUMMARY_CONFIG['min_length']
        max_chars = self.config.SUMMARY_CONFIG['max_length']
        
        if chinese_chars < min_chars:
            # 如果太短，添加一些总结性语句
            summary += "\n\n总体来看，这些研究反映了当前学术界的多元化发展趋势，涵盖了从基础理论到应用实践的多个层面。"
        elif chinese_chars > max_chars:
            # 如果太长，截断到合适长度
            summary = summary[:max_chars] + "..."
        
        return summary
    
    def generate_fallback_summary(self, articles):
        """API调用失败时的备用摘要生成"""
        self.logger.info("使用备用摘要生成方法")
        
        # 按期刊统计文章数量
        journal_stats = {}
        for article in articles:
            journal = article['journal']
            journal_stats[journal] = journal_stats.get(journal, 0) + 1
        
        # 生成简单的统计摘要
        summary = "过去7天内，各学术期刊的研究动态如下：\n\n"
        
        # 添加期刊统计
        for journal, count in journal_stats.items():
            summary += f"• {journal}: {count}篇新文章\n"
        
        summary += "\n研究热点主要集中在：\n"
        
        # 分析关键词（简单的关键词提取）
        keywords = self.extract_keywords(articles)
        for keyword in keywords[:5]:  # 取前5个关键词
            summary += f"• {keyword}\n"
        
        summary += "\n这些研究反映了当前学术界的活跃态势，涵盖了多个前沿领域。"
        
        return summary
    
    def extract_keywords(self, articles):
        """从文章标题中提取关键词"""
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from'}
        keywords = {}
        
        for article in articles:
            title = article['title'].lower()
            # 简单的分词和关键词提取
            words = title.split()
            for word in words:
                # 过滤常见词和短词
                if (len(word) > 3 and 
                    word not in common_words and 
                    word.isalpha()):
                    keywords[word] = keywords.get(word, 0) + 1
        
        # 按频率排序
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, count in sorted_keywords[:10]]  # 返回前10个关键词
    
    def summarize_individual_articles(self, articles):
        """为每篇文章生成简短摘要（可选功能）"""
        individual_summaries = []
        
        for article in articles:
            try:
                # 为单篇文章生成简短摘要
                prompt = f"请为以下学术文章标题生成一个50字左右的简短摘要：\n\n标题：{article['title']}\n\n期刊：{article['journal']}\n\n摘要："
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.config.DEEPSEEK_API_KEY}'
                }
                
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 100,
                    "stream": False
                }
                
                response = requests.post(
                    self.config.DEEPSEEK_API_URL,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                response.raise_for_status()
                
                result = response.json()
                summary = result['choices'][0]['message']['content'].strip()
                
                individual_summaries.append({
                    'title': article['title'],
                    'journal': article['journal'],
                    'link': article['link'],
                    'summary': summary
                })
                
            except Exception as e:
                self.logger.warning(f"为单篇文章生成摘要失败: {str(e)}")
                # 如果失败，使用标题作为摘要
                individual_summaries.append({
                    'title': article['title'],
                    'journal': article['journal'],
                    'link': article['link'],
                    'summary': article['title']
                })
        
        return individual_summaries

if __name__ == "__main__":
    # 测试摘要生成器
    summarizer = DeepSeekSummarizer()
    
    # 模拟测试数据
    test_articles = [
        {
            'title': 'Machine Learning Approaches for Early Detection of Language Disorders in Children',
            'journal': 'Nature Machine Intelligence',
            'link': 'https://example.com/article1',
            'date': '2024-09-28'
        },
        {
            'title': 'Deep Learning-based Medical Image Analysis for Brain Tumor Segmentation',
            'journal': 'Medical Image Analysis',
            'link': 'https://example.com/article2',
            'date': '2024-09-27'
        }
    ]
    
    summary = summarizer.generate_summary(test_articles)
    print("生成的摘要：")
    print(summary)
    print(f"摘要长度：{len(summary)} 字符")
