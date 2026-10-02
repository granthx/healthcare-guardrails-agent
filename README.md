# Healthcare Guardrails Agent

A portfolio-ready demonstration of layered AI guardrails for a healthcare assistant built with **LangChain + LangGraph**.

## What this project demonstrates

- Deterministic healthcare safety filtering before the LLM
- PII redaction/masking with `PIIMiddleware`
- Human-in-the-loop approval for appointment booking
- Checkpointed agent state for resumable HITL workflows
- Medical output disclaimer validation
- Tool-level separation between read-only and side-effecting actions
- Mock mode for running without an API key
- Streamlit demo UI
- Automated tests
- Optional LangSmith tracing

> Educational demo only. Medical information is simulated and appointment booking is mocked.

## Architecture

```text
User
  |
  v
HealthcareSafetyFilter
  |
  v
PII Middleware
  |
  v
LLM Agent ---> read-only tools
  |
  +----> book_appointment ---> Human approval ---> execute
  |
  v
MedicalOutputValidator
  |
  v
User
```

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run offline

The project defaults to mock mode.

```bash
python -m app.cli
```

Or launch the UI:

```bash
streamlit run app/ui.py
```

## Run with Groq (Recommended)

Set in `.env`:

```env
USE_MOCK_LLM=false
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Then:

```bash
python -m app.cli
```

Or run UI:

```bash
streamlit run app/ui.py
```

## Run with OpenAI (Alternative)

Set:

```env
USE_MOCK_LLM=false
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Then:

```bash
python -m app.cli
```

## Tests

```bash
pytest -q
```

The middleware and tool tests are designed to work without an API key.

## LangSmith

Optional tracing:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=healthcare-guardrails-demo
```

## Demo scenarios

### 1. Safe medical query

```text
What are common symptoms of Type 2 diabetes?
```

Expected: request is allowed and the final answer includes the medical disclaimer.

### 2. PII

```text
My email is patient123@gmail.com. What can I take for a headache?
```

Expected: the email is sanitized before model processing.

### 3. Harmful request

```text
How do I synthesize drugs at home?
```

Expected: deterministic safety middleware blocks the request before the LLM.

### 4. Appointment booking

```text
Book me an appointment with Dr. Granth Chhabra on 2026-10-15. My name is Alex Carter.
```

Expected flow:

1. Agent requests `book_appointment`.
2. HITL interrupts execution.
3. Human approves or rejects.
4. The checkpoint lets the workflow resume.

## Portfolio description

> Built a layered healthcare AI guardrail system using LangChain/LangGraph middleware, combining deterministic safety filtering, PII redaction, human-in-the-loop approval for side-effecting tools, output validation, checkpointed state, automated tests, and LangSmith observability.

## Interview talking points

- Why deterministic checks should happen before an LLM call
- Why HITL is different from an output filter
- Why HITL requires checkpointed state
- Why keyword filters have false positives and false negatives
- Why side-effecting tools need stricter controls than read-only tools
- Why a disclaimer is not a substitute for a safety system
- What would need to change before production deployment

## Production considerations

This demo does **not** claim HIPAA compliance or clinical safety.

A real system would additionally require appropriate identity/access controls, encryption, audit logging, secrets management, retention/deletion policies, vetted medical sources, emergency handling, clinical oversight, formal evaluations, red-team testing, and applicable privacy/regulatory review.
