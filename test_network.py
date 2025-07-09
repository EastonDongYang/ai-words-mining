#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import socket
import time

def test_network_connectivity():
    print("🌐 测试网络连接...")
    
    # 测试基本网络连接
    print("\n1. 🌍 测试基本网络连接...")
    try:
        response = requests.get('https://www.google.com', timeout=10)
        if response.status_code == 200:
            print("✅ 基本网络连接正常")
        else:
            print(f"⚠️ 网络连接异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 基本网络连接失败: {e}")
        return False
    
    # 测试Google API域名解析
    print("\n2. 🔍 测试Google API域名解析...")
    google_apis = [
        'sheets.googleapis.com',
        'www.googleapis.com',
        'oauth2.googleapis.com'
    ]
    
    for api in google_apis:
        try:
            ip = socket.gethostbyname(api)
            print(f"✅ {api} -> {ip}")
        except Exception as e:
            print(f"❌ {api} 解析失败: {e}")
    
    # 测试Google API HTTP连接
    print("\n3. 🔗 测试Google API HTTP连接...")
    api_endpoints = [
        'https://sheets.googleapis.com/$discovery/rest?version=v4',
        'https://www.googleapis.com/oauth2/v1/certs',
        'https://oauth2.googleapis.com/token'
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"测试: {endpoint}")
            response = requests.get(endpoint, timeout=15)
            if response.status_code in [200, 401, 403]:  # 200=成功, 401/403=需要认证但连接正常
                print(f"✅ 连接成功 (状态: {response.status_code})")
            else:
                print(f"⚠️ 连接异常 (状态: {response.status_code})")
        except requests.exceptions.Timeout:
            print(f"❌ 连接超时 - 可能被防火墙阻止")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ 连接错误: {e}")
        except Exception as e:
            print(f"❌ 其他错误: {e}")
        time.sleep(1)  # 避免请求过快
    
    # 检测代理设置
    print("\n4. 🛡️ 检查代理设置...")
    import os
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    proxy_found = False
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"📡 发现代理设置: {var} = {value}")
            proxy_found = True
    
    if not proxy_found:
        print("✅ 未检测到代理设置")
    
    # 测试简化的Google Sheets API连接
    print("\n5. 📊 测试简化的Google Sheets API连接...")
    try:
        # 不使用认证，只测试连接
        url = "https://sheets.googleapis.com/v4/spreadsheets/1qxIGZ7GltHQ9zBy66Izv0KQ1LhPEnIiBX-hNjnBn6E4"
        response = requests.get(url, timeout=15)
        if response.status_code == 401:
            print("✅ API连接正常（未认证错误是预期的）")
        elif response.status_code == 403:
            print("✅ API连接正常（权限错误）")
        elif response.status_code == 404:
            print("⚠️ 表格ID可能不正确")
        else:
            print(f"📊 API响应状态: {response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ Google Sheets API连接超时")
    except Exception as e:
        print(f"❌ Google Sheets API连接失败: {e}")
    
    print("\n💡 网络连接诊断建议:")
    print("1. 如果连接超时，可能需要:")
    print("   - 检查防火墙设置")
    print("   - 检查公司网络限制")
    print("   - 尝试使用VPN")
    print("   - 检查网络代理配置")
    print("2. 如果DNS解析失败，可能需要:")
    print("   - 更换DNS服务器(如8.8.8.8)")
    print("   - 检查host文件")

if __name__ == "__main__":
    test_network_connectivity() 