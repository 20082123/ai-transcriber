<div align="center">

# AI Transcriber

English | [中文](README_ZH.md)

An AI-powered tool to transcribe and summarize videos and podcasts — supports YouTube, TikTok, Bilibili, Apple Podcasts, SoundCloud, and 30+ platforms.

</div>

## ✨ Features

- 🎥 **Multi-Platform Support**: Works with YouTube, TikTok, Bilibili, Apple Podcasts, SoundCloud, and 30+ more
- ⚡ **Subtitle-First Architecture**: For platforms with native subtitles (e.g. YouTube), transcripts are extracted instantly — no audio download needed. Whisper is only used as a fallback
- 🗣️ **Intelligent Transcription**: High-accuracy speech-to-text using Faster-Whisper when subtitles aren't available
- 🤖 **AI Text Optimization**: Automatic typo correction, sentence completion, and intelligent paragraphing
- 🌍 **Multi-Language Summaries**: Generate intelligent summaries in multiple languages
- 🔧 **Bring Your Own Model**: Compatible with Zhipu AI, Gemini, and other OpenAI-compatible API endpoints
- ⚙️ **Conditional Translation**: Auto-translates the transcript when the summary language differs from the source language
- 🇨🇳 **Traditional to Simplified Chinese**: Automatic conversion of Traditional Chinese transcripts

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg
- AI API Key (Zhipu AI or Gemini)

### Installation

```bash
# Clone the repository
git clone https://github.com/20082123/ai-transcriber.git
cd ai-transcriber

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. **Configure AI API Key**

Copy environment template:
```bash
cp .env.example .env
```

Edit `.env` file with your API keys:

```bash
# Zhipu AI (recommended, fast in China)
OPENAI_API_KEY=your_zhipu_api_key_here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
DEFAULT_MODEL=glm-4.7-flash

# Gemini AI (optional)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Whisper model size
WHISPER_MODEL_SIZE=base
```

2. **Configure Cookies (optional, for Douyin/Bilibili)**

Some platforms (Douyin, Bilibili) require login to download videos. Follow these steps:

#### 🍪 Cookie Configuration Guide

**Supported browsers**: Chrome, Edge, Firefox

##### Douyin Cookie Configuration

1. Visit https://www.douyin.com and log in
2. Press `F12` to open Developer Tools
3. Click `Application` or `Storage` tab
4. Expand `Cookies` → `https://www.douyin.com`
5. Find key cookies like `sessionid`, `passport_csrf_token`
6. Click each cookie and copy its value
7. Create file `cookies/douyin.txt` with this format:

```
# Netscape HTTP Cookie File
.douyin.com	TRUE	/	FALSE	0	sessionid	your_sessionid_value
.douyin.com	TRUE	/	FALSE	0	passport_csrf_token	your_csrf_token_value
```

**Easy method**: Use browser extension like "Get cookies.txt LOCALLY" to export cookies directly.

##### Bilibili Cookie Configuration

1. Visit https://www.bilibili.com and log in
2. Export cookies using the same method
3. Save as `cookies/bilibili.txt`

##### YouTube Cookie Configuration

1. Visit https://www.youtube.com
2. Most videos work without cookies
3. For premium content, configure cookies the same way

### Usage

#### Basic Usage

```bash
# Transcribe YouTube video (auto-extract URL from text)
python transcribe.py "Check this out: https://www.youtube.com/watch?v=xxxxx"

# Transcribe local video file
python transcribe.py video.mp4

# Specify output directory
python transcribe.py --video video.mp4 --output ./my_output

# Choose AI model
python transcribe.py --video video.mp4 --model gemini
```

## ⚠️ Platform Limitations

### URL Download Support

| Platform | Cookie Required | Stability | Notes |
|----------|----------------|-----------|-------|
| **YouTube** | ❌ Not needed | ✅ Stable | Recommended |
| **Bilibili** | ⚠️ Recommended | ✅ Stable | Long cookie validity |
| **Douyin** | ⚠️ Required, complex | ❌ Unstable | Short cookie validity (3-7 days), strict anti-scraping |

### Recommendation for Douyin Users

Due to Douyin's strict anti-scraping measures, URL download often fails even with valid cookies. **Local file mode is recommended**:

```bash
# 1. Download Douyin video on mobile
# 2. Transfer to computer
# 3. Use local file mode
python transcribe.py video.mp4
```

#### Supported Input Methods

```bash
# Method 1: Direct URL
python transcribe.py "https://www.youtube.com/watch?v=xxxxx"

# Method 2: Text containing URL (auto-extract)
python transcribe.py "Recommended tutorial: https://www.bilibili.com/video/BV1xx411c7mD"

# Method 3: Local file path
python transcribe.py "/path/to/video.mp4"
```

## 🛠️ Technical Architecture

### Tech Stack
- **yt-dlp**: Video downloading and processing
- **Faster-Whisper**: Efficient speech transcription
- **OpenAI API**: Intelligent text summarization (compatible with Zhipu AI, Gemini)
- **OpenCC**: Traditional to Simplified Chinese conversion

### Project Structure
```
ai-transcriber/
├── transcribe.py       # Main program (CLI tool)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── cookies/            # Cookie files directory (optional)
│   ├── douyin.txt      # Douyin cookies
│   ├── bilibili.txt    # Bilibili cookies
│   └── youtube.txt     # YouTube cookies
├── temp/               # Temporary files (downloaded audio)
└── output/             # Output files (transcription results)
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Zhipu AI API key | - | Yes* |
| `OPENAI_BASE_URL` | API endpoint | `https://open.bigmodel.cn/api/paas/v4/` | No |
| `GEMINI_API_KEY` | Gemini API key | - | No |
| `WHISPER_MODEL_SIZE` | Whisper model size | `base` | No |

*At least one AI service must be configured

### Whisper Model Size Options

| Model | Parameters | English-only | Multilingual | Speed | Memory Usage |
|-------|------------|--------------|--------------|-------|--------------|
| tiny | 39 M | ✓ | ✓ | Fast | Low |
| base | 74 M | ✓ | ✓ | Medium | Low |
| small | 244 M | ✓ | ✓ | Medium | Medium |
| medium | 769 M | ✓ | ✓ | Slow | Medium |
| large | 1550 M | ✗ | ✓ | Very Slow | High |

## 🔧 FAQ

### Q: Why are cookies needed?
A: Platforms like Douyin and Bilibili require login to download videos. Cookies are your login credentials that allow the tool to download videos as you.

### Q: Are cookies secure?
A: Cookies only contain your login information, not passwords. Don't share cookie files with others or upload them to public repositories.

### Q: Why is transcription slow?
A: Depends on video length and Whisper model size. Try using `base` or `small` models.

### Q: Which platforms are supported?
A: All platforms supported by yt-dlp, including YouTube, TikTok, Facebook, Instagram, Bilibili, Youku, iQiyi, Tencent Video, etc.

### Q: How to get API keys?
A:
- **Zhipu AI**: Visit https://open.bigmodel.cn/ to register
- **Gemini**: Visit https://aistudio.google.com/

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
