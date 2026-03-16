#!/bin/bash

# AI Transcriber Installation Script

echo "🚀 AI Transcriber 安装脚本"
echo "=========================="

# Check Python version
echo "检查Python环境..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
if [[ -z "$python_version" ]]; then
    echo "❌ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi
echo "✅ Python版本: $python_version"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi
echo "✅ pip已安装"

# Install Python dependencies
echo ""
echo "安装Python依赖..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装完成"
else
    echo "❌ Python依赖安装失败"
    exit 1
fi

# Check FFmpeg
echo ""
echo "检查FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg已安装"
else
    echo "⚠️  FFmpeg未安装，正在尝试安装..."

    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo "❌ 无法自动安装FFmpeg，请手动安装"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "❌ 请先安装Homebrew，然后运行: brew install ffmpeg"
        fi
    else
        echo "❌ 不支持的操作系统，请手动安装FFmpeg"
    fi
fi

# Create necessary directories
echo ""
echo "创建必要的目录..."
mkdir -p temp
echo "✅ 目录创建完成"

# Setup environment file
echo ""
echo "配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑填入你的 API 密钥"
else
    echo "⚠️  .env 文件已存在"
fi

echo ""
echo "🎉 安装完成!"
echo ""
echo "使用方法:"
echo "  1. 配置API密钥以启用智能摘要功能"
echo "     编辑 .env 文件，填入 OPENAI_API_KEY"
echo ""
echo "  2. 启动 Web 界面 (Streamlit):"
echo "     streamlit run streamlit_app.py"
echo ""
echo "  3. 或使用命令行工具:"
echo "     python transcribe.py video.mp4"
echo ""
echo "  4. 打开浏览器访问: http://localhost:8501"
echo ""
echo "支持的视频平台:"
echo "  - YouTube"
echo "  - Bilibili"
echo "  - 抖音"
echo "  - 其他yt-dlp支持的平台"
