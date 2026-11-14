# Strongest_AI_Py

A hands-on Python and PyTorch repository where I build and test core AI system mechanics from scratch—without hiding behind high-level agent frameworks.

The focus here is practical: getting tool-calling, input sanitization, hardware-constrained inference, and C++/CUDA extensions working cleanly on local hardware before wiring them into larger enterprise workflows.

> **Note on scope:** Proprietary client work (ERP integrations, production APIs, and internal business agents) cannot be shared publicly. This repo is my open sandbox for testing the underlying mechanics, failure modes, and guardrails.

---

## What's in This Repo

| Directory / File | What It Does |
| :--- | :--- |
| `tiny_llm_agent.py` | From-scratch PyTorch character-level RNN (`TinyLLM`) + deterministic tool controller (`MinimalAgent`) |
| `LLM_Agent_In_Action/` | Iterative experiments on token-level action emission and regex-based tool dispatch |
| `Image_diffuser/` | Local `sd-turbo` inference tuned for CPU/32GB RAM with a two-layer safety gate (`image_generator_1.py`, `Hugging_face_safety_check.py`) |
| `NumPy_In_Action/` | Custom PyTorch C++ / C / CUDA extensions (`clip_scale.cpp`) wrapped as an `nn.Module` |
| `Resume_Generation_Parser/` | Programmatic `.docx` document generation (`python-docx`) and parsing experiments |

---

## Architecture & How the Workflows Run

### 1. From-Scratch Tool-Calling Agent (`tiny_llm_agent.py`)
Instead of importing an agent SDK, I trained a small PyTorch RNN (`Embedding -> RNN -> Linear`) on synthetic query-action pairs to see how reliably a lightweight model can emit structured tool commands:

1. **Inference & Decoding:** A user query is encoded character-by-character and passed through `TinyLLM` using greedy decoding until the stop delimiter (`|`) is hit.
2. **Structured Parsing:** `MinimalAgent` matches the output against `ACT:(\w+)\[(.*?)\]` and separates the intent from the runtime argument slot (`$`).
3. **Deterministic Dispatch:** `extract_expression()` pulls the math expression from the raw query, checks it against `TOOL_REGISTRY` (`calc`, `time`), runs the registered Python function, and returns the result.

### 2. Safety-Gated Local Diffusion (`Image_diffuser/image_generator_1.py`)
Designed to run `stabilityai/sd-turbo` predictably on CPU (`float32` with attention slicing enabled):

1. **Pre-Inference Gate:** `prompt_allowed()` tokenizes the prompt and rejects blocked terms before loading tensors into the pipeline.
2. **Generation:** Runs 1–4 inference steps (`guidance_scale=0.0`), clamping user-supplied step counts (`max(1, min(4, steps))`) and logging wall-clock generation time.
3. **Post-Inference Gate:** Runs `StableDiffusionSafetyChecker` (`CLIPVisionModel` cosine-distance check against 17 concept embeddings). If `nsfw_content_detected` triggers, the image is dropped in memory and never written to disk.

---

## Evals, Permissions & Error Handling

* **Runtime Checks:** `tiny_llm_agent.py` logs training loss every 10 epochs and runs `MinimalAgent` against both seen training phrases and unseen test queries in `__main__`.
* **Execution Boundaries:** Only functions explicitly registered in `TOOL_REGISTRY` can run. Unparseable model outputs (`(no tool)`) and unregistered tool names (`unknown tool`) fail closed without executing anything.
* **Graceful Failures:** `tool_calculate` wraps execution in `try/except` so bad syntax returns a structured error string instead of crashing the agent loop.

---

## Real Failures Turned Into Permanent Guardrails

1. **Unbounded `eval()` & Resource-Exhaustion Hangs**
   * **What broke:** Letting a model pass raw strings into `eval()` creates both code-injection risk and trivial CPU hangs (e.g., nested exponentiation like `9**9**9`).
   * **Permanent guardrail:** Locked `tool_calculate` behind a strict character allowlist (`0123456789+-*/(). `), explicitly blocked `**`, and capped expression length at 30 characters.

2. **Single-Layer Safety Gaps & CPU Memory Spikes**
   * **What broke:** Relying only on prompt keyword filtering misses visual edge cases, while running default `sd-turbo` settings on CPU triggers memory errors.
   * **Permanent guardrail:** Enforced a two-stage check (`prompt_allowed` before inference + `nsfw_content_detected` before disk write) and locked the pipeline to `float32` with attention slicing and explicit CPU thread allocation.

---

## Current State & What Remains for Production

This repo validates the core mechanics in isolation, not a multi-tenant production service. To take these patterns into a live enterprise environment, four pieces still need to be swapped in:

1. **AST-based math evaluation** (e.g., `ast.literal_eval` / custom AST walker) in place of sanitized `eval()`.
2. **Authenticated external connectors** (webhooks, ERP/CRM APIs) with idempotency keys, retries with backoff, and role-based tool permissions.
3. **Structured observability** (JSON trace logs, per-run latency/token metrics, and OpenTelemetry spans) instead of stdout prints.
4. **CI regression evals** over a versioned golden dataset of edge cases before any prompt or model weight change ships.
