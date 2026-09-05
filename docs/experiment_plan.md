# Experiment plan

| ID | Cases | Treatment | Primary observation |
|---|---:|---|---|
| A | 5 | broad baseline vs routed structured repair | local scope and preserve score |
| B | 3 | full regenerate vs local repair | unnecessary changes outside mask |
| C | 3 | first pass, QA, reflection, second pass | bounded retry value |
| D | 20 | classify and route a small batch | route distribution and attempts |

The local run is a simulator-only gate. A real-model phase must add model identifier, weight/API provenance, runtime, seed, cost, raw response, and human blind review before making quality claims.
