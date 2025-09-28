# AutoDLD - Academic Journal Daily Report System

An automated academic journal daily report system that automatically crawls the latest articles from multiple top-tier academic journals, uses DeepSeek AI to generate summaries, and creates beautiful HTML daily reports with email notifications.

## 🌟 Features

- **📚 Multi-Journal Support**: Automatic crawling of 10 top academic journals
- **🤖 AI Summary Generation**: Uses DeepSeek API to generate 300-500 word Chinese summaries
- **🎨 Beautiful Interface**: Responsive HTML pages with dark/light mode support
- **📧 Email Delivery**: Automatic HTML-formatted daily report emails
- **⏰ Scheduled Tasks**: Automatic cron job configuration, runs daily at 8:00 AM
- **📊 Statistical Analysis**: Provides journal distribution and article statistics

## 📋 Supported Journals

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

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd AutoDLD
pip install -r requirements.txt
```

### 2. Configuration

Edit the `config.py` file with your information:

```python
# DeepSeek API Configuration (Enter your API key here)
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE"

# Email Configuration (Enter your email information here)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',  # or use other SMTP servers
    'smtp_port': 587,
    'sender_email': 'YOUR_EMAIL@example.com',  # sender email
    'sender_password': 'YOUR_EMAIL_PASSWORD',  # email authorization code or password
    'receiver_email': 'YOUR_RECEIVER_EMAIL@example.com'  # receiver email
}
```

### 3. Get QQ Email Authorization Code (if using QQ Mail)

1. Log in to QQ Mail web version
2. Go to "Settings" → "Account"
3. Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service"
4. Enable "POP3/SMTP Service"
5. Follow instructions to get authorization code

### 4. Test the System

```bash
# Test system functionality
python3 main.py --test

# Test email connection
python3 email_sender.py
```

### 5. Generate Daily Report

```bash
# Generate report (send email and open browser)
python3 main.py

# Generate report without sending email
python3 main.py --no-email

# Generate report without opening browser
python3 main.py --no-browser
```

### 6. Set Up Scheduled Tasks

```bash
# Set up daily execution at 8:00 AM
python3 main.py --setup-schedule

# Or use scheduler.py to manage scheduled tasks
python3 scheduler.py add      # Add task
python3 scheduler.py status   # Check status
python3 scheduler.py remove   # Remove task
```

## 📁 Project Structure

```
AutoDLD/
├── main.py              # Main program entry
├── config.py            # Configuration file
├── requirements.txt     # Dependencies list
├── README.md           # Project documentation
├── crawler.py          # Web crawling module
├── summarizer.py       # Summary generation module
├── html_generator.py   # HTML page generator
├── email_sender.py     # Email sending module
├── scheduler.py        # Scheduled task management
├── data/               # Data directory (auto-created)
├── logs/               # Logs directory (auto-created)
└── templates/          # Templates directory (auto-created)
```

## 🔧 Command Line Arguments

### main.py Arguments

- `--test`: Run system tests
- `--no-email`: Don't send email
- `--no-browser`: Don't open browser
- `--setup-schedule`: Set up scheduled tasks

### scheduler.py Arguments

- `add`: Add scheduled task
- `remove`: Remove scheduled task
- `status`: Check task status
- `enable`: Enable task
- `disable`: Disable task
- `test`: Test scheduled task

## 📧 Email Format

The system sends HTML emails containing:

- **Email Subject**: `Daily News Digest - YYYY-MM-DD`
- **Email Content**:
  - Today's overview summary (AI-generated)
  - Article lists from each journal
  - Statistical information
  - Generation timestamp

## 🎨 Interface Features

Generated HTML pages include:

- **Responsive Design**: Adapts to desktop and mobile devices
- **Dark Mode Support**: Automatically adapts to system theme
- **Smooth Animations**: Hover effects and transition animations
- **Table of Contents**: Quick navigation to journal sections
- **Back to Top**: Convenient navigation feature

## 📊 Logging System

The system automatically generates detailed log files:

- `logs/main.log`: Main program logs
- `logs/crawler.log`: Crawler logs
- `logs/summarizer.log`: Summary generation logs
- `logs/html_generator.log`: HTML generation logs
- `logs/email_sender.log`: Email sending logs
- `logs/scheduler.log`: Scheduled task logs

## 🔒 Security Notes

- All API keys and email passwords are stored in local configuration files
- System uses TLS encryption for email sending
- Crawler has reasonable request intervals to avoid overloading target websites
- Log files do not contain sensitive information

## 🐛 Troubleshooting

### Common Issues

1. **Email Authentication Failed**
   - Check if QQ email and authorization code are correct
   - Confirm SMTP service is enabled

2. **Crawling Failed**
   - Check network connection
   - Target website may have updated page structure

3. **API Call Failed**
   - Check if DeepSeek API key is valid
   - Check network connection

4. **Scheduled Task Not Executing**
   - Check if cron service is running
   - Check log files for detailed information

### View Logs

```bash
# View latest logs
tail -f logs/main.log
```

## 📄 License

This project is for learning and research purposes only.

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project.

## 📞 Contact Information

If you have questions, please submit an Issue in the GitHub project.

---

**Note**: Please ensure compliance with the terms of use of each journal website and use crawling functionality responsibly.
