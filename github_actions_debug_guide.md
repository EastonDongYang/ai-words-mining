# GitHub Actions 调试完全指南

## 🚀 快速开始

### 步骤1：准备credentials.json内容
1. 打开本地的 `credentials.json` 文件
2. **全选复制所有内容** (Ctrl+A, Ctrl+C)
3. 这将用于GitHub Secrets中的 `GOOGLE_SHEETS_CREDENTIALS`

### 步骤2：设置GitHub Secrets
进入你的GitHub仓库 → Settings → Secrets and variables → Actions

必需设置的Secrets：
```
OPENAI_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_SHEETS_ID = 1qxIGZ7GltHQ9zBy66lzv0KQ1LhPEnIiBX-hNjnBn6E4
GOOGLE_SHEETS_CREDENTIALS = [整个credentials.json文件内容]
GOOGLE_SHEETS_RANGE = Sheet1!A:Z
TARGET_URL = https://theresanaiforthat.com/trending/week/top-50/?pos=1
```

可选设置：
```
NOTIFICATION_WEBHOOK_URL = 你的webhook地址
NOTIFICATION_EMAIL = 你的邮箱
```

## 🧪 测试GitHub Actions

### 方法1：手动触发测试
1. 进入GitHub仓库
2. 点击 **Actions** 标签
3. 选择 "AI Words Mining System" 工作流
4. 点击 **Run workflow** 按钮
5. 选择：
   - ✅ **Enable debug mode**: true
   - ✅ **Run in test mode**: true
6. 点击 **Run workflow**

### 方法2：推送代码触发
```bash
git add .
git commit -m "Test GitHub Actions"
git push origin main
```

## 🔍 调试技巧

### 1. 查看运行日志
1. Actions → 选择运行记录 → 点击具体的job
2. 展开每个步骤查看详细日志
3. 查找 ❌ 红色错误标记

### 2. 常见错误及解决方案

#### 错误：Secrets not found
```
Error: Required secret OPENAI_API_KEY not found
```
**解决**: 检查Secrets拼写，确保已正确添加

#### 错误：Google Sheets认证失败
```
Error: Failed to authenticate with Google Sheets
```
**解决**: 
- 检查 `GOOGLE_SHEETS_CREDENTIALS` 是否完整
- 确保服务账户有编辑权限

#### 错误：OpenAI API失败
```
Error: OpenAI API request failed
```
**解决**:
- 检查API密钥是否有效
- 确认账户有足够余额

#### 错误：网页爬取失败
```
Error: Failed to scrape AI tools
```
**解决**:
- 这是正常的，系统会自动使用模拟数据
- 检查日志中的 "使用模拟数据" 信息

### 3. 启用调试模式
手动运行时选择 "Enable debug mode" = true
- 会上传调试文件
- 提供更详细的日志
- 保存中间结果文件

## 📊 监控运行状态

### 运行成功的标志：
- ✅ 所有步骤都是绿色
- 📊 Google Sheets 有新数据
- 📬 收到成功通知（如果配置了）

### 运行失败的处理：
- 📋 查看错误日志
- 🔧 修复问题
- 🔄 重新运行工作流

## ⏰ 定时任务设置

当前设置：每天早上6:00 UTC 自动运行
```yaml
schedule:
  - cron: '0 6 * * *'
```

修改运行时间：
- `0 6 * * *` = 每天 6:00 UTC (北京时间 14:00)
- `0 14 * * *` = 每天 14:00 UTC (北京时间 22:00)
- `0 */6 * * *` = 每6小时运行一次

## 🎯 故障排除清单

运行前检查：
- [ ] 所有必需的Secrets已设置
- [ ] OPENAI_API_KEY 有效且有余额
- [ ] Google Sheets 可以正常访问
- [ ] credentials.json 内容完整

运行失败时检查：
- [ ] 查看Actions运行日志
- [ ] 检查错误消息
- [ ] 验证Secrets配置
- [ ] 测试本地运行是否正常

## 📞 获取帮助

如果遇到问题：
1. 📋 复制完整的错误日志
2. 🔍 检查上述故障排除清单
3. 💬 描述具体的错误情况 