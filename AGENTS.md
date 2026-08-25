claud# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository overview

This is an Obsidian vault containing personal study notes, primarily in Chinese with English technical terminology. It is version-controlled with Git and hosted on GitHub (muyuhuanghun/muyu_note). The repo is public — do not include sensitive information (credentials are excluded via .gitignore).

## User role

The user can approve and merge PRs from other collaborators on this repo.

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
- **Before every push**: review all changes for sensitive data leakage (credentials, tokens, API keys, personal info); update README.md to reflect current content
- **When approving/merging PRs**: perform the same leakage risk review on the PR's changes before merging

## Note writing style

Notes follow a **code-driven learning style** — the core is code blocks with concepts explained through inline comments, not lengthy prose.

### Key conventions

1. **Code as the body**: Notes center on code; concepts are explained via comments within code blocks
2. **Chinese with English terms**: Body text and comments in Chinese, keep technical terms (RNN, CrossEntropyLoss, embedding, etc.) in English
3. **Emoji markers**:
   - 📌 Key changes / critical points
   - 🚀 Initialization / startup related
   - 🌟 Core techniques / highlights
   - ⚠️ Pitfalls / warnings
   - 💡 Tips / supplementary notes
4. **Section dividers**: Use `# ==========================================` to separate functional modules
5. **Bug fix markers**: Format as `📌 修复 Bug X：`
6. **Progressive iteration**: Keep multiple versions of code in the same note (initial → improved → final) to show the optimization process
7. **Colloquial metaphors**: Use vivid analogies in comments (e.g. "expand memory to 16 dimensions", "learn to write love letters from gibberish")
8. **Canvas visualization**: Each chapter has a `.canvas` file showing knowledge relationships visually

### Chapter naming convention

- Two-digit number prefix: `01.`, `02.` ... `13.`
- Mixed Chinese-English titles: e.g. `01.overview_1.md`, `13.RNN Classifier.md`
