# GitHub Secrets 设置指南

## 📋 必需的Secrets列表

### 1. OPENAI_API_KEY
- **值**: 你的OpenAI API密钥
- **示例**: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### 2. GOOGLE_SHEETS_ID  
- **值**: 1qxIGZ7GltHQ9zBy66lzv0KQ1LhPEnIiBX-hNjnBn6E4
- **说明**: 这是你的Google Sheets文档ID

### 3. GOOGLE_SHEETS_CREDENTIALS
- **值**: credentials.json文件的完整内容
- **注意**: 复制整个JSON文件内容，包括所有花括号

### 4. GOOGLE_SHEETS_RANGE (可选)
- **值**: Sheet1!A:Z
- **说明**: Google Sheets的数据范围

### 5. TARGET_URL (可选)
- **值**: https://theresanaiforthat.com/trending/week/top-50/?pos=1
- **说明**: 要爬取的目标网站

### 6. NOTIFICATION_WEBHOOK_URL (可选)
- **值**: 你的通知webhook URL (如Slack、Discord等)
- **说明**: 用于接收运行结果通知

### 7. NOTIFICATION_EMAIL (可选)  
- **值**: 你的邮箱地址
- **说明**: 用于邮件通知

## 🔧 设置步骤

### 步骤1：进入GitHub仓库
1. 打开你的GitHub仓库页面
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Secrets and variables** > **Actions**

### 步骤2：添加每个Secret
1. 点击 **New repository secret**
2. 输入 **Name** (密钥名称)
3. 输入 **Value** (密钥值) 
4. 点击 **Add secret**

### 步骤3：验证设置
确保所有必需的secrets都已添加：
- ✅ OPENAI_API_KEY
- ✅ GOOGLE_SHEETS_ID  
- ✅ GOOGLE_SHEETS_CREDENTIALS
- ✅ GOOGLE_SHEETS_RANGE
- ✅ TARGET_URL

## ⚠️ 重要注意事项

1. **GOOGLE_SHEETS_CREDENTIALS**: 这是最重要的，必须复制credentials.json的完整内容
2. **不要在代码中暴露这些敏感信息**
3. **确保credentials.json文件在本地项目根目录下**
4. **OPENAI_API_KEY必须有效且有足够余额** 