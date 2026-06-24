---
title: "AI Studio-帮助文档"
source: "https://ai.baidu.com/ai-doc/AISTUDIO/bmfl1tnm4"
author:
published:
created: 2026-06-24
description: "百度AI Studio是面向AI学习者的一站式开发实训平台. 本平台集合了AI课程, 深度学习样例工程, 各领域的经典数据集, 云端的超强运算及存储资源, 以及比赛和社区. 你可以学习AI课程，提升技能，平台提供视频、项目、文档一体化课程，为你打造沉浸式学习体验。你可以探索项目，交流分享，平台提供精彩的实战项目、高质量数据集，更有免费GPU计算资源和在线实训环境。你可以参加比赛，用实力证明自己。"
tags:
  - "clippings"
---
## PaddleOCR 官网 MCP 服务器说明文档

PaddleOCR 提供轻量级的 MCP 服务器，可用于将 PaddleOCR 的文本识别、文档解析等能力快速集成到各种大模型应用中。PaddleOCR MCP 服务器当前支持的工具如下：

- **当前支持的工具**
	- **OCR** ：对图像和 PDF 文件进行文本检测与识别。
		- **PP-StructureV3** ：从图像或 PDF 文件中识别和提取文本块、标题、段落、图片、表格以及其他版面元素，将输入转换为 Markdown 文档。
		- **PaddleOCR-VL** ：多模态高精度文档解析模型，对图像或 PDF 文件中的文本、表格、公式、图标等进行解析，将输入转换为 Markdown 文档。

PaddleOCR MCP 服务器可被多种应用集成，支持其文本识别与文档解析能力。这里以 Claude for Desktop 为例，以下为快速接入 PaddleOCR MCP 服务器的步骤：

1. 安装 [uv](https://docs.astral.sh/uv/#installation) 。
2. 在以下位置之一找到 Claude for Desktop 配置文件：
	打开 `claude_desktop_config.json` 文件，参考如下示例调整配置，填充到 `claude_desktop_config.json` 中。
	对于 PP-OCRv5 服务：
	```json
	{
	  "mcpServers": {
	    "PP-OCRv5": {
	      "command": "uvx",
	      "args": [
	        "--from",
	        "paddleocr-mcp",
	        "paddleocr_mcp"
	      "env": {
	        "PADDLEOCR_MCP_PIPELINE": "OCR",
	        "PADDLEOCR_MCP_PPOCR_SOURCE": "aistudio",
	        "PADDLEOCR_MCP_SERVER_URL": "<your url>",
	        "PADDLEOCR_MCP_AISTUDIO_ACCESS_TOKEN": "<your-access-token>"
	      }
	    }
	  }
	}
	```
	对于 PP-StructureV3 服务：
	```json
	{
	  "mcpServers": {
	    "PP-StructureV3": {
	      "command": "uvx",
	      "args": [
	        "--from",
	        "paddleocr-mcp",
	        "paddleocr_mcp"
	      ],
	      "env": {
	        "PADDLEOCR_MCP_PIPELINE": "PP-StructureV3",
	        "PADDLEOCR_MCP_PPOCR_SOURCE": "aistudio",
	        "PADDLEOCR_MCP_SERVER_URL": "<your url>",
	        "PADDLEOCR_MCP_AISTUDIO_ACCESS_TOKEN": "<your-access-token>"
	      }
	    }
	  }
	}
	```
	对于 PaddleOCR-VL 服务：
	```json
	{
	  "mcpServers": {
	    "PaddleOCR-VL": {
	      "command": "uvx",
	      "args": [
	        "--from",
	        "paddleocr-mcp",
	        "paddleocr_mcp"
	      ],
	      "env": {
	        "PADDLEOCR_MCP_PIPELINE": "PaddleOCR-VL",
	        "PADDLEOCR_MCP_PPOCR_SOURCE": "aistudio",
	        "PADDLEOCR_MCP_SERVER_URL": "<your url>",
	        "PADDLEOCR_MCP_AISTUDIO_ACCESS_TOKEN": "<your-access-token>"
	      }
	    }
	  }
	}
	```
	`PADDLEOCR_MCP_SERVER_URL` 值模型对应服务的基础URL(如https:/xxxxxx.aistudio-app.com)，同时在 [此页面](https://aistudio.baidu.com/index/accessToken) 获取您的 **访问令牌** 。
3. 重启 Claude for Desktop。新的 `paddleocr-ocr` 工具现在应该可以在应用中使用了。

除了上述使用方式外，PaddleOCR MCP 服务器还支持更多用法，例如接入本地 Python 库、使用 Streamable HTTP 传输等。关于 PaddleOCR MCP 服务器的更多能力，请参考 [PaddleOCR](https://www.paddleocr.ai/latest/version3.x/deployment/mcp_server.html) 官方文档。