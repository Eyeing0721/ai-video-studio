---
spec_issue_number: N/A
spec_issue_url: N/A
spec_filed_at: 2026-06-19T00:00:00Z
spec_branch: unknown
spec_plan_mode: inactive
spec_executed: false
spec_worktree_path:
---

# AI 全自动短剧/视频生成 Web 工作台

## Context

当前 AI 视频生成流程分散在多个工具之间：ComfyUI 手动搭工作流、文本 LLM 单独调用、TTS 单独调百炼、剪辑手动在 PR/剪映做、资产散落各处。每个环节都要人肉衔接，无法批量生产。

本系统将全流程整合为一个本地 Web 工作台：文本创作 -> 分镜拆解 -> 静态图生成 -> 图生视频 -> 配音 -> 后期合成 -> 超分字幕，一键完成。目标用户为个人创作者，后续保留商业化扩展空间。

## Current State

| 组件 | 现状 |
|---|---|
| ComfyUI | `F:\ComfyUI`, 本地运行在 `127.0.0.1:8188` |
| 文本 LLM | DeepSeek V4 Pro API (settings.json 已配) |
| TTS | 阿里云百炼 Qwen TTS（待配 Key） |
| 视频剪辑 | 无自动化方案 |
| 资产库 | 散落各处，无统一标签体系 |

**已有模型：** Z-Image Turbo (1024), Z-Image De-Turbo (1024), Wan 2.2 T2V fp8 (640), Wan 2.2 I2V (需下载), Sulphur 2 fp8mixed+GGUF (1024), FLUX.1 Dev+FLUX.2 Klein

## Proposed Change

全栈 Web 工作台，FastAPI 后端编排 ComfyUI/DeepSeek/百炼TTS/MLT，React 19 前端。全自动流水线：文本创作 -> 分镜 -> 静态图 -> 图生视频 -> 超分 -> 配音 -> 后期合成 -> 输出。

## Architecture

```
React 19 + TypeScript + Tailwind CSS
  | WebSocket + REST
FastAPI (Python 3.11)
  |-- ComfyUI API Client
  |-- DeepSeek V4 Pro Client
  |-- 阿里云百炼 TTS Client
  |-- MLT Pipeline (视频后期)
  |-- asyncio.Queue 任务调度
SQLite
```

## Pipeline

1. 文本创作辅助 (DeepSeek: 续写/扩写/结构化/修改/富文本编辑)
2. 分镜拆解 (DeepSeek V4 Pro 推理模式 -> JSON 分镜脚本, 每个 2-5s)
3. 静态图生成 (Z-Image Turbo, 1024x1024, 自动提示词优化)
4. 图生视频 (Sulphur 2 1024 或 Wan 2.2 I2V 640->超分, 自动尾帧接续, 失败切换)
   - Sulphur 2 prompt: auto-append `[no speech, no dialogue, silent]`
5. 超分 (ComfyUI Video Upscale GAN x4, 640->1080p+)
6. 配音 (百炼 Qwen TTS, 音色克隆/ID, 干声 WAV)
7. 后期合成 (MLT: 拼接+转场(AI决策)+ASS字幕+BGM闪避+LUT)
8. 输出 (MP4 H.264 + ZIP 中间资产)

## Model Routing

| 条件 | 模型 | 分辨率 |
|---|---|---|
| 动态幅度低、写实风格 | Sulphur 2 | 1024x1024 |
| 动态幅度高、复杂场景 | Wan 2.2 I2V | 640->超分 |
| 任一失败 | 切换另一模型 | — |

## Design System

7 个预设主题：浅色(Pantone 2026 Cloud Dancer)、深色、潘通摩卡慕斯(2025)、和风樱花、合成波、东京之夜、自定义(JSON 导入导出)。首次启动主题引导。每元素颜色/圆角可调。零 emoji。

## Asset Tagging

`media_library/` 下 BGM/转场/字幕/LUT/SFX 统一标签管理。内置免版权曲库 + 用户上传。前端按标签组合筛选。

## Smart Learning

- 工作流抓取：GitHub/ComfyUI社区/CivitAI -> 解析 -> 兼容性校验 -> 入库
- 提示词学习：NLP 分析公开高质量提示词 -> 优化生成 prompt
- 社区工作流自动禁用 Prompt Enhance 节点 (DeepSeek 已做分镜层提示词)

## AI Dynamic Tuning

每个任务根据分镜 mood/节奏 AI 决策转场类型、BGM闪避参数、字幕动画速度、LUT选择。模板骨架 + AI 填参数。

## Key Decisions

- API Key 明文存储
- 单用户本地, 不上服务器
- MLT 替代 MoviePy (100+转场, 专业 ASS 字幕, 多轨合成)
- Wan 2.2 生成 640 + ComfyUI 超分到 1080p+
- 自建 asyncio.Queue 任务队列 (不需 Redis)
- SQLite 数据库 (零配置)

## Acceptance Criteria

1. 文本创作：一句话扩写为完整小说，可在线富文本编辑，自然语言修改
2. 一键成片：上传文本 -> 全自动流水线 -> MP4 + ZIP 输出
3. 分镜 JSON 合法，含所有必填字段
4. Z-Image 关键帧 1024x1024 PNG
5. Wan 2.2 640生成 + 超分 >=1080p；Sulphur 2 直接 1024
6. 尾帧接续确保画面连贯
7. Sulphur 2 prompt 含 no speech prefix
8. 导入工作流 Prompt Enhance 节点自动禁用
9. 配音-字幕时间轴对齐 <200ms
10. BGM 对话时自动闪避 (15-30% vol, attack 100ms, release 500ms)
11. 首次启动主题引导，7 主题切换无错位
12. 任务失败显示错误原因 + 支持重试
13. 资产库上传+标签+筛选
14. 启动时环境自检，缺失项前端卡片指引

## Tech Stack

| 层 | 技术 |
|---|---|
| 前端 | React 19, TypeScript, Tailwind CSS, Vite, TipTap |
| 后端 | Python FastAPI, Pydantic, SQLAlchemy |
| 数据库 | SQLite (aiosqlite) |
| 视频后期 | MLT (python-mlt), FFmpeg |
| 实时通信 | FastAPI WebSocket |
| 图像处理 | Pillow, OpenCV |
| AI 客户端 | openai (DeepSeek 兼容), alibabacloud-nls-python-sdk |

## Effort: ~84h total

| 模块 | 工时 |
|---|---|
| 项目脚手架 | 4h |
| ComfyUI Client + 工作流构建 | 8h |
| DeepSeek Client + 分镜 | 4h |
| 百炼 TTS Client | 2h |
| MLT 后期管线 | 12h |
| 任务队列 + 管线编排 | 8h |
| 资产标签系统 | 3h |
| 提示词学习 + 工作流抓取 | 8h |
| 前端主题系统 | 6h |
| 前端文本创作 | 6h |
| 前端一键成片 | 6h |
| 前端任务管理 | 6h |
| 前端资产库 | 4h |
| 前端系统设置 | 3h |
| 测试 | 8h |

## Out of Scope

- 多用户/SaaS/云端部署
- 实时协作
- 付费系统
- 移动端
- 社交媒体发布
