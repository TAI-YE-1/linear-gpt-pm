# AI Builder Pack Maker

Local Python command-line tool for generating AI Builder assessment Markdown materials from a standard problem pack.

## Usage

```powershell
python run.py --input inputs/problem_pack.md --output-dir outputs
```

Generated files:

- `outputs/latest/one_page_summary.md`
- `outputs/latest/recording_script.md`
- `outputs/latest/defense_qa.md`
- `outputs/latest/materials_index.md`

## Verification

```powershell
python -m unittest discover -s tests -p "test_*.py"
npx --yes @fission-ai/openspec@1.4.1 validate add-ai-builder-pack-maker --strict
```

This first version is local-only and deterministic. It does not call model APIs, start a web server, use a database, or integrate with Feishu.
