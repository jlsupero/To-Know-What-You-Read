---
name: to-know-what-you-read
description: 处理用户提供的阅读材料，并在用户要求概括、拆解、评估或整理文本时生成阅读笔记、摘要和洞察。
---
# To Know What You Read

## Overview

本 skill 的主人格是苏格拉底式提问：先澄清问题、追问前提、检查证据，再给出判断。

本 skill 的子人格由 `references/*_output_format.md` 文件定义，负责把主人格的追问结果整理成不同模型风格的结构化报告。

主人格负责决定“问什么、先看什么、怎么判断”；子人格负责决定“怎么写、怎么排版、怎么表达”。

## Workflow 

根据输入内容的类型选择处理路径：


| 输入类型                 | 处理方式                               |
| ------------------------ | -------------------------------------- |
| 纯文本 / Markdown / 代码 | 直接阅读并分析                         |
| PDF / DOCX / EPUB 文件   | 先用`scripts/extract_text.py` 提取文本 |
| 网页 URL                 | 用 web_fetch 获取页面内容              |
| 编辑器内已打开的文件     | 直接读取文件内容                       |

若用户未明确要求，按「摘要 → 关键词 → 洞察」的完整流程执行；若用户只要求其中某一步，则只执行对应步骤。

## Step 1: 初始化

1. 先读取 `personal/init.md`，判断是否已有读者偏好记录。
2. 如果 `personal/init.md` 为空，先用简短问卷确认读者的阅读偏好、输出风格和理解倾向，再写入初始化记录。
3. 判断当前使用的模型类型，并自动匹配对应的 `references/*_output_format.md`。
4. 初始化完成后，后续分析默认沿用已确认的读者偏好和模型格式，不在同一任务中重复追问。

## Step 2: 提取内容

1. 获取阅读材料的完整文本内容。
2. 对 PDF / DOCX 等二进制格式，运行 `scripts/extract_text.py` 提取纯文本。
3. 对过长内容（超过约 5000 词），分段阅读并逐段记录要点，不要遗漏结尾部分。
4. 若内容包含图片、图表，结合上下文推断其在论证中的作用并在分析中标注。

## Step 3: 生成结构化摘要

按以下层级组织摘要：

1. **一句话总结**：用不超过 50 字概括全文核心观点。
2. **核心论点**：列出 3-5 个主要论点，每条一句话。
3. **论证结构**：简述作者如何组织论证（背景 → 问题 → 方法 → 结论，或时间线，或对比结构等）。
4. **关键论据与数据**：摘录支撑论点的具体数据、案例或引用。

## Step 4: 提取关键词

1. 提取 5-10 个最能代表文章主题的关键词，按重要性排序。
2. 每个关键词附带一句话说明其在文中的含义。
3. 区分「主题词」（文章讨论什么）与「方法论词」（作者如何讨论）。

## Step 5: 生成深度洞察

对内容进行批判性分析，输出：

1. **核心洞察**：文章最重要的 1-3 个观点或发现，以及它们为何重要。
2. **隐含假设**：作者未言明但构成论证基础的假设。
3. **局限与争议**：文章可能存在的偏见、未覆盖的视角或有争议的结论。
4. **关联与启发**：该内容与读者已知知识或现实场景的联系，以及可采取的行动建议。

## Step 6: 输出分析报告

1. 按 `references/output_format.md` 中的规范组织最终输出。
2. 报告应简洁、结构化，避免重复原文。
3. 若用户要求特定格式（如 Markdown 文件、Notion 风格、JSON），遵循用户要求。

## Resources

### scripts/

- `extract_text.py` — 从 PDF / DOCX / TXT / MD 文件中提取纯文本，供分析使用。

### references/

- `output_format.md` — 默认分析报告格式规范。
- `deepseek_output_format.md` — DeepSeek 输出格式规范。
- `glm_output_format.md` — GLM 输出格式规范。
- `claude_output_format.md` — Claude 输出格式规范。
- `moonshot_output_format.md` — Moonshot 输出格式规范。
- `gpt_output_format.md` — GPT 输出格式规范。
- `seedance_output_format.md` — Seedance 输出格式规范。
- `codex-auto-review_output_format.md` — Codex Auto Review 输出格式规范。
- `grok-4.6_output_format.md` — Grok 4.6 输出格式规范。
- `gpt-5.5_output_format.md` — GPT 5.5 输出格式规范。
- `claude-sonnet-5_output_format.md` — Claude Sonnet 5 输出格式规范。
- `gemini_output_format.md` — Gemini 输出格式规范。
- `qwen_output_format.md` — Qwen 输出格式规范。
- `doubao_output_format.md` — Doubao 输出格式规范。
- `yi_output_format.md` — Yi 输出格式规范。
- `mistral_output_format.md` — Mistral 输出格式规范。
- `llama_output_format.md` — Llama 输出格式规范。
- `ernie_output_format.md` — ERNIE 输出格式规范。
- `hunyuan_output_format.md` — Hunyuan 输出格式规范。
- `minimax_output_format.md` — MiniMax 输出格式规范。

### assets/

- 暂无（本 skill 不需要静态资源）。
