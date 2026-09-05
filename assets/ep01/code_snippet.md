```python
diagnosis = diagnose(case)
route = route(diagnosis.to_dict())
structured = repair(before, truth, mask, route["strategy"], attempt=2)
```

Evidence: `runs/EXP-A/case_00/`.
