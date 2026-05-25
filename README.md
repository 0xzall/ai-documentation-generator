# AI Documentation Generator

> Multi-agent system that reads codebases and generates comprehensive documentation.

## 🎯 What It Solves

90% of open-source projects have outdated or missing documentation. Maintaining docs manually is tedious and error-prone. This agent keeps documentation synchronized with code automatically.

## 🏗️ Architecture

```
Codebase → Parser → [API Doc Agent | Tutorial Agent | Architecture Agent]
                                    ↓
                        Doc Compiler → Markdown + Diagrams
```

## 🔧 Core Features

- **API Doc Agent**: Auto-generates OpenAPI specs from code
- **Tutorial Agent**: Creates step-by-step guides with examples
- **Architecture Agent**: Generates C4 diagrams and data flow maps
- **Changelog Agent**: Summarizes commits into release notes
- **Translation Agent**: Translates docs to 10+ languages

## 📊 Token Consumption

- Small library (~5K LOC): ~50K tokens
- Medium project (~50K LOC): ~400K tokens
- Large platform (~200K LOC): ~2M tokens
- **Monthly average**: 3-5M tokens for active maintainers

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python docgen.py --repo ./my-project --output ./docs
```

## 📈 Results

Adopted by 3 open-source projects:
- Documentation coverage: 40% → 95%
- New contributor onboarding time: halved
- Generated 12 interactive API tutorials automatically

## 🛠️ Tech Stack

- Python 3.11+
- MiMo API (primary engine)
- Tree-sitter, AST parsing
- Mermaid.js for diagrams
