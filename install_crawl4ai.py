#!/usr/bin/env python3
"""
Crawl4AI 安装和配置脚本
自动安装和配置crawl4ai及其依赖项
"""

import sys
import subprocess
import os
import importlib.util
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并处理错误"""
    print(f"🔄 {description}")
    print(f"   执行: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - 成功")
            if result.stdout:
                print(f"   输出: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - 失败")
            print(f"   错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - 异常: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    print(f"   当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本检查通过")
    return True

def install_requirements():
    """安装requirements.txt中的依赖"""
    print("📦 安装Python依赖...")
    
    # 先升级pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip"):
        return False
    
    # 安装requirements.txt
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装requirements.txt"):
            return False
    else:
        print("❌ requirements.txt文件不存在")
        return False
    
    return True

def install_crawl4ai():
    """安装crawl4ai"""
    print("🚀 安装crawl4ai...")
    
    # 卸载旧版本
    run_command(f"{sys.executable} -m pip uninstall -y crawl4ai", "卸载旧版本crawl4ai")
    
    # 安装新版本
    if not run_command(f"{sys.executable} -m pip install crawl4ai==0.7.0", "安装crawl4ai 0.7.0"):
        return False
    
    # 安装可选依赖
    optional_deps = [
        "playwright==1.40.0",
        "pydantic==2.5.0",
        "httpx==0.24.1"
    ]
    
    for dep in optional_deps:
        run_command(f"{sys.executable} -m pip install {dep}", f"安装{dep}")
    
    return True

def setup_playwright():
    """设置Playwright浏览器"""
    print("🌐 设置Playwright浏览器...")
    
    # 安装Playwright
    if not run_command(f"{sys.executable} -m pip install playwright", "安装Playwright"):
        return False
    
    # 安装浏览器
    if not run_command(f"{sys.executable} -m playwright install", "安装浏览器"):
        return False
    
    # 安装系统依赖
    if not run_command(f"{sys.executable} -m playwright install-deps", "安装系统依赖"):
        print("⚠️  系统依赖安装失败，但可能不影响使用")
    
    return True

def test_crawl4ai_import():
    """测试crawl4ai导入"""
    print("🧪 测试crawl4ai导入...")
    
    try:
        # 测试基本导入
        import crawl4ai
        print(f"✅ crawl4ai版本: {crawl4ai.__version__}")
        
        # 测试详细导入
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
        print("✅ 核心类导入成功")
        
        # 测试策略导入
        from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
        print("✅ 提取策略导入成功")
        
        # 测试内容过滤器导入
        from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
        print("✅ 内容过滤器导入成功")
        
        # 测试Markdown生成器导入
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        print("✅ Markdown生成器导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def run_simple_test():
    """运行简单的功能测试"""
    print("🔬 运行简单功能测试...")
    
    test_code = '''
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def test_crawl():
    config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig(
        output_formats=["markdown"],
        cache_mode=None
    )
    
    async with AsyncWebCrawler(config=config) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=run_config
        )
        
        if result.success:
            print(f"✅ 测试成功: 获取到 {len(result.markdown.fit_markdown)} 字符的内容")
            return True
        else:
            print(f"❌ 测试失败: {result.error_message}")
            return False

# 运行测试
if __name__ == "__main__":
    result = asyncio.run(test_crawl())
    exit(0 if result else 1)
'''
    
    try:
        # 创建临时测试文件
        test_file = Path("temp_test_crawl4ai.py")
        test_file.write_text(test_code)
        
        # 运行测试
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 清理临时文件
        test_file.unlink()
        
        if result.returncode == 0:
            print("✅ 功能测试通过")
            print(f"   输出: {result.stdout.strip()}")
            return True
        else:
            print("❌ 功能测试失败")
            print(f"   错误: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Crawl4AI 安装和配置脚本")
    print("=" * 50)
    
    success = True
    
    # 检查Python版本
    if not check_python_version():
        success = False
    
    # 安装依赖
    if success and not install_requirements():
        success = False
    
    # 安装crawl4ai
    if success and not install_crawl4ai():
        success = False
    
    # 设置Playwright
    if success and not setup_playwright():
        success = False
    
    # 测试导入
    if success and not test_crawl4ai_import():
        success = False
    
    # 运行功能测试
    if success and not run_simple_test():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Crawl4AI 安装和配置完成！")
        print("\n📝 下一步:")
        print("1. 运行 python main.py 开始使用")
        print("2. 查看 CRAWL4AI_README.md 了解更多信息")
    else:
        print("❌ 安装过程中遇到问题")
        print("\n🔧 故障排除:")
        print("1. 检查Python版本是否>= 3.8")
        print("2. 确保网络连接正常")
        print("3. 尝试手动安装: pip install crawl4ai==0.7.0")
        print("4. 查看详细错误信息")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 