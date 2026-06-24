import re
from pathlib import Path


OUTPUT_FILENAMES = (
    "one_page_summary.md",
    "recording_script.md",
    "defense_qa.md",
    "materials_index.md",
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def load_problem_pack(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Input file is empty: {path}")
    return text


def extract_sections(text: str) -> dict[str, str]:
    sections = {"_full_text": text}
    matches = list(HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


def _section(sections: dict[str, str], title: str, fallback: str = "未在输入材料中单独提供。") -> str:
    value = sections.get(title, "").strip()
    if value:
        return value
    return sections.get("_full_text", "").strip() or fallback


def _bulletize(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "- 未在输入材料中单独提供。"
    return "\n".join(line if line.startswith("- ") else f"- {line}" for line in lines[:8])


def render_one_page_summary(sections: dict[str, str]) -> str:
    return "\n".join(
        [
            "# AI Builder 考核材料一页纸",
            "",
            "## 项目背景",
            _section(sections, "项目背景"),
            "",
            "## 真实问题",
            _section(sections, "真实问题"),
            "",
            "## 解决方案",
            _section(sections, "解决方案"),
            "",
            "## 交付结果",
            _section(sections, "交付结果"),
            "",
            "## 验证效果",
            _section(sections, "验证效果"),
            "",
            "## 可复用价值",
            _section(sections, "可复用价值"),
            "",
        ]
    )


def render_recording_script(sections: dict[str, str]) -> str:
    return "\n".join(
        [
            "# 三分钟录屏脚本",
            "",
            "## 0:00-0:30 背景与问题",
            _section(sections, "项目背景"),
            "",
            _section(sections, "真实问题"),
            "",
            "## 0:30-1:20 方案说明",
            _section(sections, "解决方案"),
            "",
            "## 1:20-2:20 执行过程与交付",
            _section(sections, "AI 执行过程"),
            "",
            _section(sections, "交付结果"),
            "",
            "## 2:20-3:00 验证与复用",
            _section(sections, "验证效果"),
            "",
            _section(sections, "可复用价值"),
            "",
        ]
    )


def render_defense_qa(sections: dict[str, str]) -> str:
    return "\n".join(
        [
            "# 答辩问答",
            "",
            "## Q1: 这个工具解决了什么问题？",
            _section(sections, "真实问题"),
            "",
            "## Q2: 第一版为什么只做本地 Markdown 生成？",
            "第一版聚焦确定性交付，避免模型 API、网页、数据库、飞书等扩展影响验收边界。",
            "",
            "## Q3: 如何证明结果有效？",
            _section(sections, "验证效果"),
            "",
            "## Q4: 交付物有哪些？",
            _bulletize(_section(sections, "交付结果")),
            "",
            "## Q5: 后续可以如何复用？",
            _section(sections, "可复用价值"),
            "",
        ]
    )


def render_materials_index(sections: dict[str, str]) -> str:
    return "\n".join(
        [
            "# 成果材料索引",
            "",
            "## 输入材料",
            "- `inputs/problem_pack.md`",
            "",
            "## 生成材料",
            "- `outputs/latest/one_page_summary.md`",
            "- `outputs/latest/recording_script.md`",
            "- `outputs/latest/defense_qa.md`",
            "- `outputs/latest/materials_index.md`",
            "",
            "## 证据材料",
            _bulletize(_section(sections, "成果素材")),
            "",
        ]
    )


def render_documents(text: str) -> dict[str, str]:
    sections = extract_sections(text)
    return {
        "one_page_summary.md": render_one_page_summary(sections),
        "recording_script.md": render_recording_script(sections),
        "defense_qa.md": render_defense_qa(sections),
        "materials_index.md": render_materials_index(sections),
    }


def write_documents(documents: dict[str, str], output_root: Path) -> list[Path]:
    latest_dir = output_root / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for filename in OUTPUT_FILENAMES:
        path = latest_dir / filename
        path.write_text(documents[filename].rstrip() + "\n", encoding="utf-8")
        written.append(path)
    return written


def generate_pack(input_path: Path, output_root: Path) -> list[Path]:
    text = load_problem_pack(input_path)
    return write_documents(render_documents(text), output_root)
