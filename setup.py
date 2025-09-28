#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import getpass
from config import Config

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version}")

def install_dependencies():
    """安装依赖包"""
    print("\n📦 正在安装依赖包...")
    
    try:
        # 安装requirements.txt中的包
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ 依赖包安装成功")
        else:
            print("❌ 依赖包安装失败")
            print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装依赖包时出错: {str(e)}")
        return False
    
    return True

def configure_email():
    """配置邮箱信息"""
    print("\n📧 配置邮箱信息")
    
    config = Config()
    
    # 获取用户输入
    sender_email = input("请输入发件人QQ邮箱: ").strip()
    if not sender_email:
        print("❌ 邮箱地址不能为空")
        return False
    
    sender_password = getpass.getpass("请输入QQ邮箱授权码: ").strip()
    if not sender_password:
        print("❌ 授权码不能为空")
        return False
    
    # 更新配置文件
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换邮箱配置
        new_content = content.replace(
            "'sender_email': '',  # 需要填写发件人QQ邮箱",
            f"'sender_email': '{sender_email}',  # 发件人QQ邮箱"
        ).replace(
            "'sender_password': '',  # 需要填写QQ邮箱授权码",
            f"'sender_password': '{sender_password}',  # QQ邮箱授权码"
        )
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ 邮箱配置已更新")
        return True
        
    except Exception as e:
        print(f"❌ 更新配置文件失败: {str(e)}")
        return False

def test_email_connection():
    """测试邮箱连接"""
    print("\n🔗 测试邮箱连接...")
    
    try:
        from email_sender import EmailSender
        sender = EmailSender()
        success, message = sender.test_email_connection()
        
        if success:
            print("✅ 邮箱连接测试成功")
            return True
        else:
            print(f"❌ 邮箱连接测试失败: {message}")
            return False
            
    except Exception as e:
        print(f"❌ 邮箱连接测试出错: {str(e)}")
        return False

def test_system():
    """测试系统功能"""
    print("\n🧪 测试系统功能...")
    
    try:
        from main import AutoDLD
        system = AutoDLD()
        success = system.test_system()
        
        if success:
            print("✅ 系统功能测试通过")
            return True
        else:
            print("❌ 系统功能测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 系统测试出错: {str(e)}")
        return False

def setup_schedule():
    """设置定时任务"""
    print("\n⏰ 设置定时任务...")
    
    try:
        from scheduler import setup_schedule
        success = setup_schedule()
        
        if success:
            print("✅ 定时任务设置成功")
            return True
        else:
            print("❌ 定时任务设置失败")
            return False
            
    except Exception as e:
        print(f"❌ 定时任务设置出错: {str(e)}")
        return False

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建项目目录...")
    
    config = Config()
    directories = [
        config.PATHS['data_dir'],
        config.PATHS['logs_dir'],
        config.PATHS['templates_dir']
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
        except Exception as e:
            print(f"❌ 创建目录失败 {directory}: {str(e)}")
            return False
    
    return True

def main():
    """主安装函数"""
    print("=" * 60)
    print("🚀 AutoDLD 学术期刊日报系统 - 安装向导")
    print("=" * 60)
    
    # 检查当前目录
    current_dir = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(current_dir, 'config.py')):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    steps = [
        ("检查Python版本", check_python_version),
        ("创建项目目录", create_directories),
        ("安装依赖包", install_dependencies),
        ("配置邮箱信息", configure_email),
        ("测试邮箱连接", test_email_connection),
        ("测试系统功能", test_system),
        ("设置定时任务", setup_schedule)
    ]
    
    for step_name, step_function in steps:
        print(f"\n📋 步骤 {steps.index((step_name, step_function)) + 1}: {step_name}")
        if not step_function():
            print(f"\n❌ 安装过程在 '{step_name}' 步骤失败")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    print("\n📋 下一步操作:")
    print("1. 手动运行日报生成:")
    print("   python3 main.py")
    print("\n2. 查看生成的HTML文件")
    print("3. 检查邮箱是否收到测试邮件")
    print("\n📖 详细使用说明请参考 README.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
