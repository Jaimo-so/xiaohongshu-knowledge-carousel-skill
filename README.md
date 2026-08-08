# 小红书知识轮播制作 Skill

[![Validate Skill](https://github.com/Jaimo-so/xiaohongshu-knowledge-carousel-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/Jaimo-so/xiaohongshu-knowledge-carousel-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

把一个知识主题、文章、课程笔记或已有内容方案，制作成一套可以直接发布的小红书教学轮播图。

这个 Skill 解决的不是单纯“生成几张好看的图”，而是同时保证：

- 定义、意义、机制、步骤、边界、失败条件与核验要求不被删减；
- 固定人物、服装、道具、配色与印刷质感在整套图片中保持一致；
- 视觉生成与确定性中文排版在同一次最终渲染中完成，不单独生成或审阅无字底图；
- 第一张可展示的图片就是带完整文字的最终效果图，交付目录只出现编号后的最终 PNG；
- 每页在手机上可读，并能通过脚本检查尺寸、页数与文件命名。

## 图片演示

下面两张图锁定整个系列的颜色层级：封面固定使用复古蓝满版底色，所有正文页固定使用旧纸黄色满版底色。

<table>
  <tr>
    <td><img src="docs/images/01-cover-final.png" alt="RAG 封面" width="360"></td>
    <td><img src="docs/images/02-definition-final.png" alt="RAG 定义" width="360"></td>
  </tr>
</table>

## 它怎样工作

```mermaid
flowchart LR
    A[提取全部知识点] --> B[逐页覆盖矩阵]
    B --> C[锁定角色与视觉系统]
    C --> D[直接生成并排版最终效果图]
    D --> E[逐页文字与视觉检查]
    E --> F[仅交付 final PNG]
```

核心原则是：用增加页面解决信息密度，而不是把定义和意义压缩掉；用单次最终渲染直接交付完整页面，不设置无字底图环节。

## 安装

### 方法一：让 Codex 安装

把下面这句话发送给 Codex：

```text
使用 $skill-installer 从 https://github.com/Jaimo-so/xiaohongshu-knowledge-carousel-skill 安装 create-xiaohongshu-knowledge-carousel。
```

安装后重启 Codex，或开始一个新任务，让 Skill 出现在可用 Skills 列表中。

### 方法二：克隆并运行安装脚本

macOS 或 Linux：

```bash
git clone https://github.com/Jaimo-so/xiaohongshu-knowledge-carousel-skill.git
cd xiaohongshu-knowledge-carousel-skill
bash install.sh
```

脚本会把 Skill 复制到：

```text
${CODEX_HOME:-$HOME/.codex}/skills/create-xiaohongshu-knowledge-carousel
```

### 方法三：手动安装

把下面这个目录完整复制到 Codex Skills 目录：

```text
skill/create-xiaohongshu-knowledge-carousel
```

目标位置：

- macOS / Linux：`~/.codex/skills/create-xiaohongshu-knowledge-carousel`
- Windows：`%USERPROFILE%\.codex\skills\create-xiaohongshu-knowledge-carousel`

Windows PowerShell 示例：

```powershell
git clone https://github.com/Jaimo-so/xiaohongshu-knowledge-carousel-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Copy-Item -Recurse -Force ".\xiaohongshu-knowledge-carousel-skill\skill\create-xiaohongshu-knowledge-carousel" "$env:USERPROFILE\.codex\skills\"
```

## 使用方法

直接点名 Skill，并提供主题或源材料：

```text
使用 $create-xiaohongshu-knowledge-carousel，把「RAG 是什么」制作成一套小红书知识轮播。保留全部定义、机制和限制，只展示最终效果图。
```

也可以提供文章、课程笔记、访谈整理或已有图片作为输入：

```text
使用 $create-xiaohongshu-knowledge-carousel，把这篇文章制作成教学轮播。先建立完整知识覆盖矩阵，页数由内容密度决定，不要删除定义和意义。
```

## Skill 包含什么

```text
skill/create-xiaohongshu-knowledge-carousel/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── manifest.example.json
│   ├── style-anchor-cover.png
│   └── style-anchor-interior.png
├── references/
│   ├── content-integrity.md
│   ├── rag-eight-page-example.md
│   └── visual-system.md
└── scripts/
    ├── typeset_carousel.py
    └── verify_deliverables.py
```

- `SKILL.md`：完整制作流程、操作顺序与交付规则。
- `content-integrity.md`：防止定义、意义、边界和核验要求在总结中消失。
- `visual-system.md`：角色、服装、配色、构图、提示词和视觉语义规范。
- `rag-eight-page-example.md`：未删减的 RAG 八页知识示例。
- `typeset_carousel.py`：根据 JSON 清单进行可靠中文排版。
- `verify_deliverables.py`：检查最终目录是否只含规范 PNG。

## 排版脚本

依赖 Python 3.10+ 和 Pillow：

```bash
python -m pip install Pillow
```

复制并修改示例清单：

```bash
cp skill/create-xiaohongshu-knowledge-carousel/assets/manifest.example.json ./manifest.json
```

生成最终图片：

```bash
python skill/create-xiaohongshu-knowledge-carousel/scripts/typeset_carousel.py ./manifest.json --output-dir ./final
```

验证最终交付目录：

```bash
python skill/create-xiaohongshu-knowledge-carousel/scripts/verify_deliverables.py ./final --expected-count 8
```

示例清单默认使用 macOS 系统中文字体。Windows 或 Linux 用户需要把 `fonts` 中的字体路径替换为本机可用的中文字体。

## 默认视觉系统

- 画布：1080 × 1440，3:4 竖版。
- 封面底色：固定复古蓝 `#287F98`。
- 正文页底色：固定旧纸黄色 `#EFE4CC`，不轮换其他满版底色。
- 正文信息框：统一复古蓝；正文用旧纸米色；重点提示用芥末黄。
- 辅助色：炭黑用于文字与描边；橙红只用于极少量标记，禁止作为正文页满版背景。
- 媒介：复古出版物拼贴、软胶人物、纸张颗粒、磨损边缘和轻微套印偏移。
- 固定人物：原创角色 Jaimo。
- 排版：顶部标题区、中央叙事插画、底部解释区、固定四角标识。

这些默认设置都可以替换成你的个人 IP、品牌色和栏目系统；知识完整性与最终交付规则保持不变。

## 适合的内容

- AI、产品、技术与商业概念解释；
- 课程笔记、方法论与流程拆解；
- 文章、报告与内部知识库内容可视化；
- 需要固定个人 IP 或栏目风格的系列内容；
- 对中文准确性和知识边界要求较高的教育内容。

## 注意事项

- 图像生成能力取决于当前 Codex 环境提供的图像工具。
- 不要让图像模型直接生成大段中文；应使用清单和排版脚本。
- 如果一页放不下完整定义，应增加页面，不应删除知识点。
- 发布前仍需人工核对重要事实、来源、版权、隐私和权限。

## License

[MIT](LICENSE)
