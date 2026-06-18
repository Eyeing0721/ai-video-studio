# AI Video Studio

全栈 AI 视频生成工作台。从文本创作到成片，全自动流水线。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React 19 + TypeScript + Tailwind CSS + Vite |
| 后端 | Python FastAPI + WebSocket |
| 数据库 | SQLite |
| AI 模型 | Z-Image Turbo, Wan 2.2, Sulphur 2 |
| 视频后期 | MLT (Media Lovin' Toolkit) + FFmpeg |
| 文本 AI | DeepSeek V4 Pro |
| TTS | 阿里云百炼 Qwen |

## 功能

- **文本创作辅助** — 续写、扩写、结构化创作、自然语言修改
- **一键成片** — 文本/小说 → 分镜 → 静态图 → 视频 → 配音 → 后期合成
- **多模型路由** — Sulphur 2 (1024) / Wan 2.2 I2V (640+超分) 自动选择
- **7 主题预设** — 潘通年度色 + 日本和色 + 合成波 + 东京之夜 + 樱花
- **AI 动态调参** — 每任务根据分镜风格自动决策转场/字幕/BGM 参数
- **资产标签系统** — BGM/转场/字幕/LUT/SFX 统一标签管理
- **云端学习** — 自动抓取社区工作流和优质提示词

## 快速开始

```bash
# 后端
cd backend
pip install -r requirements.txt
python main.py

# 前端
cd frontend
npm install
npm run dev
```

## 依赖

- ComfyUI (本地运行, 端口 8188)
- DeepSeek API Key
- 阿里云百炼 API Key
