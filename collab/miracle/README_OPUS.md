Opus Workflow and Gemini Quickstart
=================================

This project includes a minimal Opus workflow (`opus_workflow.json`) that
demonstrates the Intake → Understand → Decide → Review → Deliver pattern
required for the hackathon Opus challenge. The workflow calls our backend
adapter endpoints that can optionally integrate with Gemini.

Quick steps to prototype with Gemini (Google AI Studio)
----------------------------------------------------
1. Open Google AI Studio (https://studio.google.ai) and experiment with a
   multimodal prompt for image understanding. Example prompt:

   "Describe the main imaging findings in plain language and return a JSON
   object with keys: finding, severity (low/medium/high), localization, confidence (0-1), rationale."

2. Once you have a stable prompt, copy it and set `GEMINI_API_KEY` and
   `GEMINI_API_URL` in the Render/GitHub Actions environment (or locally
   as env vars) so the backend adapter will call Gemini instead of the
   heuristic fallback.

Opus workflow notes
-------------------
- `intake` node: uploads the image.
- `ai_understand` node: calls `/ai/case-understand` on the backend. Returns
  structured fields.
- `qdrant_search` node: calls `/medical/analyze` to retrieve similar cases.
- `decision` node: simple code node that routes to human review when
  confidence or similarity thresholds are not met.
- `agentic_review` node: optional reranker or policy check (calls `/ai/rerank`).
- `human_review` node: human-in-the-loop step.
- `audit_and_deliver` node: generates a compact JSON audit artifact and
  writes the result to storage or Google Sheets.

Files added
-----------
- `collab/miracle/opus_workflow.json` — minimal Opus workflow.
- `collab/miracle/README_OPUS.md` — this file.

Next steps
----------
Pick one:
- Prototype prompts in Google AI Studio and set `GEMINI_API_KEY`.
- I can wire the real Gemini calls into the backend (requires API key).
- I can export a more complete Opus workflow with code node details and
  a runnable example using the Opus platform (I can prepare that next).
