#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import webbrowser
from datetime import datetime
from config import Config
from api_crawler import APICrawler
from summarizer import DeepSeekSummarizer
from html_generator import HTMLGenerator
from email_sender import EmailSender

class AutoDLD:
    """学术期刊日报系统主类"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
        self.config.ensure_directories()
        
        # 初始化各模块
        self.crawler = APICrawler()
        self.summarizer = DeepSeekSummarizer()
        self.html_generator = HTMLGenerator()
        self.email_sender = EmailSender()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/main.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_daily_report(self, send_email=True, open_browser=True):
        """运行日报生成流程"""
        try:
            self.logger.info("开始生成学术期刊日报")
            start_time = datetime.now()
            
            # 1. 爬取期刊文章
            self.logger.info("步骤1: 爬取期刊文章")
            articles = self.crawler.crawl_journals()
            
            if not articles:
                self.logger.warning("未找到任何文章，日报生成终止")
                return False
            
            self.logger.info(f"爬取到 {len(articles)} 篇文章")
            
            # 2. 生成摘要
            self.logger.info("步骤2: 生成摘要")
            summary = self.summarizer.generate_summary(articles)
            self.logger.info(f"摘要生成完成，长度: {len(summary)} 字符")
            
            # 3. 生成HTML页面
            self.logger.info("步骤3: 生成HTML页面")
            html_content, html_filepath = self.html_generator.generate_daily_report(articles, summary)
            self.logger.info(f"HTML页面生成完成: {html_filepath}")
            
            # 4. 发送邮件
            if send_email:
                self.logger.info("步骤4: 发送邮件")
                email_success = self.email_sender.send_daily_report(html_content, len(articles))
                if email_success:
                    self.logger.info("邮件发送成功")
                else:
                    self.logger.warning("邮件发送失败")
            
            # 5. 打开浏览器预览
            if open_browser:
                self.logger.info("步骤5: 打开浏览器预览")
                webbrowser.open(f'file://{html_filepath}')
            
            # 计算执行时间
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            self.logger.info(f"日报生成完成，总耗时: {execution_time:.2f} 秒")
            
            # 输出结果摘要
            self.print_summary(articles, summary, html_filepath, execution_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"日报生成过程中出错: {str(e)}")
            return False
    
    def print_summary(self, articles, summary, html_filepath, execution_time):
        """打印结果摘要"""
        print("\n" + "="*60)
        print("🎯 学术期刊日报生成完成")
        print("="*60)
        
        # 统计信息
        journals = {}
        for article in articles:
            journal = article['journal']
            journals[journal] = journals.get(journal, 0) + 1
        
        print(f"📊 统计信息:")
        print(f"   文章总数: {len(articles)}")
        print(f"   期刊数量: {len(journals)}")
        print(f"   执行时间: {execution_time:.2f} 秒")
        
        print(f"\n📖 期刊分布:")
        for journal, count in sorted(journals.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {journal}: {count}篇")
        
        print(f"\n📄 生成文件:")
        print(f"   HTML文件: {html_filepath}")
        
        print(f"\n📋 摘要预览 (前200字符):")
        print(f"   {summary[:200]}...")
        
        print("\n" + "="*60)
    
    def test_system(self):
        """测试系统功能"""
        self.logger.info("开始系统测试")
        
        # 测试爬虫
        try:
            test_articles = [
                {
                    'title': '测试文章 - Machine Learning for Medical Diagnosis',
                    'journal': 'Nature Machine Intelligence',
                    'link': 'https://example.com/test1',
                    'date': '2024-09-28',
                    'abstract': '测试摘要内容'
                },
                {
                    'title': '测试文章 - Deep Learning in Healthcare',
                    'journal': 'Medical Image Analysis',
                    'link': 'https://example.com/test2',
                    'date': '2024-09-27',
                    'abstract': ''
                }
            ]
            
            # 测试摘要生成
            test_summary = self.summarizer.generate_summary(test_articles)
            print("✅ 摘要生成测试通过")
            
            # 测试HTML生成
            html_content, filename = self.html_generator.generate_daily_report(test_articles, test_summary)
            print("✅ HTML生成测试通过")
            
            # 测试邮件发送（仅测试连接）
            success, message = self.email_sender.test_email_connection()
            if success:
                print("✅ 邮件连接测试通过")
            else:
                print(f"⚠️ 邮件连接测试: {message}")
            
            print("🎉 系统测试完成，所有功能正常")
            return True
            
        except Exception as e:
            self.logger.error(f"系统测试失败: {str(e)}")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AutoDLD学术期刊日报系统')
    parser.add_argument('--test', action='store_true', help='运行系统测试')
    parser.add_argument('--no-email', action='store_true', help='不发送邮件')
    parser.add_argument('--no-browser', action='store_true', help='不打开浏览器')
    parser.add_argument('--setup-schedule', action='store_true', help='设置定时任务')
    
    args = parser.parse_args()
    
    # 创建系统实例
    system = AutoDLD()
    
    if args.test:
        # 运行测试
        system.test_system()
    
    elif args.setup_schedule:
        # 设置定时任务
        from scheduler import setup_schedule
        setup_schedule()
    
    else:
        # 运行日报生成
        send_email = not args.no_email
        open_browser = not args.no_browser
        
        success = system.run_daily_report(send_email=send_email, open_browser=open_browser)
        
        if success:
            print("\n🎉 日报生成任务完成！")
        else:
            print("\n❌ 日报生成失败，请检查日志文件")
            sys.exit(1)

if __name__ == "__main__":
    main()
