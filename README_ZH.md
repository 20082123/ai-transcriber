<div align="center">

# AI Transcriber | AI 视频转录器

中文 | [English](README.md)

一款开源的AI视频/播客转录和摘要工具，支持YouTube、Bilibili、抖音、Apple Podcasts、SoundCloud等30+平台。

![Interface](https://img.shields.io/badge/Interface-Streamlit-blue) ![CLI](https://img.shields.io/badge/CLI-Ready-green)

</div>

## ✨ 功能特性

- 🎥 **多平台支持**: 支持YouTube、Bilibili、抖音、Apple Podcasts、SoundCloud等30+平台
- ⚡ **字幕优先架构**: 对有原生字幕的平台（如YouTube），直接提取字幕文本，无需下载音频，速度大幅提升；无字幕时自动回退至Whisper转录
- 🗣️ **智能转录**: 无字幕时使用Faster-Whisper进行高精度语音转文字
- 🤖 **AI文本优化**: 自动错别字修正、句子完整化和智能分段
- 🌍 **多语言摘要**: 支持多种语言的智能摘要生成
- 🔧 **自定义AI模型**: 在页面中直接配置任意OpenAI兼容接口（OpenAI、OpenRouter、本地LLM等）——输入API地址和Key，点击 **Fetch** 自动获取可用模型并选择
- ⚙️ **条件式翻译**: 当所选摘要语言与转录语言不一致时，自动生成翻译
- 📱 **移动适配**: 完美支持移动设备
- 💻 **命令行工具**: 支持本地视频文件处理，无需联网

## 🚀 快速开始

### 环境要求

- Python 3.8+
- FFmpeg
- 任意OpenAI兼容服务商的API Key（智谱AI、Gemini、OpenAI等）—— 直接在页面UI中配置，无需服务器环境变量

### 安装方法

#### 方法一：Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/ai-transcriber.git
cd ai-transcriber

# 使用Docker Compose（最简单）
cp .env.example .env
# 编辑.env文件设置API密钥
docker-compose up -d

# 访问 http://localhost:8501
```

#### 方法二：手动安装

1. **安装Python依赖**（建议使用虚拟环境）
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **安装FFmpeg**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows: 从 https://ffmpeg.org/download.html 下载
```

3. **配置环境变量**（可选）
```bash
# 复制配置模板
cp .env.example .env
# 编辑 .env 文件填入你的 API 密钥
```

### 启动服务

#### Streamlit Web 界面

```bash
streamlit run streamlit_app.py
```

服务启动后，打开浏览器访问 `http://localhost:8501`

#### 命令行工具

```bash
# 简化模式：处理单个文件
python transcribe.py video.mp4

# 完整模式：指定输出和模型
python transcribe.py --video video.mp4 --output ./output --model zhipu

# URL 模式：支持视频链接（自动从文本中提取 URL）
python transcribe.py "看看这个视频：https://www.bilibili.com/video/BV1xx411c7mD"
```

## 📖 使用指南

### Web 界面

1. **输入视频链接**: 在输入框中粘贴YouTube、Bilibili等平台的视频链接
2. **选择摘要语言**: 在输入框旁的下拉菜单中选择输出语言
3. **（可选）配置AI模型**: 点击 **AI Settings** 展开配置面板
   - 填写 **API Base URL** 和 **API Key**
   - 点击 **Fetch** 自动拉取可用模型列表
   - 选择你想用的模型
4. **开始处理**: 点击 **Transcribe** 按钮，进度条会显示当前所处的模式：
   - **⚡ Subtitle**（绿色）——检测到原生字幕，秒级提取完成
   - **🎙 Whisper**（橙色）——无字幕，下载音频后转录
5. **查看结果**: 查看优化后的转录文本和AI摘要

### 命令行工具

```bash
# 处理本地视频文件
python transcribe.py video.mp4

# 指定输出目录
python transcribe.py --video video.mp4 --output ./my_output

# 选择 AI 模型（zhipu 或 gemini）
python transcribe.py --video video.mp4 --model gemini

# 处理 URL（自动从文本中提取链接）
python transcribe.py "https://www.youtube.com/watch?v=xxxxx"
```

## 🛠️ 技术架构

### 技术栈
- **Streamlit**: Web 界面框架
- **Faster-Whisper**: 高效的语音转录
- **yt-dlp**: 视频下载和处理
- **OpenAI API**: 智能文本摘要（兼容智谱AI、Gemini等）

### 项目结构
```
ai-transcriber/
├── streamlit_app.py        # Streamlit Web 界面
├── transcribe.py           # 命令行工具
├── Dockerfile              # Docker 镜像配置
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore           # Docker 忽略规则
├── .env.example            # 环境变量模板
├── requirements.txt        # Python 依赖
├── install.sh              # 自动安装脚本
├── README.md               # 项目文档
└── README_ZH.md            # 中文文档
```

## ⚙️ 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | API密钥 | - | 是 |
| `OPENAI_BASE_URL` | API地址 | `https://open.bigmodel.cn/api/paas/v4/` | 否 |
| `GEMINI_API_KEY` | Gemini API密钥 | - | 否 |
| `WHISPER_MODEL_SIZE` | Whisper模型大小 | `base` | 否 |

### Whisper模型大小选项

| 模型 | 参数量 | 英语专用 | 多语言 | 速度 | 内存占用 |
|------|--------|----------|--------|------|----------|
| tiny | 39 M | ✓ | ✓ | 快 | 低 |
| base | 74 M | ✓ | ✓ | 中 | 低 |
| small | 244 M | ✓ | ✓ | 中 | 中 |
| medium | 769 M | ✓ | ✓ | 慢 | 中 |
| large | 1550 M | ✗ | ✓ | 很慢 | 高 |

## 🔧 常见问题

### Q: 为什么转录速度很慢？
A: 转录速度取决于视频长度、Whisper模型大小和硬件性能。可以尝试使用更小的模型（如tiny或base）来提高速度。

### Q: 支持哪些视频平台？
A: 支持所有yt-dlp支持的平台，包括但不限于：YouTube、抖音、Bilibili、优酷、爱奇艺、腾讯视频等。

### Q: 如何使用Docker部署？
A:
```bash
docker-compose up -d
# 访问 http://localhost:8501
```

### Q: 内存需求是多少？
A: 推荐配置：4GB+内存。Whisper模型占用：base ~250MB，small ~750MB，medium ~1.5GB。

### Q: 网络连接错误怎么办？
A: 尝试切换VPN/代理，检查网络稳定性，或更换AI服务商端点。

## 🎯 支持的语言

### 转录
- 通过Whisper支持100+种语言
- 自动语言检测

### 摘要生成
- 英语、中文、日语、韩语、西班牙语、法语、德语、葡萄牙语、俄语、阿拉伯语等

## 📈 性能提示

| 视频长度 | 字幕模式 | Whisper模式 |
|---------|---------|------------|
| 1分钟 | ≈5秒 | 30秒–1分钟 |
| 5分钟 | ≈10秒 | 2–5分钟 |
| 15分钟 | ≈15秒 | 5–15分钟 |
| 30分钟+ | ≈20秒 | 15–60分钟 |

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📞 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## ⭐ Star History

如果您觉得这个项目有帮助，请考虑给它一个星星！
