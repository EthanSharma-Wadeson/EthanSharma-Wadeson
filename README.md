# Hi, I'm Ethan Sharma-Wadeson

I build research infrastructure for quantitative and macro workflows.

Right now, my main project is the **Narrative Volatility Engine (NVE)** — a self-hosted system for measuring how financial narratives change over time.

---

## What NVE is

NVE is a **narrative telemetry observatory**.

It ingests text corpora (filings, macro context, news, earnings events, or client-provided datasets), converts them into embeddings, scores rolling narrative windows, and produces auditable findings and evidence exports.

Core focus:

- coherence and semantic drift tracking
- instability and instability-velocity monitoring
- temporal safeguards against look-ahead leakage
- local-first deployment with BYOK (Bring Your Own Key)

---

## Why I built it

Most research stacks measure price and volatility very well, but narrative change is often handled informally.

I built NVE to make narrative state measurable, reviewable, and reproducible:

- from ingestion to scoring
- from scoring to findings
- from findings to structured evidence packs

The goal is not hype or signal-selling; the goal is disciplined research telemetry.

---

## How I engineered it

I designed and implemented NVE as a modular Python system with:

- source adapters for SEC, RSS, macro, and earnings context
- a shared ingestion pipeline with timestamp validation/sanitization
- local persistence (SQLite + Chroma vector store)
- rolling-window Metrics v2 (coherence, drift, divergence, persistence, instability)
- CLI + API interfaces for repeatable workflows
- evidence export for technical and institutional review

---

## Project proof points

- ~21,368 lines of Python
- extensive automated tests (132 passing in latest full run)
- full CLI smoke matrix for operational command paths
- Dockerized local deployment model
- append-only findings archive and generated evidence packs

---

## Stack

- **Language:** Python
- **Interfaces:** Typer CLI, FastAPI
- **Storage:** SQLite, Chroma
- **Packaging:** Docker / docker-compose
- **Testing:** pytest
- **Data modes:** local fixtures + BYOK external sources

---

## What NVE is not

- not financial advice
- not a trading bot
- not a buy/sell recommendation engine
- not a black-box "AI predicts markets" product

NVE is an analytical research framework and information tool.

---

## Current direction

I am currently focused on:

- early-access architecture evaluations with research professionals
- hardening documentation for pilot onboarding
- keeping claims restrained and evidence-based
- expanding integration options for client-owned data feeds

---

## Open to connect

I enjoy speaking with:

- quant researchers
- macro and thematic analysts
- risk teams
- infrastructure engineers

If you care about rigorous systems, reproducibility, and local-first research tooling, feel free to connect.

