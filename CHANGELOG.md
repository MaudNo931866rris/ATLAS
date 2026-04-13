# Changelog

## Unreleased

### Documentation
- Added multilingual documentation: Simplified Chinese (zh-CN), Japanese (ja), Korean (ko) for README, SETUP, and TROUBLESHOOTING
- Added language selector badges to README
- Added star history chart to Latest News section
- Rewrote README contributing section to encourage issue reports and community feedback
- Fixed V3_1_STATUS.md false claims about speed optimizations that were never applied to code

### Code Accuracy Audit
- Audited and corrected comments across 72 files for V3.0.1 accuracy
- Updated model references: Qwen3-14B to Qwen3.5-9B, embedding dimensions 5120 to 4096
- Renamed service references: rag-api to geometric-lens, Fox to llama-server
- Corrected G(x) XGBoost status: deployed and active (was incorrectly described as removed)
- Fixed normalization comments from "Fox 9B" to "Qwen3.5-9B C(x)"
- Marked legacy Fox code paths as unused in benchmark runner and geo_learning

### Test Fixes
- Fixed embedding dimensions in test fixtures (5120 to 4096)
- Fixed geometric-lens port in test conftest (8001 to 8099)
- Updated DivSampling test assertions to match actual 4+4+4 perturbation counts
- Corrected G(x) cost field parameter count: ~2.16M / 8.3MB (was ~2.7M / 10MB)

### Personal Notes
- Increased exploration budget threshold from 4 to 6 consecutive read-only calls before nudge (felt too aggressive for larger codebases)
- Raised write_file rejection threshold for existing files from 100 to 150 lines — the 100-line limit was refusing too many real files in projects I work with
- Lowered Best-of-K candidate count from 5 to 3 — generating 5 candidates was noticeably slow on my machine and 3 seemed sufficient for most edits

## [3.0.1] - 2026-04-05

### Tool-Call Agent Loop Architecture
- Replaced Aider format-translation proxy with structured JSON tool-call agent loop
- Grammar-constrained output via llama-server `response_format:json_object` — 100% valid JSON
- 8 tool definitions: `read_file`, `write_file`, `edit_file`, `delete_file`, `run_command`, `search_files`, `list_directory`, `plan_tasks`
- Per-file tier classification: T1 (config/data) writes directly, T2 (logic/features) routes through V3 pipeline
- 3400+ lines new Go code across 12 files in `atlas-proxy/`

### V3 Pipeline Integration
- All 14 V3 steps wired into `write_file`/`edit_file` executors for T2/T3 files
- PlanSearch → DivSampling → Budget Forcing → Build Verification → C(x)/G(x) Scoring → Best-of-K → S*/Blend-ASC → Failure Analysis → PR-CoT Repair → Refinement Loop → Derivation Chains → Metacognitive → Final Write
- Per-file-type build verification: tsc, py_compile, gcc, go build, cargo check, bash -n
- V3 service SSE streaming: pipeline progress visible in real-time

### CLI Experience
- `atlas` command: starts all services and launches Aider
- Streaming progress: `[Turn N/M]` with tool call details, V3 pipeline steps, completion summary
- Exploration budget: 4 consecutive read-only calls triggers nudge, prevents model from over-exploring
- Pre-injected project context: model sees project file list in system prompt
- File deletion via fast-path before tier classificat
