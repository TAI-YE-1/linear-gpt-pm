param(
    [Parameter(Mandatory = $true)]
    [string]$ChangeId,

    [string]$Goal,

    [string]$GoalFile,

    [string]$Constraints = "只修改当前需求明确要求的范围；不做无关重构；不引入不必要依赖；不修改生产配置。",

    [string]$ConstraintsFile,

    [string]$PromptDir = "docs\prompts",

    [string]$OutputPrefix = "current"
)

$ErrorActionPreference = "Stop"

try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {
    # Older PowerShell hosts may not allow changing output encoding. Ignore safely.
}

function Write-Info {
    param([string]$Message)
    Write-Host "[info] $Message"
}

function Write-Ok {
    param([string]$Message)
    Write-Host "[ok] $Message"
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[warn] $Message"
}

function Ensure-Directory {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Force $Path | Out-Null
        Write-Info "Created directory: $Path"
    }
}

function Read-RequiredUtf8File {
    param(
        [string]$Path,
        [string]$Label
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "$Label file not found: $Path"
    }

    $content = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
    if ([string]::IsNullOrWhiteSpace($content)) {
        throw "$Label file is empty: $Path"
    }

    return $content
}

function Write-TemplateIfMissing {
    param(
        [string]$Path,
        [string]$Content
    )

    if (-not (Test-Path $Path)) {
        $parent = Split-Path $Path -Parent
        if ($parent) {
            Ensure-Directory $parent
        }
        $Content | Set-Content -Encoding UTF8 $Path
        Write-Info "Created missing template: $Path"
    }
}

function Expand-Template {
    param(
        [string]$TemplatePath,
        [string]$OutputPath
    )

    if (-not (Test-Path $TemplatePath)) {
        throw "Template not found: $TemplatePath"
    }

    $content = Get-Content -Raw -Encoding UTF8 $TemplatePath

    $content = $content.Replace("<CHANGE_ID>", $ChangeId)
    $content = $content.Replace("<change-id>", $ChangeId)
    $content = $content.Replace("<在这里填写本次新功能或修复目标>", $Goal)
    $content = $content.Replace("<在这里填写限制条件，例如不接 API、不做网页、不改生产配置等>", $Constraints)

    $promptNames = @{
        "00_ROUTER" = "$OutputPrefix-00-router.md"
        "01_PROPOSE" = "$OutputPrefix-01-propose.md"
        "02_SUBAGENT_PLAN" = "$OutputPrefix-02-subagent-plan.md"
        "03_APPLY" = "$OutputPrefix-03-apply.md"
        "04_VERIFY" = "$OutputPrefix-04-verify.md"
        "05_REVIEW_ARCHIVE" = "$OutputPrefix-05-review-archive.md"
    }

    foreach ($key in $promptNames.Keys) {
        $fileName = $promptNames[$key]
        $content = $content.Replace("<PROMPT_$key>", $fileName)
        $content = $content.Replace("<PROMPT_PATH_$key>", "docs/prompts/$fileName")
    }

    $parent = Split-Path $OutputPath -Parent
    if ($parent) {
        Ensure-Directory $parent
    }

    $content | Set-Content -Encoding UTF8 $OutputPath
    Write-Ok "Generated $OutputPath"
}

if ($ChangeId -notmatch "^[a-z0-9]+(-[a-z0-9]+)*$") {
    throw "Invalid ChangeId: '$ChangeId'. Use lowercase kebab-case, for example: add-user-login or fix-deviation-time-baseline."
}

if ($OutputPrefix -notmatch "^[a-z0-9]+(-[a-z0-9]+)*$") {
    throw "Invalid OutputPrefix: '$OutputPrefix'. Use lowercase kebab-case without path separators, for example: current or sprint-01."
}

if ([string]::IsNullOrWhiteSpace($Goal) -and [string]::IsNullOrWhiteSpace($GoalFile)) {
    throw "Either -Goal or -GoalFile is required."
}

if (-not [string]::IsNullOrWhiteSpace($Goal) -and -not [string]::IsNullOrWhiteSpace($GoalFile)) {
    throw "Use either -Goal or -GoalFile, not both."
}

if (-not [string]::IsNullOrWhiteSpace($GoalFile)) {
    $Goal = Read-RequiredUtf8File -Path $GoalFile -Label "Goal"
}

if (-not [string]::IsNullOrWhiteSpace($ConstraintsFile)) {
    $Constraints = Read-RequiredUtf8File -Path $ConstraintsFile -Label "Constraints"
}

if ([string]::IsNullOrWhiteSpace($Constraints)) {
    throw "Constraints cannot be empty."
}

Ensure-Directory $PromptDir

$templateNames = @(
    "00-router.md",
    "01-propose.md",
    "02-subagent-plan.md",
    "03-apply.md",
    "04-verify.md",
    "05-review-archive.md"
)

foreach ($templateName in $templateNames) {
    $templatePath = Join-Path $PromptDir $templateName
    if (-not (Test-Path $templatePath)) {
        throw "Template not found: $templatePath. Run scripts\bootstrap-ai-sop.ps1 first, or restore docs\prompts templates."
    }
}

Expand-Template (Join-Path $PromptDir "00-router.md") (Join-Path $PromptDir "$OutputPrefix-00-router.md")
Expand-Template (Join-Path $PromptDir "01-propose.md") (Join-Path $PromptDir "$OutputPrefix-01-propose.md")
Expand-Template (Join-Path $PromptDir "02-subagent-plan.md") (Join-Path $PromptDir "$OutputPrefix-02-subagent-plan.md")
Expand-Template (Join-Path $PromptDir "03-apply.md") (Join-Path $PromptDir "$OutputPrefix-03-apply.md")
Expand-Template (Join-Path $PromptDir "04-verify.md") (Join-Path $PromptDir "$OutputPrefix-04-verify.md")
Expand-Template (Join-Path $PromptDir "05-review-archive.md") (Join-Path $PromptDir "$OutputPrefix-05-review-archive.md")

$index = @"
# Current AI Change Prompts

Change ID: $ChangeId

## Goal

$Goal

## Constraints

$Constraints

## Files

0. $OutputPrefix-00-router.md
1. $OutputPrefix-01-propose.md
2. $OutputPrefix-02-subagent-plan.md
3. $OutputPrefix-03-apply.md
4. $OutputPrefix-04-verify.md
5. $OutputPrefix-05-review-archive.md

## Suggested Codex Usage

请读取 docs/prompts/$OutputPrefix-00-router.md，并按里面的要求执行。

如果 Router 判断需要 OpenSpec change，再依次执行：

请读取 docs/prompts/$OutputPrefix-01-propose.md，并按里面的要求执行。

OpenSpec validate 通过后：

请读取 docs/prompts/$OutputPrefix-02-subagent-plan.md，并按里面的要求执行。

计划确认后：

请读取 docs/prompts/$OutputPrefix-03-apply.md，并按里面的要求执行。

实现完成后：

请读取 docs/prompts/$OutputPrefix-04-verify.md，并按里面的要求执行。

验证通过后：

请读取 docs/prompts/$OutputPrefix-05-review-archive.md，并按里面的要求执行。
"@

$indexPath = Join-Path $PromptDir "$OutputPrefix-README.md"
$index | Set-Content -Encoding UTF8 $indexPath
Write-Ok "Generated $indexPath"

Write-Host ""
Write-Ok "AI change prompt files generated."
Write-Host ""
Write-Host "Next command for Codex:"
Write-Host "请读取 docs/prompts/$OutputPrefix-00-router.md，并按里面的要求执行。"

