<div align="center">

# AI Transcriber

English | [中文](README_ZH.md)

An AI-powered tool to transcribe and summarize videos and podcasts — supports YouTube, TikTok, Bilibili, Apple Podcasts, SoundCloud, and 30+ platforms.

![Interface](https://img.shields.io/badge/Interface-Streamlit-blue) ![CLI](https://img.shields.io/badge/CLI-Ready-green)

</div>

## ✨ Features

- 🎥 **Multi-Platform Support**: Works with YouTube, TikTok, Bilibili, Apple Podcasts, SoundCloud, and 30+ more
- ⚡ **Subtitle-First Architecture**: For platforms with native subtitles (e.g. YouTube), transcripts are extracted instantly — no audio download needed. Whisper is only used as a fallback
- 🗣️ **Intelligent Transcription**: High-accuracy speech-to-text using Faster-Whisper when subtitles aren't available
- 🤖 **AI Text Optimization**: Automatic typo correction, sentence completion, and intelligent paragraphing
- 🌍 **Multi-Language Summaries**: Generate intelligent summaries in multiple languages
- 🔧 **Bring Your Own Model**: Configure any OpenAI-compatible API endpoint (OpenAI, OpenRouter, local LLM, etc.) directly in the UI
- ⚙️ **Conditional Translation**: Auto-translates the transcript when the summary language differs from the source language
- 📱 **Mobile-Friendly**: Perfect support for mobile devices
- 💻 **CLI Tool**: Support for local video file processing without internet connection

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg
- An API key from any OpenAI-compatible provider (Zhipu AI, Gemini, OpenAI, etc.)

### Installation

#### Method 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-transcriber.git
cd ai-transcriber

# Using Docker Compose (easiest)
cp .env.example .env
# Edit .env file to set your API key
docker-compose up -d

# Visit http://localhost:8501
```

#### Method 2: Manual Installation

1. **Install Python Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Install FFmpeg**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

3. **Configure Environment Variables** (optional)
```bash
cp .env.example .env
# Edit .env file and add your API key
```

### Start the Service

#### Streamlit Web Interface

```bash
streamlit run streamlit_app.py
```

After the service starts, open your browser and visit `http://localhost:8501`

#### Command Line Tool

```bash
# Simple mode: process a single file
python transcribe.py video.mp4

# Full mode: specify output and model
python transcribe.py --video video.mp4 --output ./output --model zhipu

# URL mode: extract URL from text automatically
python transcribe.py "Check this out: https://www.youtube.com/watch?v=xxxxx"
```

## 📖 Usage Guide

### Web Interface

1. **Enter Video URL**: Paste a video link from YouTube, Bilibili, or other supported platforms
2. **Select Summary Language**: Choose the output language from the dropdown
3. **(Optional) Configure AI Model**: Click **AI Settings** to expand the panel
   - Enter your **API Base URL** and **API Key**
   - Click **Fetch** to auto-load available models
   - Select the model you want to use
4. **Start Processing**: Click the **Transcribe** button. The progress bar shows which mode is active:
   - **⚡ Subtitle** (green) — native subtitles found, transcript extracted in seconds
   - **🎙 Whisper** (amber) — no subtitles available, downloading audio for transcription
5. **View Results**: Review the optimized transcript and AI summary

### Command Line Tool

```bash
# Process local video file
python transcribe.py video.mp4

# Specify output directory
python transcribe.py --video video.mp4 --output ./my_output

# Choose AI model (zhipu or gemini)
python transcribe.py --video video.mp4 --model gemini

# Process URL (automatically extract link from text)
python transcribe.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

## 🛠️ Technical Architecture

### Tech Stack
- **Streamlit**: Web interface framework
- **Faster-Whisper**: Efficient speech transcription
- **yt-dlp**: Video downloading and processing
- **OpenAI API**: Intelligent text summarization (compatible with Zhipu AI, Gemini, etc.)

### Project Structure
```
ai-transcriber/
├── streamlit_app.py        # Streamlit Web Interface
├── transcribe.py           # Command Line Tool
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Docker ignore rules
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── install.sh              # Auto-install script
├── README.md               # Project documentation
└── README_ZH.md            # Chinese documentation
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | API key | - | Yes |
| `OPENAI_BASE_URL` | API endpoint | `https://open.bigmodel.cn/api/paas/v4/` | No |
| `GEMINI_API_KEY` | Gemini API key | - | No |
| `WHISPER_MODEL_SIZE` | Whisper model size | `base` | No |

### Whisper Model Size Options

| Model | Parameters | English-only | Multilingual | Speed | Memory Usage |
|-------|------------|--------------|--------------|-------|--------------|
| tiny | 39 M | ✓ | ✓ | Fast | Low |
| base | 74 M | ✓ | ✓ | Medium | Low |
| small | 244 M | ✓ | ✓ | Medium | Medium |
| medium | 769 M | ✓ | ✓ | Slow | Medium |
| large | 1550 M | ✗ | ✓ | Very Slow | High |

## 🔧 FAQ

### Q: Why is transcription slow?
A: Transcription speed depends on video length, Whisper model size, and hardware performance. Try using smaller models (like tiny or base).

### Q: Which video platforms are supported?
A: All platforms supported by yt-dlp, including: YouTube, TikTok, Facebook, Instagram, Twitter, Bilibili, Youku, iQiyi, Tencent Video, etc.

### Q: How to use Docker?
A:
```bash
docker-compose up -d
# Visit http://localhost:8501
```

### Q: What are the memory requirements?
A: Recommended: 4GB+ RAM. Whisper model usage: base ~250MB, small ~750MB, medium ~1.5GB.

### Q: Network connection errors?
A: Try switching VPN/proxy, check network stability, or change AI provider endpoint.

## 🎯 Supported Languages

### Transcription
- Supports 100+ languages through Whisper
- Automatic language detection

### Summary Generation
- English, Chinese, Japanese, Korean, Spanish, French, German, Portuguese, Russian, Arabic, and more

## 📈 Performance Tips

| Video Length | Subtitle Mode | Whisper Mode |
|-------------|---------------|--------------|
| 1 minute | ~5s | 30s–1 min |
| 5 minutes | ~10s | 2–5 min |
| 15 minutes | ~15s | 5–15 min |
| 30+ minutes | ~20s | 15–60 min |

## 🤝 Contributing

We welcome Issues and Pull Requests!

## 📞 License

MIT License - see [LICENSE](LICENSE) file for details

## ⭐ Star History

If you find this project helpful, please consider giving it a star!
