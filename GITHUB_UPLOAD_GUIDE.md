# GitHub上传指南

## 步骤1：在GitHub上创建新仓库

1. 访问 [GitHub.com](https://github.com) 并登录您的账户
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `AutoDLD`
   - **Description**: `Academic Journal Daily Report System with DLD Focus`
   - **Public** (选择公开)
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

## 步骤2：推送代码到GitHub

在终端中执行以下命令：

```bash
# 进入项目目录
cd /Users/ambrose/Desktop/codelab/AutoDLD

# 设置远程仓库（将YOUR_USERNAME替换为您的GitHub用户名）
git remote add origin https://github.com/Peter-awe/AutoDLD.git

# 推送代码到GitHub
git push -u origin main
```

## 步骤3：验证上传

1. 访问您的GitHub仓库：`https://github.com/Peter-awe/AutoDLD`
2. 确认所有文件都已成功上传
3. 检查README.md文件是否正确显示

## 项目文件说明

已上传的文件包括：

- ✅ `main.py` - 主程序入口
- ✅ `config.py` - 配置文件（已移除敏感信息）
- ✅ `api_crawler.py` - API爬虫模块
- ✅ `summarizer.py` - 摘要生成模块
- ✅ `html_generator.py` - HTML页面生成器
- ✅ `email_sender.py` - 邮件发送模块
- ✅ `scheduler.py` - 定时任务管理
- ✅ `requirements.txt` - 依赖包列表
- ✅ `README.md` - 详细的项目说明文档
- ✅ `.gitignore` - Git忽略文件配置
- ✅ `使用指南.md` - 中文使用指南

## 安全注意事项

**已移除的敏感信息：**
- DeepSeek API密钥
- QQ邮箱地址和授权码
- 具体的用户路径信息

**用户需要自行配置的信息：**
1. 在 `config.py` 中填写您的DeepSeek API密钥
2. 在 `config.py` 中配置您的邮箱信息
3. 根据实际路径调整定时任务设置

## 项目功能

这个AutoDLD系统具有以下功能：

1. **自动爬取** - 通过学术API获取儿童言语障碍DLD相关文章
2. **AI摘要** - 使用DeepSeek生成专业趋势分析
3. **日报生成** - 创建美观的HTML页面
4. **邮件推送** - 自动发送日报到指定邮箱
5. **定时任务** - 每天8点自动执行

## 后续使用

上传到GitHub后，其他人可以通过以下方式使用：

```bash
# 克隆项目
git clone https://github.com/Peter-awe/AutoDLD.git
cd AutoDLD

# 安装依赖
pip install -r requirements.txt

# 配置信息
# 编辑 config.py 文件，填写API密钥和邮箱信息

# 运行系统
python3 main.py
```

## 许可证

本项目采用MIT许可证，允许自由使用和修改。
