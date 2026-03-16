<div align="center">

# AI Transcriber | AI 视频转录器

中文 | [English](README.md)

一款开源的AI视频/播客转录和摘要工具，支持YouTube、Bilibili、抖音、Apple Podcasts、SoundCloud等30+平台。

</div>

## ✨ 功能特性

- 🎥 **多平台支持**: 支持YouTube、Bilibili、抖音、Apple Podcasts、SoundCloud等30+平台
- ⚡ **字幕优先架构**: 对有原生字幕的平台（如YouTube），直接提取字幕文本，无需下载音频，速度大幅提升；无字幕时自动回退至Whisper转录
- 🗣️ **智能转录**: 无字幕时使用Faster-Whisper进行高精度语音转文字
- 🤖 **AI文本优化**: 自动错别字修正、句子完整化和智能分段
- 🌍 **多语言摘要**: 支持多种语言的智能摘要生成
- 🔧 **自定义AI模型**: 支持智谱AI、Gemini等OpenAI兼容接口
- ⚙️ **条件式翻译**: 当所选摘要语言与转录语言不一致时，自动生成翻译
- 🇨🇳 **繁简转换**: 自动将繁体中文转录结果转换为简体中文

## 🚀 快速开始

### 环境要求

- Python 3.8+
- FFmpeg
- AI API Key（智谱AI 或 Gemini）

### 安装

```bash
# 克隆项目
git clone https://github.com/20082123/ai-transcriber.git
cd ai-transcriber

# 安装依赖
pip install -r requirements.txt
```

### 配置

1. **配置 AI API 密钥**

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```bash
# 智谱 AI（推荐，国内访问快）
OPENAI_API_KEY=your_zhipu_api_key_here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
DEFAULT_MODEL=glm-4.7-flash

# Gemini AI（可选）
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Whisper 模型大小
WHISPER_MODEL_SIZE=base
```

2. **配置 Cookie（可选，用于抖音/B站）**

部分平台（抖音、B站）需要登录才能下载视频。请按以下步骤配置：

#### 🍪 Cookie 配置教程

**支持的浏览器**: Chrome, Edge, Firefox

##### 抖音 Cookie 配置

1. 访问 https://www.douyin.com 并登录
2. 按 `F12` 打开开发者工具
3. 点击 `Application` 或 `存储` 标签
4. 展开 `Cookies` → `https://www.douyin.com`
5. 找到 `sessionid`、`passport_csrf_token` 等关键 Cookie
6. 点击每个 Cookie，复制其值
7. 创建文件 `cookies/douyin.txt`，格式如下：

```
# Netscape HTTP Cookie File
.douyin.com	TRUE	/	FALSE	0	sessionid	你的sessionid值
.douyin.com	TRUE	/	FALSE	0	passport_csrf_token	你的csrf_token值
```

**简单方法**：使用浏览器插件（如 "Get cookies.txt LOCALLY"）直接导出 Cookie 文件。

##### B站 Cookie 配置

1. 访问 https://www.bilibili.com 并登录
2. 使用同样的方法导出 Cookie
3. 保存为 `cookies/bilibili.txt`

##### YouTube Cookie 配置

1. 访问 https://www.youtube.com
2. 大部分视频无需 Cookie 即可下载
3. 如需下载会员视频，按相同方法配置

### 使用方法

#### 基本用法

```bash
# 转录 YouTube 视频（自动从文本中提取 URL）
python transcribe.py "看看这个视频：https://www.youtube.com/watch?v=xxxxx"

# 转录本地视频文件
python transcribe.py video.mp4

# 指定输出目录
python transcribe.py --video video.mp4 --output ./my_output

# 选择 AI 模型
python transcribe.py --video video.mp4 --model gemini
```

#### 支持的输入方式

```bash
# 方式1: 直接粘贴 URL
python transcribe.py "https://www.youtube.com/watch?v=xxxxx"

# 方式2: 包含 URL 的文本（自动提取）
python transcribe.py "推荐这个教程：https://www.bilibili.com/video/BV1xx411c7mD"

# 方式3: 本地文件路径
python transcribe.py "/path/to/video.mp4"
```

## 🛠️ 技术架构

### 技术栈
- **yt-dlp**: 视频下载和处理
- **Faster-Whisper**: 高效的语音转录
- **OpenAI API**: 智能文本摘要（兼容智谱AI、Gemini）
- **OpenCC**: 繁简中文转换

### 项目结构
```
ai-transcriber/
├── transcribe.py       # 主程序（命令行工具）
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
├── cookies/            # Cookie 文件目录（可选）
│   ├── douyin.txt      # 抖音 Cookie
│   ├── bilibili.txt    # B站 Cookie
│   └── youtube.txt     # YouTube Cookie
├── temp/               # 临时文件（下载的音频）
└── output/             # 输出文件（转录结果）
```

## ⚙️ 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | 智谱AI API密钥 | - | 是* |
| `OPENAI_BASE_URL` | API地址 | `https://open.bigmodel.cn/api/paas/v4/` | 否 |
| `GEMINI_API_KEY` | Gemini API密钥 | - | 否 |
| `WHISPER_MODEL_SIZE` | Whisper模型大小 | `base` | 否 |

*至少配置一个 AI 服务

### Whisper模型大小选项

| 模型 | 参数量 | 英语专用 | 多语言 | 速度 | 内存占用 |
|------|--------|----------|--------|------|----------|
| tiny | 39 M | ✓ | ✓ | 快 | 低 |
| base | 74 M | ✓ | ✓ | 中 | 低 |
| small | 244 M | ✓ | ✓ | 中 | 中 |
| medium | 769 M | ✓ | ✓ | 慢 | 中 |
| large | 1550 M | ✗ | ✓ | 很慢 | 高 |

## 🔧 常见问题

### Q: 为什么需要 Cookie？
A: 抖音、B站等平台需要登录才能下载视频。Cookie 是你的登录凭证，让工具能够以你的身份下载视频。

### Q: Cookie 安全吗？
A: Cookie 仅包含你的登录信息，不包含密码。请勿将 Cookie 文件分享给他人或上传到公开仓库。

### Q: 转录速度很慢？
A: 取决于视频长度和 Whisper 模型大小。建议使用 `base` 或 `small` 模型。

### Q: 支持哪些视频平台？
A: 支持 yt-dlp 支持的所有平台，包括 YouTube、抖音、B站、优酷、爱奇艺等。

### Q: 如何获取 API 密钥？
A:
- **智谱AI**: 访问 https://open.bigmodel.cn/ 注册
- **Gemini**: 访问 https://aistudio.google.com/ 获取

## 📈 性能提示

| 视频长度 | 字幕模式 | Whisper模式 |
|---------|---------|------------|
| 1分钟 | ≈5秒 | 30秒–1分钟 |
| 5分钟 | ≈10秒 | 2–5分钟 |
| 15分钟 | ≈15秒 | 5–15分钟 |
| 30分钟+ | ≈20秒 | 15–60分钟 |

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📞 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## ⭐ Star History

如果您觉得这个项目有帮助，请考虑给它一个星星！
