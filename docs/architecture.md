# Architecture

```text
case manifest
    |
    v
diagnose() -> Diagnosis JSON -> route() -> strategy JSON
    |                                |
    +-----------------------------> repair()
                                      |
                                      v
                             visual/rule QA -> PASS/FAIL
                                      |
                               reflection + retry
```

The seam between deterministic fixture metadata and a real vision model is `diagnose()`. The seam between a strategy and an editing backend is `repair()`. This makes it possible to replace one component without collapsing diagnosis, execution, and QA into a single prompt.

Every run stores the case manifest, diagnosis, route, output filenames, QA thresholds, and evidence class. Missing real-model credentials or weights fail closed in the status report rather than silently falling back to a production claim.
