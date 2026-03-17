---
name: ai-transcriber
description: Intelligent video transcription assistant for AI-powered video content
version: "1.0.0"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Question
user-invocable: true
---

# AI Transcriber / AI 视频转录助手

## Overview | 概述

Intelligent video transcription assistant that guides users through the entire process of downloading, transcribing, and summarizing video content from various platforms.

智能视频转录助手，引导用户完成从各种平台下载、转录和总结视频内容的整个流程。

Built on ai-transcriber project | 基于 ai-transcriber 项目：https://github.com/20082123/ai-transcriber

---

## User Interaction Flow | 用户交互流程

### Basic Usage | 基本用法

#### 1. Simple Mode | 简单模式（推荐）

```
User | 用户：帮我转录这个抖音视频
https://www.douyin.com/video/123456789

AI Response | AI 响应：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
检测到 Douyin 链接！

正在检查配置...
✅ Python 环境就绪
✅ FFmpeg 已安装
⚠️  检测到需要 Cookie（抖音链接需要登录验证）

是否配置 Cookie？
[跳过（可能失败）] [配置 Cookie]

User 选择：配置 Cookie

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/3] 下载音频中... ✨
[2/3] 语音转录中... 🔊
[3/3] 生成摘要中... 🤖

✅ 处理完成！

## 📝 视频摘要

**主题**: 最新 AI 技术发展概览
**关键要点:**
1. 多模态大模型进展
2. 推理能力提升
3. 应用场景扩展

**详细总结:**
本文介绍了当前人工智能领域的前沿技术...

📄 完整转录已保存到：
output/douyin_video_2026-03-16.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Direct URL | 直接提供 URL

```
User | 用户：转录：https://www.douyin.com/video/xyz

↓ (AI 自动执行完整流程)

✅ 完成！摘要和完整转录已保存
```

#### 3. Local File | 本地文件

```
User | 用户：转录这个本地视频文件
/path/to/my/video.mp4

↓ (AI 自动提取音频并处理)

✅ 完成！
```

---

## Advanced Usage | 高级用法

### Model Selection | 模型选择

```
User: 使用 Gemini 模型转录
AI: 正在使用 Gemini 模型...
```

Options | 选项：
- `zhipu`（默认，中国用户推荐）
- `gemini`

### Custom Output Directory | 自定义输出目录

```
User: 转录视频，输出到 reports/
AI: 输出将保存到：reports/
```

### Platform List | 支持的平台

| Platform | Cookie Required | Speed | 说明 |
|----------|----------------|-------|------|
| **Douyin** | ⚠️ Recommended | ✅ Stable | 抖音（推荐配置 Cookie） |
| **YouTube** | ❌ Not needed | ✅ Stable | 推荐，稳定性高 |
| **Bilibili** | ⚠️ Suggested | ✅ Stable | B 站（建议配置） |
| **TikTok** | ⚠️ Recommended | ⚠️ Variable | TikTok |
| **Local File**| ❌ No | ✅ Fast | 本地文件（最快） |

---

## When to Use | 使用场景

| Scenario | 场景 | Usage | 用法 |
|----------|------|-------|------|
| 抖音内容整理 | Content curation | 一键转录并生成笔记 | One-click transcription |
| 课程视频学习 | Study materials | 生成结构化学习摘要 | Structured learning notes |
| 会议录音转录 | Meeting notes | 快速转换为文字 | Quick transcription |
| Podcast 整理 | Podcast management | 音频转文字 + 摘要 | Transcription + summary |
| 多语言内容 | Cross-language | 中文摘要 + 英文原文 | Chinese summary + English original |

---

## Architecture | 架构

**Complete integrated skill | 完整集成技能**

All functionality combined into one skill:
- User interaction & guidance | 用户交互和引导
- Configuration validation | 配置验证
- Cookie management | Cookie 管理
- Progress tracking | 进度跟踪
- Result display | 结果展示

Core capabilities 核心功能：
- Input processing | 输入处理
- Audio download/extract | 音频下载/提取
- Speech transcription | 语音转录
- AI summary generation | AI 摘要生成
- Markdown output | Markdown 输出

---

## Quick Start Guide | 快速开始指南

### Step 1: Install Dependencies | 步骤 1：安装依赖

```bash
cd /mnt/data2/home/hsy/Projects/ai-transcriber
pip install -r requirements.txt

