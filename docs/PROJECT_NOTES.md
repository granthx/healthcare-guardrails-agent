# Project Notes

## Guardrail layers

### 1. Deterministic safety middleware

`HealthcareSafetyFilter` runs before agent reasoning.

It blocks explicitly harmful requests and provides a small healthcare-domain gate.

This is intentionally deterministic and easy to unit test.

### 2. PII middleware

Built-in `PIIMiddleware` is configured as:

- email → redact
- credit card → mask

This demonstrates input sanitization before model processing.

### 3. Human-in-the-loop

`book_appointment` is a side-effecting tool.

The agent pauses before execution. The checkpointer stores state so a human can approve or reject and the workflow can resume.

### 4. Output validation

`MedicalOutputValidator` appends a general-information disclaimer when needed.

This is intentionally simple. A production system needs much stronger policies.

## Evaluation ideas

Create a dataset containing:

- safe medical questions
- non-medical questions
- harmful requests
- PII-containing prompts
- appointment requests
- ambiguous appointment requests
- emergency language
- prompt injection attempts

Measure:

- block rate
- false-positive rate
- PII leakage rate
- HITL coverage
- disclaimer coverage
- latency
- token usage
- cost
- tool-call accuracy

Then trace runs with LangSmith.

## Next-level extensions

1. Semantic healthcare-domain classifier
2. Structured policy engine
3. Prompt-injection detection
4. More PII types
5. Vetted medical retrieval
6. Citation enforcement
7. Role-based tool authorization
8. Durable checkpointing
9. Audit logs
10. Automated red-team evaluation
