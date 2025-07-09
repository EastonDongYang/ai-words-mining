#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def test_credentials():
    print("🔍 测试 Google Sheets 凭据...")
    
    # 检查文件是否存在
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json 文件不存在")
        return False
    
    try:
        # 测试JSON格式
        with open('credentials.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON格式正确")
        
        # 检查必要字段
        required_fields = ['type', 'project_id', 'client_email', 'private_key']
        for field in required_fields:
            if field not in data:
                print(f"❌ 缺少必要字段: {field}")
                return False
        
        print(f"✅ 服务账户类型: {data.get('type')}")
        print(f"✅ 项目ID: {data.get('project_id')}")
        print(f"✅ 客户端邮箱: {data.get('client_email')}")
        
        # 测试凭据有效性
        print("\n🔐 测试凭据有效性...")
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        
        print("✅ 凭据格式有效")
        
        # 测试网络连接
        print("\n🌐 测试网络连接...")
        request = Request()
        credentials.refresh(request)
        print("✅ 网络连接正常，凭据已刷新")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 凭据测试失败: {e}")
        return False

if __name__ == "__main__":
    test_credentials() 