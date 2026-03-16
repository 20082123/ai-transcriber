#!/usr/bin/env python3
"""
AI Video Transcriber - Streamlit Frontend
支持视频链接和本地文件上传
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="AI Video Transcriber",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d0b09;
    }
    .stTextArea [data-testid="stTextAreaTextArea"] {
        background-color: #171310;
        color: #ddd5cb;
    }
    [data-testid="stMarkdownContainer"] {
        color: #ddd5cb;
    }
</style>
""", unsafe_allow_html=True)

# Model configuration
MODELS = {
    "Zhipu AI (GLM-4.7-Flash)": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        "model": "glm-4.7-flash"
    },
    "Gemini (2.5-Flash)": {
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "base_url": os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
        "model": "gemini-2.5-flash"
    }
}

# Initialize session state
if 'task_id' not in st.session_state:
    st.session_state.task_id = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Temp directory
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)


def extract_audio(video_path, output_path):
    """Extract audio from video using moviepy"""
    try:
        video = VideoFileClip(str(video_path))
        video.audio.write_audiofile(
            str(output_path),
            fps=16000,
            nbytes=2,
            codec='pcm_s16le',
            ffmpeg_params=["-ac", "1"]
        )
        video.close()
        return True
    except Exception as e:
        st.error(f"音频提取失败: {e}")
        return False


def transcribe_audio(audio_path):
    """Transcribe audio using faster-whisper"""
    try:
        st.info("🔄 正在加载 Whisper 模型...")
        model = WhisperModel("base", device="cpu", compute_type="int8")

        st.info("🎙️ 正在转录音频...")
        segments, info = model.transcribe(
            str(audio_path),
            beam_size=5,
            language="zh"
        )

        transcript = ""
        for segment in segments:
            transcript += segment.text + " "

        return transcript.strip(), info.language_probability
    except Exception as e:
        st.error(f"转录失败: {e}")
        return None, 0.0


def summarize_text(text, file_name, model_config):
    """Summarize text using selected AI model"""
    try:
        client = OpenAI(
            api_key=model_config["api_key"],
            base_url=model_config["base_url"]
        )

        prompt = f"""请对以下视频转录文本进行总结：

{text}

请提供：
1. 视频主题/标题
2. 关键要点（3-5点）
3. 详细总结

输出格式：
## 视频主题
...

## 关键要点
1. ...
2. ...
3. ...

## 详细总结
...
"""

        response = client.chat.completions.create(
            model=model_config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4000
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"总结失败: {e}")
        return None


def main():
    """Main application"""
    st.title("🎬 AI Video Transcriber")

    # Model selection
    st.markdown("### ⚙️ 设置")
    col1, col2 = st.columns(2)

    with col1:
        selected_model_name = st.selectbox(
            "选择 AI 模型",
            options=list(MODELS.keys()),
            index=0,
            help="选择用于生成摘要的AI模型"
        )

    with col2:
        st.caption(f"🔑 API 状态: {'✅ 已配置' if MODELS[selected_model_name]['api_key'] else '❌ 未配置'}")

    st.markdown("---")

    # Check if selected model has API key
    if not MODELS[selected_model_name]["api_key"]:
        st.error(f"❌ {selected_model_name} 未配置 API Key！")
        st.info("📝 请在 .env 文件中配置对应的 API Key")
        if selected_model_name == "Zhipu AI (GLM-4.7-Flash)":
            st.code("""
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
            """, language="bash")
        else:
            st.code("""
GEMINI_API_KEY=your_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
            """, language="bash")
        return

    # Mode selection
    mode = st.radio(
        "选择输入模式",
        ["🔗 视频链接", "📁 本地文件"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if mode == "🔗 视频链接":
        url = st.text_input(
            "粘贴视频链接",
            placeholder="YouTube, B站, 抖音等...",
            help="支持 YouTube、B站、抖音等平台"
        )

        if st.button("🚀 开始处理", disabled=not url):
            with st.spinner("正在处理视频..."):
                st.warning("⚠️ URL 模式需要 cookies 支持，请使用本地文件模式")
                st.info("💡 建议：使用浏览器插件下载视频后，选择 '📁 本地文件' 模式")

    else:  # 本地文件模式
        uploaded_file = st.file_uploader(
            "选择视频文件",
            type=["mp4", "avi", "mov", "mkv", "webm"],
            help="支持 MP4, AVI, MOV, MKV, WEBM 格式"
        )

        if uploaded_file is not None:
            # Display file info
            file_details = {
                "文件名": uploaded_file.name,
                "文件大小": f"{uploaded_file.size / 1024 / 1024:.2f} MB"
            }
            st.json(file_details)

            if st.button("🚀 开始处理", type="primary"):
                st.session_state.processing = True

                # Save uploaded file
                task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = TEMP_DIR / f"{task_id}_{uploaded_file.name}"
                audio_path = TEMP_DIR / f"{task_id}.wav"

                with open(str(video_path), "wb") as f:
                    f.write(uploaded_file.getvalue())

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Step 1: Extract audio
                status_text.text("🎬 正在提取音频...")
                progress_bar.progress(20)
                if not extract_audio(video_path, audio_path):
                    st.session_state.processing = False
                    st.stop()

                # Step 2: Transcribe
                status_text.text("🎙️ 正在转录音频...")
                progress_bar.progress(50)
                transcript, confidence = transcribe_audio(audio_path)

                if not transcript:
                    st.session_state.processing = False
                    st.stop()

                st.success(f"✅ 转录完成！置信度: {confidence:.2f}")

                # Step 3: Summarize
                status_text.text(f"🤖 正在生成摘要 ({selected_model_name})...")
                progress_bar.progress(80)
                summary = summarize_text(transcript, uploaded_file.name, MODELS[selected_model_name])

                progress_bar.progress(100)

                # Display results
                st.markdown("---")
                st.subheader("📝 处理结果")

                if summary:
                    st.markdown(summary)

                with st.expander("📄 完整转录文本"):
                    st.text_area(
                        "转录文本",
                        transcript,
                        height=200,
                        disabled=True
                    )

                # Generate output content
                date_str = datetime.now().strftime("%Y-%m-%d")
                output_content = f"""# {uploaded_file.name}

> 📅 处理日期: {date_str}
> 📁 来源: 本地上传
> 🤖 AI模型: {selected_model_name}

---

{summary if summary else '## ❌ 摘要未生成'}

---

## 📄 完整转录

{transcript}

---

*由 AI Video Transcriber 自动生成*
"""

                # Download button
                st.download_button(
                    "📥 下载结果文件",
                    output_content,
                    f"{uploaded_file.name}_{date_str}.md",
                    mime="text/markdown",
                    key=f"download_{task_id}",
                    type="primary"
                )

                # Show save location info
                st.info(f"💾 **文件保存位置**: 点击上方按钮下载后，文件将保存在您的浏览器默认下载目录中\n\n文件名: `{uploaded_file.name}_{date_str}.md`")

                # Cleanup
                st.session_state.processing = False

                # Clean up temp files
                if audio_path.exists():
                    audio_path.unlink()
                if video_path.exists():
                    video_path.unlink()

    st.markdown("---")
    st.caption("💡 提示：处理大文件可能需要较长时间，请耐心等待")


if __name__ == "__main__":
    main()