# System dependency 系统依赖
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: Download from ffmpeg.org
```

### Step 2: Configure API Key | 步骤 2：配置 API 密钥

```bash
cp .env.example .env

# Edit .env file
nano .env
```

Add your API key | 添加 API 密钥：
```bash
OPENAI_API_KEY=your_zhipu_api_key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
DEFAULT_MODEL=glm-4-flash
WHISPER_MODEL_SIZE=base
```

### Step 3: Setup Cookie (for Douyin) | 步骤 3：配置 Cookie（抖音）

```bash
# Method 1: Browser extension 浏览器扩展
1. Install: "Get cookies.txt LOCALLY"
2. Login to https://www.douyin.com
3. Export cookies
4. Save to: ai-transcriber/cookies/douyin.txt

# Method 2: Manual 手动方式
1. Open browser F12 → Application/Storage → Cookies
2. Find: sessionid, passport_csrf_token
3. Copy values
4. Create cookies/douyin.txt with format:
```

```
# Netscape HTTP Cookie File
.douyin.com	TRUE	/	FALSE	0	sessionid	your_session_value
.douyin.com	TRUE	/	FALSE	0	passport_csrf_token	your_token_value
```

### Step 4: Start Using | 步骤 4：开始使用

```bash
# Option A: Use through opencode (recommended)
opencode "帮我转录：https://www.douyin.com/video/xxx"

# Option B: Run directly
cd ai-transcriber
python transcribe.py "https://www.douyin.com/video/xxx"
```

---

## System Requirements | 系统要求

### Software Dependencies | 软件依赖

| Package | Version | Purpose | 用途 |
|---------|---------|---------|------|
| Python | 3.8+ | Runtime | 运行环境 |
| yt-dlp | >=2024.12.13 | Video download | 视频下载 |
| faster-whisper | >=1.1.0 | Transcription | 语音转录 |
| openai | >=1.51.0 | AI API | AI API |
| python-dotenv | >=1.0.0 | Env管理 | 环境变量 |
| OpenCC | >=0.1.7 | Chinese conversion | 中文转换 |

### System Dependencies | 系统依赖

- **FFmpeg**: Required for audio/video processing
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: Download from https://ffmpeg.org

### Hardware Requirements | 硬件要求

| Task | Minimum | Recommended |
|------|---------|-------------|
| Transcription (CPU) | 2GB RAM | 4GB RAM |
| Whisper model | Any CPU | Intel/Apple Silicon |
| AI API | Internet | Stable connection |

---

## Configuration Reference | 配置参考

### Environment Variables | 环境变量

```bash
# AI Service Configuration
# AI 服务配置

# Zhipu AI (Recommended for China)
# 智谱 AI（中国推荐）
export OPENAI_API_KEY=your_key
export OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
export DEFAULT_MODEL=glm-4-flash

# Alternative: Google Gemini
# 可选：Google Gemini
export GEMINI_API_KEY=your_key
export GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Whisper Model Settings
# Whisper 模型设置

export WHISPER_MODEL_SIZE=base
# Options: tiny, base, small, medium, large

# Output Settings
# 输出设置

export OUTPUT_DIR=output
```

### Whisper Model Comparison | Whisper 模型对比

| Model | Size | Speed | Quality | Memory |
|-------|------|-------|---------|--------|
| tiny | 39MB | Fastest | Good | Low |
| **base** | **74MB** | **Fast** | **Good** | **Low** |
| small | 246MB | Medium | Better | Medium |
| medium | 768MB | Slow | Best | High |
| large | 1.5GB | Slowest | Best | Very High |

**Recommendation | 推荐**: Use `base` for balance, `small` for better accuracy

---

## Common Workflows | 常见工作流

### Workflow 1: Quick Douyin Taked | 快速抖音记录

```
1. User provides Douyin link
2. AI checks cookie status
3. Automatic download → transcribe → summarize
4. Review and save notes
```

**Use case**: Daily content capture / 日常内容捕获

### Workflow 2: Course Video Learning | 课程学习

```
1. Upload course video or provide link
2. Multiple passes if needed
3. Review AI summary for key concepts
4. Refer to full transcript for details
```

**Use case**: Online courses / 在线课程

### Workflow 3: Podcast Production | 播客制作

```
1. Process audio file
2. Generate transcript
3. Create show notes from summary
4. Archive for future reference
```

**Use case**: Content repurposing / 内容再利用

---

## Output Format | 输出格式

### Example Markdown Output | 示例输出

```markdown
# 最新 AI 技术进展

