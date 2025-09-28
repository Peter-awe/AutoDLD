#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from crontab import CronTab
import logging
from config import Config

class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
        self.cron = CronTab(user=True)
        # 使用相对路径
        self.script_path = 'main.py'
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/scheduler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def add_daily_task(self):
        """添加每日定时任务"""
        try:
            # 检查任务是否已存在
            if self.task_exists():
                self.logger.info("定时任务已存在，无需重复添加")
                return True, "定时任务已存在"
            
            # 创建新的定时任务
            job = self.cron.new(
                command=f'cd {self.config.PATHS["base_dir"]} && python3 {self.script_path} >> {self.config.SCHEDULE_CONFIG["log_file"]} 2>&1'
            )
            
            # 设置执行时间（早上8点）
            job.setall(f'{self.config.SCHEDULE_CONFIG["minute"]} {self.config.SCHEDULE_CONFIG["hour"]} * * *')
            
            # 添加任务描述
            job.set_comment('AutoDLD Daily Report')
            
            # 写入crontab
            self.cron.write()
            
            self.logger.info(f"定时任务添加成功: 每天 {self.config.SCHEDULE_CONFIG['hour']}:{self.config.SCHEDULE_CONFIG['minute']:02d} 执行")
            return True, f"定时任务添加成功: 每天 {self.config.SCHEDULE_CONFIG['hour']}:{self.config.SCHEDULE_CONFIG['minute']:02d} 执行"
            
        except Exception as e:
            self.logger.error(f"添加定时任务失败: {str(e)}")
            return False, f"添加定时任务失败: {str(e)}"
    
    def task_exists(self):
        """检查任务是否已存在"""
        for job in self.cron:
            if job.comment == 'AutoDLD Daily Report':
                return True
        return False
    
    def remove_task(self):
        """移除定时任务"""
        try:
            removed = False
            for job in self.cron:
                if job.comment == 'AutoDLD Daily Report':
                    self.cron.remove(job)
                    removed = True
                    self.logger.info("定时任务已移除")
            
            if removed:
                self.cron.write()
                return True, "定时任务已成功移除"
            else:
                return False, "未找到对应的定时任务"
                
        except Exception as e:
            self.logger.error(f"移除定时任务失败: {str(e)}")
            return False, f"移除定时任务失败: {str(e)}"
    
    def list_tasks(self):
        """列出所有定时任务"""
        tasks = []
        for job in self.cron:
            tasks.append({
                'command': str(job.command),
                'schedule': str(job.slices),
                'comment': job.comment or '无描述'
            })
        return tasks
    
    def get_task_status(self):
        """获取任务状态"""
        exists = self.task_exists()
        if exists:
            for job in self.cron:
                if job.comment == 'AutoDLD Daily Report':
                    return {
                        'exists': True,
                        'schedule': str(job.slices),
                        'command': str(job.command),
                        'enabled': job.is_enabled()
                    }
        else:
            return {
                'exists': False,
                'schedule': f'{self.config.SCHEDULE_CONFIG["minute"]} {self.config.SCHEDULE_CONFIG["hour"]} * * *',
                'command': f'cd {self.config.PATHS["base_dir"]} && python3 {self.script_path}',
                'enabled': False
            }
    
    def enable_task(self):
        """启用定时任务"""
        try:
            for job in self.cron:
                if job.comment == 'AutoDLD Daily Report':
                    job.enable()
                    self.cron.write()
                    self.logger.info("定时任务已启用")
                    return True, "定时任务已启用"
            return False, "未找到对应的定时任务"
        except Exception as e:
            self.logger.error(f"启用定时任务失败: {str(e)}")
            return False, f"启用定时任务失败: {str(e)}"
    
    def disable_task(self):
        """禁用定时任务"""
        try:
            for job in self.cron:
                if job.comment == 'AutoDLD Daily Report':
                    job.enable(False)
                    self.cron.write()
                    self.logger.info("定时任务已禁用")
                    return True, "定时任务已禁用"
            return False, "未找到对应的定时任务"
        except Exception as e:
            self.logger.error(f"禁用定时任务失败: {str(e)}")
            return False, f"禁用定时任务失败: {str(e)}"
    
    def test_schedule(self):
        """测试定时任务设置"""
        try:
            # 创建一个测试任务（立即执行）
            test_job = self.cron.new(
                command=f'cd {self.config.PATHS["base_dir"]} && echo "定时任务测试成功 - $(date)" >> {self.config.PATHS["logs_dir"]}/test_schedule.log'
            )
            test_job.minute.every(1)  # 每分钟执行一次，用于测试
            
            # 立即写入并等待执行
            self.cron.write()
            self.logger.info("测试任务已添加，等待执行...")
            
            # 等待几秒钟让任务执行
            import time
            time.sleep(65)  # 等待超过1分钟
            
            # 检查日志文件
            test_log_path = f'{self.config.PATHS["logs_dir"]}/test_schedule.log'
            if os.path.exists(test_log_path):
                with open(test_log_path, 'r') as f:
                    content = f.read()
                self.logger.info(f"测试任务执行结果: {content}")
                
                # 清理测试任务
                self.cron.remove(test_job)
                self.cron.write()
                os.remove(test_log_path)
                
                return True, "定时任务测试成功"
            else:
                # 清理测试任务
                self.cron.remove(test_job)
                self.cron.write()
                return False, "测试任务未执行，请检查cron服务状态"
                
        except Exception as e:
            self.logger.error(f"定时任务测试失败: {str(e)}")
            return False, f"定时任务测试失败: {str(e)}"

def setup_schedule():
    """设置定时任务（主函数）"""
    scheduler = TaskScheduler()
    
    # 确保日志目录存在
    os.makedirs(scheduler.config.PATHS['logs_dir'], exist_ok=True)
    
    # 添加定时任务
    success, message = scheduler.add_daily_task()
    
    if success:
        print(f"✅ {message}")
        print(f"📅 执行时间: 每天 {scheduler.config.SCHEDULE_CONFIG['hour']}:{scheduler.config.SCHEDULE_CONFIG['minute']:02d}")
        print(f"📁 日志文件: {scheduler.config.SCHEDULE_CONFIG['log_file']}")
        print(f"🔧 脚本路径: {scheduler.script_path}")
    else:
        print(f"❌ {message}")
    
    return success

if __name__ == "__main__":
    # 命令行接口
    import argparse
    
    parser = argparse.ArgumentParser(description='AutoDLD定时任务管理')
    parser.add_argument('action', choices=['add', 'remove', 'status', 'enable', 'disable', 'test'], 
                       help='操作类型')
    
    args = parser.parse_args()
    
    scheduler = TaskScheduler()
    
    if args.action == 'add':
        success, message = scheduler.add_daily_task()
        print(message)
    elif args.action == 'remove':
        success, message = scheduler.remove_task()
        print(message)
    elif args.action == 'status':
        status = scheduler.get_task_status()
        if status['exists']:
            print("✅ 定时任务状态:")
            print(f"   存在: 是")
            print(f"   启用: {'是' if status['enabled'] else '否'}")
            print(f"   时间: {status['schedule']}")
            print(f"   命令: {status['command']}")
        else:
            print("❌ 定时任务不存在")
    elif args.action == 'enable':
        success, message = scheduler.enable_task()
        print(message)
    elif args.action == 'disable':
        success, message = scheduler.disable_task()
        print(message)
    elif args.action == 'test':
        success, message = scheduler.test_schedule()
        print(message)
