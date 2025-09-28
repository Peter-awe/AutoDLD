#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta

class Config:
    """配置文件"""
    
    # DeepSeek API配置（请在此处填写您的API密钥）
    DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE"
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    # 邮箱配置（请在此处填写您的邮箱信息）
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.qq.com',  # 或使用其他SMTP服务器
        'smtp_port': 587,
        'sender_email': 'YOUR_EMAIL@example.com',  # 发件人邮箱
        'sender_password': 'YOUR_EMAIL_PASSWORD',  # 邮箱授权码或密码
        'receiver_email': 'YOUR_RECEIVER_EMAIL@example.com'  # 接收邮箱
    }
    
    # 期刊网站列表
    JOURNAL_URLS = [
        {
            'name': 'Nature Machine Intelligence',
            'url': 'https://www.nature.com/natmachintell/',
            'type': 'nature'
        },
        {
            'name': 'Medical Image Analysis',
            'url': 'https://www.sciencedirect.com/journal/medical-image-analysis',
            'type': 'sciencedirect'
        },
        {
            'name': 'IEEE Journal of Biomedical and Health Informatics',
            'url': 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=6260354',
            'type': 'ieee'
        },
        {
            'name': 'Artificial Intelligence in Medicine',
            'url': 'https://www.sciencedirect.com/journal/artificial-intelligence-in-medicine',
            'type': 'sciencedirect'
        },
        {
            'name': 'Psychiatry Research',
            'url': 'https://www.sciencedirect.com/journal/psychiatry-research',
            'type': 'sciencedirect'
        },
        {
            'name': 'Cell Reports Medicine',
            'url': 'https://www.cell.com/cell-reports-medicine',
            'type': 'cell'
        },
        {
            'name': 'Journal of Speech, Language, and Hearing Research',
            'url': 'https://academy.pubs.asha.org/journal/jslhr',
            'type': 'asha'
        },
        {
            'name': 'Language, Speech, and Hearing Services in Schools',
            'url': 'https://academy.pubs.asha.org/journal/lshss',
            'type': 'asha'
        },
        {
            'name': 'Developmental Psychology',
            'url': 'https://www.apa.org/pubs/journals/dev',
            'type': 'apa'
        },
        {
            'name': 'International Journal of Language & Communication Disorders',
            'url': 'https://onlinelibrary.wiley.com/journal/14606984',
            'type': 'wiley'
        }
    ]
    
    # 爬取配置
    CRAWL_CONFIG = {
        'days_back': 7,  # 爬取过去7天的文章
        'timeout': 30,   # 请求超时时间（秒）
        'delay': 2,      # 请求间隔延迟（秒）
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 摘要生成配置
    SUMMARY_CONFIG = {
        'max_length': 500,  # 摘要最大长度
        'min_length': 300,  # 摘要最小长度
        'temperature': 0.7  # 生成温度
    }
    
    # 定时任务配置
    SCHEDULE_CONFIG = {
        'hour': 8,        # 早上8点执行
        'minute': 0,      # 0分钟
        'log_file': 'logs/scheduler.log'
    }
    
    # 文件路径配置（相对于项目根目录）
    PATHS = {
        'base_dir': '.',
        'templates_dir': 'templates',
        'data_dir': 'data',
        'logs_dir': 'logs'
    }
    
    @classmethod
    def get_date_range(cls):
        """获取过去7天的日期范围"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=cls.CRAWL_CONFIG['days_back'])
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        for path in cls.PATHS.values():
            if path.endswith(('templates', 'data', 'logs')):
                os.makedirs(path, exist_ok=True)
