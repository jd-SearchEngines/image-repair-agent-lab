```python
q1 = qa(before, repair_v1, truth, mask)
if q1["status"] == "FAIL":
    repair_v2 = repair(repair_v1, truth, mask, strategy, attempt=2)
```

Evidence: `runs/EXP-C/case_00/`.
