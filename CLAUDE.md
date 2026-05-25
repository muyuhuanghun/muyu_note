claud# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This is an Obsidian vault containing personal study notes, primarily in Chinese with English technical terminology. It is version-controlled with Git.

## Directory structure

- `基于pytorch的深度学习/` — PyTorch deep learning course notes (the largest section, contains `.md` and `.canvas` files)
- `AI_CODING/` — AI-assisted coding tools and workflows
- `Github/` — GitHub guides (student pack, tokens, Copilot, Actions)
- `LLAMA.CPP/` — Running LLMs locally with llama.cpp
- `ANTHROPIC/`, `OPENAI_GPT_CODEX/` — Specific AI platform notes
- `线性代数/`, `微积分/` — Math fundamentals
- `服务器与VPS/`, `科学上网/` — Infrastructure and networking
- `.obsidian/` — Obsidian plugin/config files (do not hand-edit unless asked)

## File types

- `.md` — Markdown notes with standard Obsidian wikilinks (`[[page name]]`)
- `.canvas` — Obsidian Canvas visual notes (JSON format)
- `.png` — Embedded images, typically stored in topic subdirectories

## Git conventions

- Commit messages are in Chinese, describing the topic/content added
- Commit frequently after completing a section of notes
- Do not commit `.obsidian/workspace.json` or `.obsidian/graph.json` transient changes — only commit intentional config modifications
