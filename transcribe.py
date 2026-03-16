#!/usr/bin/env python3
"""
Video Transcriber - 统一的视频转录工具
支持：URL链接（自动提取）和本地文件路径
"""

import os
import sys
import re
import io
from pathlib import Path
from dotenv import load_dotenv

# 设置 UTF-8 编码（解决 Windows GBK 编码问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

# 配置
API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
MODEL = os.getenv("DEFAULT_MODEL", "glm-4-flash")
WHISPER_MODEL = os.getenv("WHISPER_MODEL_SIZE", "base")


def extract_url(text):
    """从文本中提取URL"""
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None


def detect_platform(url):
    """检测平台"""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lower()

    if 'douyin.com' in domain:
        return 'douyin'
    elif 'bilibili.com' in domain:
        return 'bilibili'
    elif 'youtube.com' in domain or 'youtu.be' in domain:
        return 'youtube'
    elif 'tiktok.com' in domain:
        return 'tiktok'
    return None


def download_audio(url, output_path, cookies_path=None):
    """使用yt-dlp下载音频"""
    import yt_dlp

    ydl_opts = {
        'outtmpl': str(output_path),
        'format': 'bestaudio/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.douyin.com/',
        }
    }

    if cookies_path and Path(cookies_path).exists():
        ydl_opts['cookiefile'] = str(cookies_path)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def extract_audio_from_video(video_path, audio_path):
    """从视频提取音频"""
    try:
        from moviepy import VideoFileClip
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, fps=16000, nbytes=2,
                                     codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
        video.close()
        return True
    except Exception as e:
        print(f"音频提取失败: {e}")
        return False


def transcribe_audio(audio_path):
    """使用Whisper转录音频"""
    try:
        from faster_whisper import WhisperModel
        from opencc import OpenCC

        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, beam_size=5, language="zh")

        transcript = ""
        for segment in segments:
            transcript += segment.text + " "

        # 繁体转简体
        cc = OpenCC('t2s')
        transcript = cc.convert(transcript.strip())

        print(f"转录完成！语言: {info.language}, 置信度: {info.language_probability:.2f}")
        return transcript
    except Exception as e:
        print(f"转录失败: {e}")
        return None


def summarize_text(text, file_name):
    """使用AI生成中文摘要"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        prompt = f"""请总结以下视频转录内容：

{text}

请提供：
1. 视频主题
2. 关键要点（3-5点）
3. 详细总结

请用中文回答。"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"摘要生成失败: {e}")
        return None


def save_markdown(file_name, transcript, summary, output_dir):
    """保存为Markdown文件"""
    from datetime import datetime

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{file_name}_{date_str}.md"
    output_path = Path(output_dir) / filename

    # 处理摘要失败的情况
    summary_section = summary if summary else "⚠️ 摘要生成失败（可能触发内容审核）\n\n请查看下方完整转录内容。"

    content = f"""# {file_name}

> 📅 处理日期: {date_str}
> 📁 来源: 本地文件
> 🤖 AI模型: 智谱 AI (GLM-4-Flash)

---

{summary_section}

---

## 📄 完整转录

{transcript}

---

*由 AI Video Transcriber 自动生成*
"""

    output_path.write_text(content, encoding="utf-8")
    return output_path


def auto_update_cookies():
    """自动检测并更新 Downloads 目录中的新 cookie"""
    import glob
    from datetime import datetime

    downloads = Path.home() / "Downloads"
    cookies_dir = Path(__file__).parent / "cookies"
    cookies_dir.mkdir(exist_ok=True)

    # 平台映射
    patterns = {
        'douyin': 'cookies_www.douyin.com_*.txt',
        'bilibili': 'cookies_www.bilibili.com_*.txt',
        'youtube': 'cookies_www.youtube.com_*.txt'
    }

    for platform, pattern in patterns.items():
        # 查找 Downloads 中的 cookie 文件
        cookie_files = list(downloads.glob(pattern))
        if not cookie_files:
            continue

        # 获取最新的文件
        latest_file = max(cookie_files, key=lambda p: p.stat().st_mtime)
        target_file = cookies_dir / f"{platform}.txt"

        # 检查是否需要更新
        if not target_file.exists() or latest_file.stat().st_mtime > target_file.stat().st_mtime:
            import shutil
            shutil.copy2(latest_file, target_file)
            print(f"✅ {platform} cookie 已自动更新")


def main():
    import argparse

    # 自动更新 cookie
    auto_update_cookies()

    # 参数解析
    parser = argparse.ArgumentParser(description='视频转录工具')
    parser.add_argument('input', nargs='?', help='URL文本或文件路径（简化模式）')
    parser.add_argument('--video', help='视频文件路径或URL（完整模式）')
    parser.add_argument('--output', help='输出目录（完整模式）')
    parser.add_argument('--model', default='zhipu', choices=['zhipu', 'gemini'], help='AI模型选择')

    args = parser.parse_args()

    # 确定输入和输出
    if args.video:
        # 完整模式
        user_input = args.video
        output_dir = Path(args.output) if args.output else Path("output")
    elif args.input:
        # 简化模式
        user_input = args.input
        output_dir = Path("output")
    else:
        print("用法:")
        print("  简化模式: python transcribe.py <URL文本或文件路径>")
        print("  完整模式: python transcribe.py --video <路径> --output <目录> --model <zhipu|gemini>")
        sys.exit(1)

    # 提取URL
    url = extract_url(user_input)

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    print("=" * 50)
    print("AI Video Transcriber")
    print("=" * 50)

    if url:
        # URL模式
        print(f"检测到URL: {url}")
        platform = detect_platform(url)
        print(f"平台: {platform or 'unknown'}")

        # 获取cookie
        cookies_path = None
        if platform:
            cookies_file = Path(__file__).parent / "cookies" / f"{platform}.txt"
            if cookies_file.exists():
                cookies_path = cookies_file

        # 下载音频
        audio_path = temp_dir / "downloaded_audio.m4a"
        print("\n[1/3] 下载音频...")
        if not download_audio(url, audio_path, cookies_path):
            sys.exit(1)
        print("下载完成")

        file_name = f"{platform}_video" if platform else "video"
    else:
        # 文件路径模式
        file_path = Path(user_input)
        if not file_path.exists():
            print(f"文件不存在: {user_input}")
            sys.exit(1)

        print(f"本地文件: {file_path.name}")

        # 判断是视频还是音频
        if file_path.suffix.lower() in ['.mp3', '.m4a', '.wav', '.flac']:
            audio_path = file_path
        else:
            # 提取音频
            audio_path = temp_dir / "audio.wav"
            print("\n[1/3] 提取音频...")
            if not extract_audio_from_video(str(file_path), str(audio_path)):
                sys.exit(1)
            print("音频提取完成")

        file_name = file_path.stem

    # 转录
    print(f"\n[2/3] 转录中...")
    transcript = transcribe_audio(str(audio_path))
    if not transcript:
        sys.exit(1)

    # 摘要
    print(f"\n[3/3] 生成摘要...")
    summary = summarize_text(transcript, file_name)
    if not summary:
        sys.exit(1)
    print("摘要生成完成")

    # 保存
    output_path = save_markdown(file_name, transcript, summary, output_dir)

    print("\n" + "=" * 50)
    print("处理完成！")
    print(f"输出文件: {output_path}")
    print("=" * 50)

    # 清理临时文件
    if url and audio_path.exists():
        audio_path.unlink()


if __name__ == "__main__":
    main()
