# Bad cases worth keeping

Bad cases are part of the evidence pack rather than being removed.

- `case_03` / `COMPOSITION`: the contrast-based composition route changes pixels beyond the declared narrow mask, so QA remains FAIL.
- `case_04` / `BACKGROUND`: the local route is intentionally too narrow for a full-width background issue; this shows why classification matters.
- `case_05` / `GLOBAL_FAILURE`: a global issue should not be evaluated with a local preservation assumption; the route is explicitly global.

See per-case `qa` and `routing` fields in the EXP-D manifest for machine-readable records.