> 📅 Date | 日期：2026-03-16
> 📁 Source | 来源：Douyin
> 🤖 Model | 模型：GLM-4-Flash

---

## 📝 Summary | 摘要

### Topic | 主题
人工智能领域最新技术发展与趋势分析

### Key Points | 关键要点
1. 多模态大模型能力持续增强
2. 推理与规划能力提升显著
3. 企业级应用场景不断扩展

### Detailed Summary | 详细总结
本期视频深入探讨了当前 AI 领域的三大发展方向...

---

## 📄 Full Transcript | 完整转录

[完整转录内容...]

---

*Generated by AI Transcriber / 由 AI 转录助手自动生成*
```

---

## Troubleshooting | 故障排除

### Issue 1: Cookie Authentication Failed | Cookie 认证失败

```
Error: Download failed / 下载失败
→ Cookie may be expired / Cookie 可能已过期
→ Re-export cookies from Douyin / 重新导出 Cookie
→ Cookie valid for 3-7 days / Cookie 有效期 3-7 天
```

### Issue 2: API Key Invalid | API 密钥无效

```
Error: Invalid API key / 无效的 API 密钥
→ Check .env file / 检查.env 文件
→ Verify key is correctly set / 确认密钥设置正确
→ Ensure no extra spaces / 确保无多余空格
```

### Issue 3: Slow Transcription | 转录速度慢

```
Long processing time / 处理时间长
→ Use smaller Whisper model: WHISPER_MODEL_SIZE=tiny
→ Check CPU usage / 检查 CPU 使用率
→ Try during off-peak hours / 避开高峰期使用
```

### Issue 4: FFmpeg Not Found | FFmpeg 未找到

```
Error: FFmpeg not installed / FFmpeg 未安装
→ Install FFmpeg / 安装 FFmpeg
→ macOS: brew install ffmpeg
→ Ubuntu: sudo apt install ffmpeg
→ Windows: Download from ffmpeg.org
```

### Issue 5: Memory Error | 内存不足

```
Error: Out of memory / 内存不足
→ Use smaller model: tiny or base
→ Close other applications / 关闭其他应用
→ Restart system if needed / 必要时重启系统
```

---

## Performance Tips | 性能建议

### Speed Optimization | 速度优化

1. **Use subtitle extraction when available**
   优先使用字幕提取功能

2. **Choose right Whisper model**
   选择合适的 Whisper 模型
   - `tiny`: Fast tests / 快速测试
   - `base`: Good balance / 良好平衡
   - `small`: Better accuracy / 更好精度

3. **Process during off-peak hours**
   避开高峰时段处理

4. **Use local files for Douyin**
   抖音视频使用本地文件模式更快

### Quality Optimization | 质量优化

1. **Ensure good audio quality**
   确保音频质量良好

2. **Configure cookies properly**
   正确配置 Cookie

3. **Use appropriate model**
   使用合适的 AI 模型

4. **Review and edit results**
   检查结果并编辑

---

## Tips for Douyin Users | 抖音用户建议

### Cookie Management | Cookie 管理

```
✅ Store cookies securely
   安全存储 Cookie

✅ Re-export every 3-7 days
   每 3-7 天重新导出

✅ Never share cookie files publicly
   不要公开分享 Cookie 文件

✅ Use local file mode as backup
   使用本地文件模式作为备用
