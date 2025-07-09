#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 加载环境变量
load_dotenv()

def test_google_sheets():
    print("📊 测试 Google Sheets 连接...")
    
    # 获取配置
    sheets_id = os.getenv('GOOGLE_SHEETS_ID')
    print(f"📋 Sheets ID: {sheets_id}")
    
    if not sheets_id or sheets_id == "your_google_sheets_id":
        print("❌ GOOGLE_SHEETS_ID 未配置或使用默认值")
        print("💡 请在.env文件中设置正确的Google Sheets ID")
        return False
    
    try:
        # 初始化服务
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        print("✅ Google Sheets API 服务初始化成功")
        
        # 测试读取表格基本信息
        print("\n📖 测试读取表格信息...")
        try:
            result = sheet.get(spreadsheetId=sheets_id).execute()
            print(f"✅ 表格标题: {result.get('properties', {}).get('title', '未知')}")
            
            # 列出所有工作表
            sheets_info = result.get('sheets', [])
            print(f"✅ 工作表数量: {len(sheets_info)}")
            for i, sheet_info in enumerate(sheets_info):
                sheet_title = sheet_info.get('properties', {}).get('title', f'Sheet{i+1}')
                print(f"   - {sheet_title}")
            
        except HttpError as e:
            if e.resp.status == 403:
                print("❌ 权限错误 (403): 服务账户没有访问此表格的权限")
                print(f"💡 请将服务账户邮箱添加到表格的编辑权限:")
                with open('credentials.json', 'r') as f:
                    import json
                    data = json.load(f)
                    print(f"   📧 {data.get('client_email')}")
                return False
            elif e.resp.status == 404:
                print("❌ 表格未找到 (404): Google Sheets ID 可能不正确")
                print("💡 请检查.env文件中的GOOGLE_SHEETS_ID是否正确")
                return False
            else:
                print(f"❌ HTTP错误 ({e.resp.status}): {e}")
                return False
        
        # 测试写入权限
        print("\n✏️ 测试写入权限...")
        try:
            # 尝试写入一个测试值
            range_name = 'Sheet1!A1'
            value_input_option = 'RAW'
            values = [['测试连接 - ' + str(datetime.now())[:19]]]
            body = {'values': values}
            
            from datetime import datetime
            
            result = sheet.values().update(
                spreadsheetId=sheets_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            print(f"✅ 写入测试成功，更新了 {result.get('updatedCells', 0)} 个单元格")
            
        except HttpError as e:
            print(f"❌ 写入测试失败: {e}")
            return False
        
        # 测试读取刚才写入的数据
        print("\n📖 测试读取数据...")
        try:
            result = sheet.values().get(
                spreadsheetId=sheets_id,
                range='Sheet1!A1:A1'
            ).execute()
            
            values = result.get('values', [])
            if values:
                print(f"✅ 读取测试成功: {values[0][0]}")
            else:
                print("⚠️ 读取到空数据")
            
        except HttpError as e:
            print(f"❌ 读取测试失败: {e}")
            return False
        
        print("\n🎉 Google Sheets 连接测试全部成功！")
        return True
        
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

if __name__ == "__main__":
    test_google_sheets() 