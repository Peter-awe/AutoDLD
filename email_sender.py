#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config

class EmailSender:
    """邮件发送器"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/email_sender.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_daily_report(self, html_content, articles_count):
        """发送日报邮件"""
        try:
            # 检查邮箱配置是否完整
            if not self.validate_email_config():
                self.logger.error("邮箱配置不完整，无法发送邮件")
                return False
            
            # 创建邮件内容
            msg = self.create_email_message(html_content, articles_count)
            
            # 发送邮件
            success = self.send_email(msg)
            
            if success:
                self.logger.info("日报邮件发送成功")
            else:
                self.logger.error("日报邮件发送失败")
            
            return success
            
        except Exception as e:
            self.logger.error(f"发送日报邮件时出错: {str(e)}")
            return False
    
    def validate_email_config(self):
        """验证邮箱配置"""
        config = self.config.EMAIL_CONFIG
        required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password', 'receiver_email']
        
        for field in required_fields:
            if not config.get(field):
                self.logger.error(f"邮箱配置缺少字段: {field}")
                return False
        
        return True
    
    def create_email_message(self, html_content, articles_count):
        """创建邮件消息"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        email_config = self.config.EMAIL_CONFIG
        
        # 创建多部分消息
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'每日新闻导览 - {current_date}'
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['receiver_email']
        
        # 创建纯文本版本（备用）
        text_content = f"""
学术期刊日报 - {current_date}

今日共收录 {articles_count} 篇文章，涵盖多个学术期刊的最新研究动态。

详细内容请查看HTML版本邮件。

--
AutoDLD系统自动生成
        """
        
        # 创建HTML版本
        html_content_with_wrapper = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                       "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .header .date {{
            margin-top: 10px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .summary-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }}
        .summary-section h2 {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 18px;
        }}
        .stats {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
            color: #2c3e50;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
            font-size: 12px;
            border-top: 1px solid #e0e0e0;
        }}
        .article-list {{
            margin-top: 20px;
        }}
        .article-item {{
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .article-item:last-child {{
            border-bottom: none;
        }}
        .article-title {{
            font-weight: 500;
            margin-bottom: 5px;
        }}
        .article-title a {{
            color: #2980b9;
            text-decoration: none;
        }}
        .article-meta {{
            font-size: 12px;
            color: #7f8c8d;
        }}
        @media (max-width: 480px) {{
            .content {{
                padding: 15px;
            }}
            .header {{
                padding: 20px;
            }}
            .header h1 {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 学术期刊日报</h1>
            <div class="date">{current_date}</div>
        </div>
        
        <div class="content">
            <div class="stats">
                📊 今日收录 {articles_count} 篇文章 | ⏰ 生成时间: {datetime.now().strftime('%H:%M:%S')}
            </div>
            
            {html_content}
            
            <div class="footer">
                <p>本日报由 AutoDLD 系统自动生成</p>
                <p>数据来源于各学术期刊官方网站</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        # 添加文本和HTML部分
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content_with_wrapper, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def send_email(self, msg):
        """发送邮件"""
        email_config = self.config.EMAIL_CONFIG
        
        try:
            # 创建SMTP连接
            if email_config['smtp_server'] == 'smtp.qq.com':
                # QQ邮箱需要TLS
                server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
                server.starttls()  # 启用TLS加密
            else:
                # 其他邮箱服务器
                server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            
            # 登录邮箱
            server.login(email_config['sender_email'], email_config['sender_password'])
            
            # 发送邮件
            server.send_message(msg)
            
            # 关闭连接
            server.quit()
            
            self.logger.info("邮件发送成功")
            return True
            
        except smtplib.SMTPAuthenticationError:
            self.logger.error("邮箱认证失败，请检查邮箱地址和授权码")
            return False
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP错误: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"发送邮件时发生未知错误: {str(e)}")
            return False
    
    def test_email_connection(self):
        """测试邮箱连接"""
        if not self.validate_email_config():
            return False, "邮箱配置不完整"
        
        email_config = self.config.EMAIL_CONFIG
        
        try:
            # 测试连接
            if email_config['smtp_server'] == 'smtp.qq.com':
                server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
                server.starttls()
            else:
                server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            
            # 测试登录
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.quit()
            
            return True, "邮箱连接测试成功"
            
        except smtplib.SMTPAuthenticationError:
            return False, "邮箱认证失败，请检查邮箱地址和授权码"
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"
    
    def send_test_email(self):
        """发送测试邮件"""
        test_html = """
        <div class="summary-section">
            <h2>🎯 测试邮件</h2>
            <p>这是一封测试邮件，用于验证邮件发送功能是否正常工作。</p>
            <p>如果收到此邮件，说明AutoDLD系统的邮件发送功能配置正确。</p>
        </div>
        """
        
        success = self.send_daily_report(test_html, 0)
        
        if success:
            return "测试邮件发送成功"
        else:
            return "测试邮件发送失败"

if __name__ == "__main__":
    # 测试邮件发送器
    sender = EmailSender()
    
    # 测试邮箱连接
    success, message = sender.test_email_connection()
    print(f"邮箱连接测试: {message}")
    
    if success:
        # 发送测试邮件
        result = sender.send_test_email()
        print(f"测试邮件发送: {result}")
    else:
        print("请先配置正确的邮箱信息")
        print("需要在 config.py 中配置以下信息：")
        print("- sender_email: 发件人QQ邮箱")
        print("- sender_password: QQ邮箱授权码")
