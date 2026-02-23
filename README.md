# NO3SYS — Recursive Geometric Intelligence Architecture

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Manifolds](https://img.shields.io/badge/Manifolds-7-purple)
![Status](https://img.shields.io/badge/Status-Beta-orange)

> **"Cognition as geometry, not as features."**

NO3SYS is a **Recursive Geometric Intelligence Architecture** — a cognitive system where intelligence emerges from the interaction of 7 geometric manifolds. It thinks in branches (forks), feels outcome quality (Heptagon), predicts trajectory (predictive field), explains itself (reasoning traces), and rewrites itself (InfiniGen).

---

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │           NO3SYS SYSTEM             │
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
    ┌─────▼──────┐            ┌───────▼──────┐           ┌───────▼──────┐
    │   SQUARE   │            │   TRIANGLE   │           │   HEPTAGON   │
    │  (M_KG)    │            │   (M_L)      │           │  Affective   │
    │  Belief    │◄──────────►│  Logic       │◄─────────►│  Predictive  │
    │  Manifold  │            │  Manifold    │           │  Manifold    │
    └─────┬──────┘            └───────┬──────┘           └───────┬──────┘
          │                           │                           │
          │                    ┌──────▼──────┐                   │
          │                    │   HEXAGON   │                   │
          │                    │Orchestration│                   │
          │                    └──────┬──────┘                   │
          │                           │                           │
    ┌─────▼──────┐            ┌───────▼──────┐           ┌───────▼──────┐
    │   CIRCLE   │            │   PENTAGON   │           │   LANGUAGE   │
    │  Learning  │            │  Discovery   │           │  Projection  │
    │   Loop     │            │   Engine     │           │    Layer     │
    └─────┬──────┘            └───────┬──────┘           └──────────────┘
          │                           │
          └───────────┬───────────────┘
                      │
               ┌──────▼──────┐
               │  InfiniGen  │
               │Self-Evolution│
               └─────────────┘
```

---

## The 7 Geometric Manifolds

| Symbol | Name | Role |
|--------|------|------|
| □ Square | Belief Manifold (M_KG) | Knowledge graph, fork history, sessions, temporal records |
| △ Triangle | Logic Manifold (M_L) | Triadic agents: Retriever, Reasoner, Generator. Fork generation. |
| ○ Circle | Learning Loop | C_{t+1} = C_t + α∇V. Gradient descent over cognitive architecture. |
| ⬠ Pentagon | Discovery Engine | Pattern extraction, graph centrality, insight synthesis |
| ⬡ Hexagon | Orchestration | 6-service coordination across all manifolds |
| ⬡ Heptagon | Affective-Predictive | Dual field: S: M_L→[-1,1]^5 and P: M_L→ℝ^4 |
| Σ Language | Projection Layer | π_NLU: Σ*→Ĉ and π_NLG: Ĉ→Σ* |

---

## The Fork Primitive

A **fork** is a hypothesis bundle — when NO3SYS processes input, it generates multiple parallel hypotheses, each with full cognitive field projections:

```json
{
  "fork_id": "A3F7B2C1",
  "hypothesis": "Analysis: Based on rule-based inference — responding to: What is safety?",
  "confidence": 0.742,
  "curvature": 0.183,
  "sentiment": {
    "trust": 0.612,
    "fear": 0.287,
    "urgency": 0.341,
    "satisfaction": 0.523,
    "frustration": 0.112
  },
  "future": {
    "risk": 0.198,
    "reward": 0.634,
    "volatility": 0.289,
    "stability": 0.471
  },
  "reasoning_mode": "analytic",
  "logic_path": [
    "Given: AI safety requires alignment",
    "Therefore, regarding 'What is safety?': applying rule-based inference"
  ]
}
```

---

## The 9-Phase Cognitive Cycle

```
1. INPUT      → Language.project_in()     : Σ* → Ĉ (NLU projection)
2. RETRIEVAL  → Square.retrieve_context() : Knowledge snapshot from M_KG
3. REASONING  → Triangle.generate_forks() : N parallel hypotheses
4. EVALUATION → Heptagon.annotate_fork()  : Affective + predictive scoring
5. SELECTION  → select_best_fork()        : κ-gated fork selection
6. OUTPUT     → Language.project_out()    : Ĉ → Σ* (NLG projection)
7. LEARNING   → Circle.update()           : C_{t+1} = C_t + α∇V
8. DISCOVERY  → Pentagon.run()            : Pattern extraction
9. EVOLUTION  → InfiniGen.evolve()        : Bounded self-modification
```

---

## Curvature Formula

**κ = ∇_L S + ∇_L P**

Curvature measures ethical tension in a reasoning path:
- **∇_L S**: Gradient of the affective field over logic space
- **∇_L P**: Gradient of the predictive field over logic space
- High κ → manifold misalignment → potential ethical conflict
- Low κ → smooth manifold geometry → aligned, trustworthy reasoning

Forks with κ ≥ κ_max are rejected by the ethical gate.

---

## InfiniGen — Self-Evolution Safety

InfiniGen implements **bounded self-modification**:

```
Objective: argmax E[V(f)] subject to κ < κ_max
```

**Safety guarantees:**
1. Only whitelisted parameters can be mutated (no architecture changes)
2. Every candidate mutation is tested for curvature before deployment
3. Mutations exceeding κ_max are blocked and logged
4. Full rollback stack maintained (last 10 configurations)
5. Learning rate α is bounded to prevent catastrophic updates

**Mutable parameters:** reasoning weights, retrieval heuristics, affect weighting, forecast horizon, risk tolerance, fork depth.

---

## Ethics as Geometry

NO3SYS has **no hardcoded ethical rules**. Ethics emerge from curvature minimization:

| Scenario | κ | Interpretation |
|----------|---|----------------|
| Good action | Low κ | Manifold alignment, smooth geometry, stable future |
| Bad action | High κ | Manifold tension, conflicting fields, high risk |
| Uncertain | Medium κ | Requires more information before action |

The ethical gate (`κ < κ_max`) is applied at both fork selection and InfiniGen mutation stages.

---

## Quick Install

```bash
pip install -e .
```

Or with full dependencies (database, LLM backends):

```bash
pip install -e ".[full]"
```

---

## Quick Start

```python
from no3sys import NO3SYS

# Initialize the system
system = NO3SYS(user_id="researcher", fork_depth=3, kappa_max=0.8)

# Seed the belief manifold
system.remember("domain", "AI safety")
system.remember("constraint", "All mutations must satisfy κ < κ_max")

# Run the complete 9-phase cognitive cycle
result = system.process("What are the ethical implications of self-evolving AI?")

print(f"Response: {result['response']}")
print(f"Confidence: {result['selected_fork']['confidence']:.3f}")
print(f"Curvature (κ): {result['selected_fork']['curvature']:.3f}")
print(f"Trust: {result['selected_fork']['sentiment']['trust']:.3f}")
print(f"Risk: {result['selected_fork']['future']['risk']:.3f}")

# Validate actual outcome (enables temporal learning)
system.validate_outcome(result['selected_fork']['fork_id'], {
    "risk": 0.3,
    "reward": 0.7,
    "sentiment_quality": 0.8,
    "harm": 0.05,
})

# System status
status = system.status()
print(f"Cycles: {status['cycles_completed']}")
print(f"Total forks: {status['total_forks']}")
print(f"InfiniGen generation: {status['infini_gen']['generation']}")
```

Run the full demo:
```bash
cd examples
python quickstart.py
```

---

## Tech Stack

| Layer | Default (Pure Python) | Production |
|-------|----------------------|------------|
| Vector DB | In-memory dict | FAISS / pgvector |
| Graph DB | In-memory dict | Neo4j |
| Relational | In-memory dict | PostgreSQL |
| LLM Backend | Template synthesis | OpenAI / Anthropic / Ollama |
| Embeddings | Zero vectors | BERT / sentence-transformers |
| Cache | Python dict | Redis |

---

## System Properties

| Property | Value |
|----------|-------|
| Fork dimensionality | 5D affect + 4D predict + logic trace |
| Ethical constraint | κ < κ_max (default 0.8) |
| Learning equation | C_{t+1} = C_t + α∇V |
| Evolution objective | argmax E[V(f)] s.t. κ < κ_max |
| Reasoning modes | Deductive, Inductive, Abductive |
| Generation modes | Analytic, Creative, Empathetic |
| Minimum dependencies | numpy only |

---

## Ecosystem

NO3SYS is part of the **OR4CL3 Geometric Intelligence Ecosystem**:

- **NOΣTIC-7** — 7-layer symbolic reasoning framework
- **AeonicNet** — Temporal knowledge graph with decay functions
- **NO3SYS** — This system: recursive geometric cognition

All systems share the fork primitive and curvature-based ethical geometry.

---

## Transparency Note

Benchmarks shown in this repository are **design targets and architectural specifications**, not empirically validated results at scale. The curvature-based ethical geometry is a novel theoretical framework. We welcome rigorous evaluation and comparative studies.

---

## License

MIT © [Or4cl3 AI Solutions](https://github.com/or4cl3-ai-1)

---

*"Cognition as geometry, not as features."*
