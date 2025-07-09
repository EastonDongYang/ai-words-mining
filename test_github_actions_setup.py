#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions 设置验证脚本
"""

import os
import json
import sys
from pathlib import Path

def test_local_environment():
    """测试本地环境配置"""
    print("🧪 测试本地环境配置...")
    print("=" * 60)
    
    success = True
    
    # 1. 检查.env文件
    print("1. 📄 检查.env文件...")
    if os.path.exists('.env'):
        print("   ✅ .env文件存在")
        
        # 读取.env文件
        with open('.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        # 检查关键配置
        required_keys = [
            'OPENAI_API_KEY',
            'GOOGLE_SHEETS_ID', 
            'GOOGLE_SHEETS_CREDENTIALS_PATH'
        ]
        
        for key in required_keys:
            if key in env_content and f'{key}=' in env_content:
                value = [line.split('=', 1)[1] for line in env_content.split('\n') if line.startswith(f'{key}=')]
                if value and value[0].strip() and value[0] != f'your_{key.lower()}_here':
                    print(f"   ✅ {key} 已配置")
                else:
                    print(f"   ❌ {key} 未正确配置")
                    success = False
            else:
                print(f"   ❌ {key} 缺失")
                success = False
    else:
        print("   ❌ .env文件不存在")
        success = False
    
    # 2. 检查credentials.json文件
    print("\n2. 🔑 检查credentials.json文件...")
    if os.path.exists('credentials.json'):
        print("   ✅ credentials.json文件存在")
        
        try:
            with open('credentials.json', 'r', encoding='utf-8') as f:
                creds = json.load(f)
            
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            for field in required_fields:
                if field in creds:
                    print(f"   ✅ {field} 字段存在")
                else:
                    print(f"   ❌ {field} 字段缺失")
                    success = False
                    
        except json.JSONDecodeError:
            print("   ❌ credentials.json格式无效")
            success = False
    else:
        print("   ❌ credentials.json文件不存在")
        success = False
    
    # 3. 检查Python依赖
    print("\n3. 🐍 检查Python依赖...")
    required_packages = [
        'openai', 'google-auth', 'google-auth-oauthlib', 
        'google-api-python-client', 'requests', 'beautifulsoup4'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} 已安装")
        except ImportError:
            print(f"   ❌ {package} 未安装")
            success = False
    
    return success

def generate_secrets_template():
    """生成GitHub Secrets模板"""
    print("\n📋 生成GitHub Secrets设置模板...")
    print("=" * 60)
    
    # 读取本地配置
    sheets_id = ""
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('GOOGLE_SHEETS_ID='):
                    sheets_id = line.split('=', 1)[1].strip()
                    break
    
    # 读取credentials.json大小
    creds_size = 0
    if os.path.exists('credentials.json'):
        creds_size = os.path.getsize('credentials.json')
    
    secrets_template = f"""
GitHub Secrets 设置清单：
========================

必需设置的Secrets：

1. OPENAI_API_KEY
   值: sk-xxxxxxxxxxxxxxxxxxxxxxxx
   说明: 你的OpenAI API密钥

2. GOOGLE_SHEETS_ID  
   值: {sheets_id if sheets_id else "1qxIGZ7GltHQ9zBy66lzv0KQ1LhPEnIiBX-hNjnBn6E4"}
   说明: Google Sheets文档ID

3. GOOGLE_SHEETS_CREDENTIALS
   值: [复制整个credentials.json文件内容]
   说明: 大约{creds_size}字节的JSON内容
   注意: 必须复制完整的JSON内容，包括所有花括号

4. GOOGLE_SHEETS_RANGE
   值: Sheet1!A:Z
   说明: 数据范围

5. TARGET_URL
   值: https://theresanaiforthat.com/trending/week/top-50/?pos=1
   说明: 目标网站

可选设置：

6. NOTIFICATION_WEBHOOK_URL
   值: 你的webhook地址 (如Slack、Discord等)

7. NOTIFICATION_EMAIL
   值: 你的邮箱地址

设置步骤：
1. 进入GitHub仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 逐个添加上述secrets
4. 确保名称拼写正确，值复制完整
"""
    
    print(secrets_template)
    
    # 保存到文件
    with open('github_secrets_template.txt', 'w', encoding='utf-8') as f:
        f.write(secrets_template)
    
    print("💾 模板已保存到: github_secrets_template.txt")

def test_github_actions_simulation():
    """模拟GitHub Actions环境测试"""
    print("\n🎭 模拟GitHub Actions环境测试...")
    print("=" * 60)
    
    # 模拟环境变量
    print("设置模拟环境变量...")
    
    # 从.env文件读取配置
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        
        # 检查关键环境变量
        env_vars = [
            'OPENAI_API_KEY',
            'GOOGLE_SHEETS_ID', 
        ]
        
        all_set = True
        for var in env_vars:
            value = os.getenv(var)
            if value and value != f'your_{var.lower()}_here':
                print(f"   ✅ {var}: {'*' * 20}")
            else:
                print(f"   ❌ {var}: 未设置或无效")
                all_set = False
        
        if all_set:
            print("\n🎉 环境变量配置正确！")
            print("💡 你现在可以设置GitHub Actions了")
            return True
        else:
            print("\n❌ 环境变量配置不完整")
            return False
    else:
        print("❌ .env文件不存在")
        return False

def main():
    """主函数"""
    print("🚀 GitHub Actions 设置验证工具")
    print("=" * 60)
    
    try:
        # 1. 测试本地环境
        local_ok = test_local_environment()
        
        # 2. 生成Secrets模板
        generate_secrets_template()
        
        # 3. 模拟测试
        simulation_ok = test_github_actions_simulation()
        
        # 总结
        print("\n" + "=" * 60)
        print("📋 测试总结")
        print("=" * 60)
        
        if local_ok and simulation_ok:
            print("🎉 所有检查都通过了！")
            print("✅ 你现在可以设置GitHub Actions")
            print("📋 请参考 github_secrets_template.txt 设置Secrets")
            print("📖 详细指南请查看 github_actions_debug_guide.md")
            return True
        else:
            print("❌ 检查发现问题")
            if not local_ok:
                print("   - 本地环境配置不完整")
            if not simulation_ok:
                print("   - 环境变量配置有问题")
            print("🔧 请修复问题后重新运行此脚本")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 