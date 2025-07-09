#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request

load_dotenv()

def test_sheets_with_http():
    print("📊 使用HTTP请求测试Google Sheets...")
    
    sheets_id = os.getenv('GOOGLE_SHEETS_ID')
    print(f"📋 Sheets ID: {sheets_id}")
    
    try:
        # 加载凭据并获取访问令牌
        print("\n🔐 获取访问令牌...")
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        
        # 刷新令牌
        request = Request()
        credentials.refresh(request)
        access_token = credentials.token
        print("✅ 访问令牌获取成功")
        
        # 设置请求头
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # 测试读取表格信息
        print("\n📖 测试读取表格信息...")
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheets_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 表格标题: {data.get('properties', {}).get('title', '未知')}")
                
                sheets_info = data.get('sheets', [])
                print(f"✅ 工作表数量: {len(sheets_info)}")
                for sheet_info in sheets_info:
                    sheet_title = sheet_info.get('properties', {}).get('title', 'Unknown')
                    print(f"   - {sheet_title}")
                    
            elif response.status_code == 403:
                print("❌ 权限错误 (403): 服务账户没有访问此表格的权限")
                print("💡 请将以下邮箱添加到Google Sheets的编辑权限:")
                with open('credentials.json', 'r') as f:
                    cred_data = json.load(f)
                    print(f"   📧 {cred_data.get('client_email')}")
                return False
                
            elif response.status_code == 404:
                print("❌ 表格未找到 (404): Google Sheets ID可能不正确")
                return False
                
            else:
                print(f"❌ 未知错误 ({response.status_code}): {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时 - 网络连接问题")
            return False
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
        
        # 测试写入数据
        print("\n✏️ 测试写入数据...")
        write_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheets_id}/values/Sheet1!A1"
        
        from datetime import datetime
        test_data = {
            "values": [["测试连接 - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
        }
        
        try:
            response = requests.put(
                f"{write_url}?valueInputOption=RAW",
                headers=headers,
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 写入成功，更新了 {result.get('updatedCells', 0)} 个单元格")
            else:
                print(f"❌ 写入失败 ({response.status_code}): {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 写入测试失败: {e}")
            return False
        
        # 测试读取数据
        print("\n📖 测试读取数据...")
        read_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheets_id}/values/Sheet1!A1:A1"
        
        try:
            response = requests.get(read_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                values = data.get('values', [])
                if values and values[0]:
                    print(f"✅ 读取成功: {values[0][0]}")
                else:
                    print("⚠️ 读取到空数据")
            else:
                print(f"❌ 读取失败 ({response.status_code}): {response.text}")
                
        except Exception as e:
            print(f"❌ 读取测试失败: {e}")
        
        print("\n🎉 HTTP方式的Google Sheets测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_sheets_with_http() 