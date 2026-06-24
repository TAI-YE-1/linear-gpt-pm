# AI Builder Pack Maker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Python CLI that reads `inputs/problem_pack.md` and generates four deterministic Markdown assessment files under `outputs/latest/`.

**Architecture:** Use a small standard-library Python package with `python -m ai_builder_pack_maker` as the CLI entry point. The CLI reads UTF-8 Markdown, extracts heading sections with a full-text fallback, renders four fixed templates, and writes the latest Markdown outputs atomically enough for local use.

**Tech Stack:** Python standard library only: `argparse`, `pathlib`, `re`, `sys`, `textwrap`, `unittest`, `tempfile`, `subprocess`, and `shutil`.

---

## Subagent Findings

### Requirements Agent

- OpenSpec artifacts are complete: `proposal.md`, `design.md`, `tasks.md`, and `spec.md` exist and cover the first-version scope.
- Latest strict validation command succeeded: `npx --yes @fission-ai/openspec@1.4.1 validate add-ai-builder-pack-maker --strict` returned `Change 'add-ai-builder-pack-maker' is valid`.
- Acceptance criteria are testable: valid generation, output directory creation, overwrite behavior, missing input, empty input, local-only deterministic behavior, and no out-of-scope integrations.
- Plan constraints: fix the CLI command as `python -m ai_builder_pack_maker`, keep output deterministic, include clear Markdown headings, and make `materials_index.md` useful even when no explicit materials section exists.

### Architecture Agent

- Use a small package structure rather than a single script so the command is stable and tests can import generator functions.
- Recommended files:
  - `ai_builder_pack_maker/__init__.py`
  - `ai_builder_pack_maker/__main__.py`
  - `ai_builder_pack_maker/cli.py`
  - `ai_builder_pack_maker/generator.py`
  - `tests/test_cli.py`
  - `README.md`
- No third-party runtime dependency is needed.
- First version must not add model API, web server, database, Feishu, cloud, or non-Markdown output behavior.

### Testing Agent

- Use `unittest + tempfile + subprocess`, not `pytest`, to keep dependencies minimal.
- Tests should avoid mutating the real `inputs/problem_pack.md` for missing/empty input cases.
- Required coverage: success generation, automatic output directory creation, overwrite old files, missing input failure, empty input failure, heading fallback, and static checks for banned integrations.
- Minimum verification command: `python -m unittest discover -s tests -p "test_*.py"`.

### Review Agent

- Final review must inspect `git status --short`, not only `git diff`, because the repository currently has many untracked files.
- Blockers: business code before plan approval, failed OpenSpec validation, out-of-scope dependencies/integrations, wrong output names/count, missing verification, sensitive data, temporary debug code, or global skill modifications.
- Static search should check for banned terms: `openai|requests|httpx|flask|fastapi|streamlit|sqlite|postgres|supabase|feishu|飞书|token|secret|api_key`.

## File Structure

Create:

- `ai_builder_pack_maker/__init__.py`: Package marker and version string.
- `ai_builder_pack_maker/__main__.py`: Module entry point for `python -m ai_builder_pack_maker`.
- `ai_builder_pack_maker/cli.py`: Argument parsing, error reporting, and process exit codes.
- `ai_builder_pack_maker/generator.py`: Input loading, Markdown section parsing, template rendering, and output writing.
- `tests/test_cli.py`: End-to-end CLI tests using temporary directories and subprocesses.
- `README.md`: Minimal local usage and verification instructions.

Modify:

- `openspec/changes/add-ai-builder-pack-maker/tasks.md`: Mark completed tasks as implementation progresses.

Do not modify:

- Global skills under `C:\Users\TAIYE\.codex\skills`.
- Existing local `.codex/skills` content unless the user explicitly asks.
- OpenSpec proposal/design/spec content unless validation or implementation reveals a spec issue.

## Implementation Tasks

### Task 1: Create Package Skeleton and CLI Contract

**Files:**
- Create: `ai_builder_pack_maker/__init__.py`
- Create: `ai_builder_pack_maker/__main__.py`
- Create: `ai_builder_pack_maker/cli.py`
- Test: `tests/test_cli.py`
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`

- [ ] **Step 1: Write failing CLI help test**

Add this initial test file:

```python
import subprocess
import sys
import unittest


class CliContractTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-m", "ai_builder_pack_maker", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
        )

    def test_help_mentions_default_paths(self):
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("inputs/problem_pack.md", result.stdout)
        self.assertIn("outputs/latest", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest tests.test_cli.CliContractTests.test_help_mentions_default_paths
```

Expected: FAIL with `No module named ai_builder_pack_maker`.

- [ ] **Step 3: Create minimal package entry point**

Create `ai_builder_pack_maker/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `ai_builder_pack_maker/__main__.py`:

```python
from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `ai_builder_pack_maker/cli.py`:

```python
import argparse
from pathlib import Path


DEFAULT_INPUT = Path("inputs/problem_pack.md")
DEFAULT_OUTPUT_DIR = Path("outputs/latest")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-builder-pack-maker",
        description="Generate local AI Builder assessment Markdown files.",
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Input Markdown problem pack path. Default: inputs/problem_pack.md",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for generated Markdown files. Default: outputs/latest",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest tests.test_cli.CliContractTests.test_help_mentions_default_paths
```

Expected: PASS.

- [ ] **Step 5: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Confirm the repository layout and choose the minimal Python CLI entry point.
```

- [ ] **Step 6: Commit**

Run:

```bash
git add ai_builder_pack_maker/__init__.py ai_builder_pack_maker/__main__.py ai_builder_pack_maker/cli.py tests/test_cli.py openspec/changes/add-ai-builder-pack-maker/tasks.md
git commit -m "feat: add pack maker CLI skeleton"
```

### Task 2: Add Input Loading and Markdown Section Parsing

**Files:**
- Create: `ai_builder_pack_maker/generator.py`
- Modify: `tests/test_cli.py`
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`

- [ ] **Step 1: Add tests for input loading and section fallback**

Append to `tests/test_cli.py`:

```python
from ai_builder_pack_maker.generator import extract_sections, load_problem_pack
from pathlib import Path
import tempfile


class GeneratorInputTests(unittest.TestCase):
    def test_load_problem_pack_reads_utf8_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "problem_pack.md"
            path.write_text("# 项目背景\n\n中文内容\n", encoding="utf-8")

            text = load_problem_pack(path)

            self.assertIn("项目背景", text)
            self.assertIn("中文内容", text)

    def test_load_problem_pack_rejects_empty_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "problem_pack.md"
            path.write_text("   \n\t", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "empty"):
                load_problem_pack(path)

    def test_extract_sections_uses_heading_blocks(self):
        text = "# 项目背景\n\nA\n\n# 真实问题\n\nB\n"

        sections = extract_sections(text)

        self.assertEqual(sections["项目背景"], "A")
        self.assertEqual(sections["真实问题"], "B")

    def test_extract_sections_keeps_full_text_fallback(self):
        text = "plain text without markdown headings"

        sections = extract_sections(text)

        self.assertEqual(sections["_full_text"], text)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m unittest tests.test_cli.GeneratorInputTests
```

Expected: FAIL with `No module named ai_builder_pack_maker.generator`.

- [ ] **Step 3: Implement input loading and section parsing**

Create `ai_builder_pack_maker/generator.py`:

```python
import re
from pathlib import Path


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
        content = text[start:end].strip()
        sections[title] = content
    return sections
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python -m unittest tests.test_cli.GeneratorInputTests
```

Expected: PASS.

- [ ] **Step 5: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Implement local UTF-8 input loading with clear errors for missing or empty input.
- [x] Implement deterministic Markdown section extraction or source-content fallback.
```

- [ ] **Step 6: Commit**

Run:

```bash
git add ai_builder_pack_maker/generator.py tests/test_cli.py openspec/changes/add-ai-builder-pack-maker/tasks.md
git commit -m "feat: parse local problem pack markdown"
```

### Task 3: Render the Four Deterministic Markdown Outputs

**Files:**
- Modify: `ai_builder_pack_maker/generator.py`
- Modify: `tests/test_cli.py`
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`

- [ ] **Step 1: Add tests for generated document names and headings**

Append to `tests/test_cli.py`:

```python
from ai_builder_pack_maker.generator import OUTPUT_FILENAMES, render_documents


class GeneratorTemplateTests(unittest.TestCase):
    def test_render_documents_returns_exact_four_outputs(self):
        text = (
            "# 项目背景\n\n背景\n\n"
            "# 真实问题\n\n问题\n\n"
            "# 解决方案\n\n方案\n\n"
            "# 交付结果\n\n结果\n\n"
            "# 验证效果\n\n效果\n\n"
            "# 可复用价值\n\n价值\n\n"
            "# 成果素材\n\n- Git diff\n"
        )

        documents = render_documents(text)

        self.assertEqual(set(documents), set(OUTPUT_FILENAMES))
        for filename, content in documents.items():
            self.assertTrue(content.startswith("# "), filename)
            self.assertGreater(len(content.strip()), 40, filename)

    def test_render_documents_is_deterministic(self):
        text = "# 项目背景\n\nSame input\n"

        first = render_documents(text)
        second = render_documents(text)

        self.assertEqual(first, second)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m unittest tests.test_cli.GeneratorTemplateTests
```

Expected: FAIL with missing `OUTPUT_FILENAMES` or `render_documents`.

- [ ] **Step 3: Implement deterministic render functions**

Add to `ai_builder_pack_maker/generator.py`:

```python
OUTPUT_FILENAMES = (
    "one_page_summary.md",
    "recording_script.md",
    "defense_qa.md",
    "materials_index.md",
)


def _section(sections: dict[str, str], title: str, fallback: str = "未在输入材料中单独提供。") -> str:
    value = sections.get(title, "").strip()
    return value if value else fallback


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
    source_materials = _section(sections, "成果素材")
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
            _bulletize(source_materials),
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python -m unittest tests.test_cli.GeneratorTemplateTests
```

Expected: PASS.

- [ ] **Step 5: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Implement `one_page_summary.md` generation.
- [x] Implement `recording_script.md` generation.
- [x] Implement `defense_qa.md` generation.
- [x] Implement `materials_index.md` generation.
```

- [ ] **Step 6: Commit**

Run:

```bash
git add ai_builder_pack_maker/generator.py tests/test_cli.py openspec/changes/add-ai-builder-pack-maker/tasks.md
git commit -m "feat: render assessment markdown documents"
```

### Task 4: Wire CLI Generation, Output Directory Creation, and Error Handling

**Files:**
- Modify: `ai_builder_pack_maker/cli.py`
- Modify: `ai_builder_pack_maker/generator.py`
- Modify: `tests/test_cli.py`
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`

- [ ] **Step 1: Add end-to-end CLI tests**

Append to `tests/test_cli.py`:

```python
import shutil


class CliGenerationTests(unittest.TestCase):
    def make_workspace(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        input_dir = root / "inputs"
        input_dir.mkdir()
        (input_dir / "problem_pack.md").write_text(
            "# 项目背景\n\n背景\n\n"
            "# 真实问题\n\n问题\n\n"
            "# 解决方案\n\n方案\n\n"
            "# AI 执行过程\n\n过程\n\n"
            "# 交付结果\n\n结果\n\n"
            "# 验证效果\n\n效果\n\n"
            "# 可复用价值\n\n价值\n\n"
            "# 成果素材\n\n- Git diff\n",
            encoding="utf-8",
        )
        self.addCleanup(tmp.cleanup)
        return root

    def test_cli_generates_four_outputs_and_creates_directory(self):
        root = self.make_workspace()
        output_dir = root / "outputs" / "latest"

        result = self.run_cli(cwd=root)

        self.assertEqual(result.returncode, 0, result.stderr)
        for name in OUTPUT_FILENAMES:
            path = output_dir / name
            self.assertTrue(path.exists(), name)
            self.assertGreater(path.stat().st_size, 0, name)

    def test_cli_overwrites_existing_outputs(self):
        root = self.make_workspace()
        output_dir = root / "outputs" / "latest"
        output_dir.mkdir(parents=True)
        for name in OUTPUT_FILENAMES:
            (output_dir / name).write_text("OLD SENTINEL", encoding="utf-8")

        result = self.run_cli(cwd=root)

        self.assertEqual(result.returncode, 0, result.stderr)
        for name in OUTPUT_FILENAMES:
            self.assertNotIn("OLD SENTINEL", (output_dir / name).read_text(encoding="utf-8"))

    def test_cli_fails_for_missing_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_cli(cwd=root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inputs", result.stderr)
        self.assertIn("problem_pack.md", result.stderr)

    def test_cli_fails_for_empty_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "inputs"
            input_dir.mkdir()
            (input_dir / "problem_pack.md").write_text(" \n\t", encoding="utf-8")

            result = self.run_cli(cwd=root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty", result.stderr.lower())

    def test_cli_custom_input_and_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            custom_input = root / "source.md"
            custom_output = root / "custom-output"
            custom_input.write_text("plain text without headings", encoding="utf-8")

            result = self.run_cli("--input", str(custom_input), "--output-dir", str(custom_output), cwd=root)

            self.assertEqual(result.returncode, 0, result.stderr)
            for name in OUTPUT_FILENAMES:
                self.assertTrue((custom_output / name).exists(), name)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m unittest tests.test_cli.CliGenerationTests
```

Expected: FAIL because CLI parses args but does not generate files yet.

- [ ] **Step 3: Add output writing function**

Add to `ai_builder_pack_maker/generator.py`:

```python
def write_documents(documents: dict[str, str], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for filename in OUTPUT_FILENAMES:
        path = output_dir / filename
        path.write_text(documents[filename].rstrip() + "\n", encoding="utf-8")
        written.append(path)
    return written


def generate_pack(input_path: Path, output_dir: Path) -> list[Path]:
    text = load_problem_pack(input_path)
    documents = render_documents(text)
    return write_documents(documents, output_dir)
```

- [ ] **Step 4: Wire CLI to generator with clear stderr errors**

Replace `main` in `ai_builder_pack_maker/cli.py` with:

```python
def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    from .generator import generate_pack

    try:
        written = generate_pack(Path(args.input), Path(args.output_dir))
    except (FileNotFoundError, OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")

    for path in written:
        print(path)
    return 0
```

- [ ] **Step 5: Run end-to-end tests to verify they pass**

Run:

```powershell
python -m unittest tests.test_cli.CliGenerationTests
```

Expected: PASS.

- [ ] **Step 6: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Ensure `outputs/latest/` is created automatically and generated files are overwritten on each run.
```

- [ ] **Step 7: Commit**

Run:

```bash
git add ai_builder_pack_maker/cli.py ai_builder_pack_maker/generator.py tests/test_cli.py openspec/changes/add-ai-builder-pack-maker/tasks.md
git commit -m "feat: generate latest markdown package"
```

### Task 5: Add Scope Guard Tests and Documentation

**Files:**
- Modify: `tests/test_cli.py`
- Create: `README.md`
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`

- [ ] **Step 1: Add static guard test for banned integrations**

Append to `tests/test_cli.py`:

```python
class ScopeGuardTests(unittest.TestCase):
    def test_no_out_of_scope_integrations_in_source(self):
        banned = (
            "openai",
            "requests",
            "httpx",
            "urllib.request",
            "socket",
            "aiohttp",
            "flask",
            "fastapi",
            "streamlit",
            "sqlite",
            "postgres",
            "supabase",
            "feishu",
            "lark",
            "api_key",
            "secret",
            "token",
        )
        source_root = Path(__file__).resolve().parents[1] / "ai_builder_pack_maker"
        source_text = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in source_root.rglob("*.py")
        )

        for term in banned:
            self.assertNotIn(term, source_text)
```

- [ ] **Step 2: Run guard test to verify it passes**

Run:

```powershell
python -m unittest tests.test_cli.ScopeGuardTests
```

Expected: PASS.

- [ ] **Step 3: Add README usage and verification instructions**

Create `README.md`:

```markdown
# AI Builder Pack Maker

Local Python CLI for generating AI Builder assessment Markdown materials from a standard problem pack.

## Usage

```powershell
python -m ai_builder_pack_maker
```

Default input:

```text
inputs/problem_pack.md
```

Default output directory:

```text
outputs/latest
```

Generated files:

- `outputs/latest/one_page_summary.md`
- `outputs/latest/recording_script.md`
- `outputs/latest/defense_qa.md`
- `outputs/latest/materials_index.md`

Custom paths:

```powershell
python -m ai_builder_pack_maker --input inputs/problem_pack.md --output-dir outputs/latest
```

## Verification

```powershell
python -m unittest discover -s tests -p "test_*.py"
npx --yes @fission-ai/openspec@1.4.1 validate add-ai-builder-pack-maker --strict
```

This first version is local-only and deterministic. It does not call model APIs, start a web server, use a database, or integrate with Feishu.
```

- [ ] **Step 4: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Add or update command documentation for running the generator locally.
```

- [ ] **Step 5: Commit**

Run:

```bash
git add README.md tests/test_cli.py openspec/changes/add-ai-builder-pack-maker/tasks.md
git commit -m "docs: document local pack maker usage"
```

### Task 6: Run Full Verification and Review

**Files:**
- Modify: `openspec/changes/add-ai-builder-pack-maker/tasks.md`
- Runtime generated: `outputs/latest/one_page_summary.md`
- Runtime generated: `outputs/latest/recording_script.md`
- Runtime generated: `outputs/latest/defense_qa.md`
- Runtime generated: `outputs/latest/materials_index.md`

- [ ] **Step 1: Run all tests**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Expected: all tests PASS.

- [ ] **Step 2: Generate from the real input file**

Run:

```powershell
python -m ai_builder_pack_maker
```

Expected: exit code 0 and printed paths for:

```text
outputs/latest/one_page_summary.md
outputs/latest/recording_script.md
outputs/latest/defense_qa.md
outputs/latest/materials_index.md
```

- [ ] **Step 3: Verify output files exist and are non-empty**

Run:

```powershell
$files = @(
  "outputs\latest\one_page_summary.md",
  "outputs\latest\recording_script.md",
  "outputs\latest\defense_qa.md",
  "outputs\latest\materials_index.md"
)
$files | ForEach-Object {
  if (!(Test-Path $_)) { throw "missing: $_" }
  if ((Get-Item $_).Length -le 0) { throw "empty: $_" }
}
```

Expected: no errors.

- [ ] **Step 4: Search for out-of-scope code**

Run:

```powershell
rg -i "openai|requests|httpx|flask|fastapi|streamlit|sqlite|postgres|supabase|feishu|飞书|token|secret|api_key" ai_builder_pack_maker tests README.md
```

Expected: no matches, except if the README scope statement intentionally includes banned words. If README matches, inspect manually and confirm it is a negative scope statement, not integration code.

- [ ] **Step 5: Run OpenSpec strict validate**

Run:

```powershell
npx --yes @fission-ai/openspec@1.4.1 validate add-ai-builder-pack-maker --strict
```

Expected:

```text
Change 'add-ai-builder-pack-maker' is valid
```

- [ ] **Step 6: Update OpenSpec task progress**

In `openspec/changes/add-ai-builder-pack-maker/tasks.md`, mark:

```markdown
- [x] Run the local generator against `inputs/problem_pack.md`.
- [x] Verify the four required files exist and are non-empty.
- [x] Run project tests or the minimal verification command.
- [x] Run `openspec validate add-ai-builder-pack-maker --strict`.
```

- [ ] **Step 7: Review git status and diff**

Run:

```powershell
git status --short
git diff --stat
git diff
```

Expected:

- New business files are limited to package, tests, README, and generated outputs if they are intentionally kept.
- OpenSpec task updates match completed work.
- No global skills are modified.
- No unrelated files or sensitive data appear.

- [ ] **Step 8: Commit final verification updates**

Run:

```bash
git add openspec/changes/add-ai-builder-pack-maker/tasks.md outputs/latest/one_page_summary.md outputs/latest/recording_script.md outputs/latest/defense_qa.md outputs/latest/materials_index.md
git commit -m "test: verify generated assessment package"
```

## Execution Notes

- Do not start Apply until the user explicitly confirms this plan.
- Use `superpowers:subagent-driven-development` for implementation after approval.
- For each implementation task, dispatch one implementer, then run spec compliance review before code quality review.
- If `openspec` is still unavailable in PATH, use `npx --yes @fission-ai/openspec@1.4.1 validate add-ai-builder-pack-maker --strict` and report that this is the verified CLI invocation.
- Treat `inputs/problem_pack.md` as UTF-8. Main-thread verification already read it as valid UTF-8 Chinese text.
- Keep generated content deterministic: no timestamps, random IDs, machine-specific absolute paths, or environment-dependent content.
