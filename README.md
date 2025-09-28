# AutoDLD - 学术期刊日报系统

一个自动化的学术期刊日报系统，能够自动爬取多个顶级学术期刊的最新文章，使用DeepSeek AI生成摘要，并生成美观的HTML日报页面和邮件推送。

## 🌟 功能特性

- **📚 多期刊支持**: 支持10个顶级学术期刊的自动爬取
- **🤖 AI摘要生成**: 使用DeepSeek API生成300-500字的中文摘要
- **🎨 美观界面**: 响应式HTML页面，支持深色/浅色模式
- **📧 邮件推送**: 自动发送HTML格式的日报邮件
- **⏰ 定时任务**: 自动配置cron定时任务，每天8点执行
- **📊 统计分析**: 提供期刊分布和文章统计信息

## 📋 支持的期刊列表

1. **Nature Machine Intelligence**
2. **Medical Image Analysis**
3. **IEEE Journal of Biomedical and Health Informatics**
4. **Artificial Intelligence in Medicine**
5. **Psychiatry Research**
6. **Cell Reports Medicine**
7. **Journal of Speech, Language, and Hearing Research**
8. **Language, Speech, and Hearing Services in Schools**
9. **Developmental Psychology**
10. **International Journal of Language & Communication Disorders**

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/ambrose/Desktop/codelab/AutoDLD
pip install -r requirements.txt
```

### 2. 配置信息

编辑 `config.py` 文件，配置以下信息：

```python
# DeepSeek API配置（请在此处填写您的API密钥）
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE"

# 邮箱配置（请在此处填写您的邮箱信息）
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',  # 或使用其他SMTP服务器
    'smtp_port': 587,
    'sender_email': 'YOUR_EMAIL@example.com',  # 发件人邮箱
    'sender_password': 'YOUR_EMAIL_PASSWORD',  # 邮箱授权码或密码
    'receiver_email': 'YOUR_RECEIVER_EMAIL@example.com'  # 接收邮箱
}
```

### 3. 获取QQ邮箱授权码

1. 登录QQ邮箱网页版
2. 进入"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"POP3/SMTP服务"
5. 按照提示获取授权码

### 4. 测试系统

```bash
# 测试系统功能
python3 main.py --test

# 测试邮箱连接
python3 email_sender.py
```

### 5. 运行日报生成

```bash
# 生成日报（发送邮件并打开浏览器）
python3 main.py

# 生成日报但不发送邮件
python3 main.py --no-email

# 生成日报但不打开浏览器
python3 main.py --no-browser
```

### 6. 设置定时任务

```bash
# 设置每天8点自动执行
python3 main.py --setup-schedule

# 或者使用scheduler.py管理定时任务
python3 scheduler.py add      # 添加任务
python3 scheduler.py status   # 查看状态
python3 scheduler.py remove   # 移除任务
```

## 📁 项目结构

```
AutoDLD/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── requirements.txt     # 依赖包列表
├── README.md           # 项目说明
├── crawler.py          # 网页爬取模块
├── summarizer.py       # 摘要生成模块
├── html_generator.py   # HTML页面生成器
├── email_sender.py     # 邮件发送模块
├── scheduler.py        # 定时任务管理
├── data/               # 数据目录（自动创建）
├── logs/               # 日志目录（自动创建）
└── templates/          # 模板目录（自动创建）
```

## 🔧 命令行参数

### main.py 参数

- `--test`: 运行系统测试
- `--no-email`: 不发送邮件
- `--no-browser`: 不打开浏览器
- `--setup-schedule`: 设置定时任务

### scheduler.py 参数

- `add`: 添加定时任务
- `remove`: 移除定时任务
- `status`: 查看任务状态
- `enable`: 启用任务
- `disable`: 禁用任务
- `test`: 测试定时任务

## 📧 邮件格式

系统会发送包含以下内容的HTML邮件：

- **邮件标题**: `每日新闻导览 - YYYY-MM-DD`
- **邮件内容**:
  - 今日导览摘要（AI生成）
  - 各期刊文章列表
  - 统计信息
  - 生成时间戳

## 🎨 界面特性

生成的HTML页面具有以下特性：

- **响应式设计**: 适配桌面和移动设备
- **深色模式支持**: 自动适配系统主题
- **平滑动画**: 悬停效果和过渡动画
- **目录导航**: 快速跳转到各期刊部分
- **返回顶部**: 便捷的导航功能

## 📊 日志系统

系统会自动生成详细的日志文件：

- `logs/main.log`: 主程序日志
- `logs/crawler.log`: 爬虫日志
- `logs/summarizer.log`: 摘要生成日志
- `logs/html_generator.log`: HTML生成日志
- `logs/email_sender.log`: 邮件发送日志
- `logs/scheduler.log`: 定时任务日志

## 🔒 安全说明

- 所有API密钥和邮箱密码都存储在本地配置文件中
- 系统使用TLS加密发送邮件
- 爬虫设置了合理的请求间隔，避免对目标网站造成压力
- 日志文件不包含敏感信息

## 🐛 故障排除

### 常见问题

1. **邮箱认证失败**
   - 检查QQ邮箱和授权码是否正确
   - 确认已开启SMTP服务

2. **爬取失败**
   - 检查网络连接
   - 目标网站可能更新了页面结构

3. **API调用失败**
   - 检查DeepSeek API密钥是否有效
   - 检查网络连接

4. **定时任务不执行**
   - 检查cron服务是否运行
   - 查看日志文件获取详细信息

### 查看日志

```bash
# 查看最新日志
tail -f /Users/ambrose/Desktop/codelab/AutoDLD/logs/main.log
```

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📞 联系信息

如有问题，请在GitHub项目中提交Issue。

---

**注意**: 请确保遵守各期刊网站的使用条款，合理使用爬虫功能。