```

### Recommended Workflow | 推荐工作流

```
1. Download video on mobile / 手机下载视频
2. Transfer to computer / 传输到电脑
3. Process with local file mode / 使用本地文件处理
4. Faster and more reliable / 更快更可靠
```

---

## Integration with Other Tools | 与其他工具集成

### Note-taking Apps | 笔记应用

```markdown
# Import to Obsidian / Notion
- Output format: Markdown
- Supports tags and metadata
- Easy to organize by date/project
```

### Search and Indexing | 搜索和索引

```bash
# Search within transcripts
grep "关键词" output/*.md

# Index for search
find output -name "*.md" -exec echo {} \;
```

---

## Legal & Ethics | 法律与伦理

### Usage Guidelines | 使用指南

- ✅ Use for personal learning and notes 用于个人学习和笔记
- ✅ Respect copyright and terms of service 尊重版权和服务条款
- ❌ Don't redistribute content without permission 未经同意不重新分发
- ❌ Don't use for commercial purposes without licenses 未经授权不商用

### Platform Terms | 平台条款

- Always respect platform ToS
- Cookies for personal use only
- Consider support content creators
- Fair use policies apply

---

## Comparison with Alternatives | 与其他方案对比

| Feature | AI Transcriber | Whisper Web | Manual |
|---------|----------------|-------------|--------|
| Speed | Fast ⚡ | Medium ⚡⚡ | Slow ⚡⚡⚡ |
| Summary | AI-generated | None | Manual |
| Price | Free* | Free | Free |
| Accuracy | High ✅ | High ✅ | High ✅ |
| Languages | Many | Many | Any |

*Requires own API key

---

## Frequently Asked Questions | 常见问题

### Q: 需要付费吗？ | Q: Is it paid?

A: 核心功能免费，需要自己的 API 密钥。可以使用智谱 AI 免费额度。
Core features are free, you need your own API key.

### Q: 支持哪些视频平台？ | Q: Which platforms are supported?

A: 支持 30+ 平台，包括 YouTube、B 站、抖音、TikTok 等。
Supports 30+ platforms including YouTube, Bilibili, Douyin, etc.

### Q: 繁体中文会自动转简体吗？ | Q: Does it convert Traditional to Simplified?

A: 是的，自动转换繁体中文为简体中文。
Yes, automatically converts Traditional to Simplified Chinese.

### Q: 处理速度快吗？ | Q: How fast is it?

A: YouTube 有字幕时秒级完成，无字幕约 30 秒/分钟。
Seconds for YouTube with subtitles, ~30s/min without.

### Q: 隐私安全吗？ | Q: Is it private?

A: 音频处理在本地，AI API 调用遵循服务商隐私政策。
Audio processed locally, AI API follows provider policies.

### Q: 可以不配置 Cookie 吗？ | Q: Can I skip cookies?

A: 可以，但抖音链接可能无法下载。推荐使用本地文件模式。
Yes, but Douyin links may fail. Use local file mode.

---

## Future Enhancements | 未来改进

- [ ] Batch processing 批量处理
- [ ] Real-time transcription 实时转录
- [ ] More AI models support 更多 AI 模型
- [ ] Translation features 翻译功能
- [ ] Speaker diarization 说话人识别
- [ ] Cloud integration 云存储集成

---

## Getting Help | 获取帮助

### Documentation | 文档

- 📖 Full README: [README.md](https://github.com/20082123/ai-transcriber)
- 📚 Chinese guide: [README_ZH.md](https://github.com/20082123/ai-transcriber)
- 🧩 This skill: [/skills/ai-transcriber/](/mnt/data2/home/hsy/Projects/AgentResearch/skills/ai-transcriber/)

### Support | 支持

- 🐛 Issues: Report bugs or suggestions
- 💡 Ideas: Feature requests welcome
- 📝 Docs: Contribute to documentation

---

## License | 许可

Apache License 2.0 - See [LICENSE](https://github.com/20082123/ai-transcriber) for details

---

## Credits | 致谢

Built by [20082123](https://github.com/20082123)
- Based on yt-dlp community
- Powered by Faster-Whisper
- AI models: Zhipu AI, Gemini, OpenAI

感谢所有开源项目的贡献者！🙏

---

## Final Checklist | 最终检查清单

Before starting, ensure:

- [ ] Python 3.8+ installed / Python 已安装
- [ ] FFmpeg installed / FFmpeg 已安装
- [ ] API key configured / API 密钥已配置
- [ ] Cookie file ready (for Douyin) / Cookie 文件准备
- [ ] Network connection stable / 网络稳定
- [ ] Sufficient disk space / 磁盘空间充足
- [ ] Understanding of platform ToS / 了解平台条款

Ready to transcribe? 🚀 / 准备好开始转录了吗？