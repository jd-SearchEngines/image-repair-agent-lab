# Douyin Gamma Asset & QA Gates

## 1. Image Relevance Rubric

Score every candidate image before using it.

- **5/5 — Direct evidence:** The image directly proves the card claim. Examples: exact before/after pair, exact failing/passing test, exact code/Skill excerpt, exact metric chart from the experiment.
- **4/5 — Strong supporting evidence:** The image does not prove the whole claim alone but clearly illustrates the same object/process and materially improves understanding.
- **3/5 — Context only:** Related topic, but the reader could not infer the card claim from it. Do not use by default.
- **2/5 — Tangential:** Same broad domain, weak relation. Reject.
- **1/5 — Decorative:** Attractive but does not explain or prove the point. Reject unless the user explicitly wants decorative art.

**Hard gate:** only 4/5 or 5/5 images may be used as content visuals.

## 2. Provenance Gate

Every used image must have one of these provenance labels internally:

1. `PROJECT_RAW` — raw project asset, preferred.
2. `PROJECT_EVIDENCE` — code/log/test/metric screenshot from the project.
3. `OFFICIAL_EXTERNAL` — official docs/blog/paper illustration with clear source.
4. `REUSABLE_EXTERNAL` — public-domain or reusable external image with source.
5. `DECORATIVE` — non-evidence visual; normally reject.

Never use `OLD_PPT`, `OLD_GAMMA`, `CONTACT_SHEET`, or a previous card export as evidence unless the card is explicitly discussing that artifact.

## 3. Mandatory Asset Map

Before calling Gamma, create this map internally for every image candidate:

| Card | Candidate asset | Provenance | Claim supported | Reader should look at | Relevance | Use? |
|---|---|---|---|---|---:|---|
| 1 | ... | PROJECT_RAW | ... | ... | 5 | YES |

Generation is blocked until all `Use=YES` assets have provenance, claim relation, and reader focus completed.

## 4. Image/Card Integration Gate

For every image card, at least one of these must be present:

- explicit Before / After labels;
- crop or zoom to the important region;
- arrow / bounding box / highlight;
- one-line caption: “这张图证明：…”;
- one-line reading cue: “看这里：…”;
- code/log callout identifying the exact line/result;
- metric chart with a one-line interpretation.

If none applies, the image is probably decorative or detached; remove it.

## 5. Card Mix

Do not enforce one image per card.

For a default 6-card Douyin technical post, preferred mix:

- 1 Hook / hero evidence card;
- 1–2 direct evidence / before-after cards;
- 1 reasoning or mechanism card, often text-only or simple diagram;
- 1 code / Skill / workflow evidence card when relevant;
- 1 result / verification / metric card when relevant;
- 1 strong save-worthy summary/checklist card, often text-only.

The exact mix follows the evidence, not a fixed quota.

## 6. Truthfulness Gate

Before generation, verify every concrete claim against source evidence.

Fail the gate if:
- a metric/status is invented;
- a model is credited for a result actually produced by a fallback/deterministic tool;
- a screenshot is described as evidence of something it does not show;
- a web image is presented as if it came from the user's experiment;
- a single successful demo is generalized into stable improvement without repeatable evidence.

## 7. Gamma Generation Gate

Required settings for this workflow unless the user explicitly overrides them:

- `format = social`
- `cardOptions.dimensions = 4x5`
- Chinese language
- explicit `---` card breaks
- `cardSplit = inputTextBreaks`
- do not use random filler images
- preserve approved inline evidence URLs

## 8. Post-Generation QA

Before saying “done/final”, check:

- [ ] 4:5 social format is correct.
- [ ] Card count matches the approved structure.
- [ ] No old PPT/Gamma/contact-sheet page was accidentally used as a content image.
- [ ] Every used image has an obvious relation to the card claim.
- [ ] Every used image tells the reader what to look at.
- [ ] No card has a screenshot floating separately from the explanation.
- [ ] No unsupported status/metric/causal claim appears.
- [ ] Text-only cards remain text-only when images add no value.
- [ ] Layouts vary appropriately; not every page uses the same image-above/text-below pattern.
- [ ] Final card has clear save/recall value.

Any failed hard item means the artifact is not final.

## 9. Retry Policy

- Normal budget: one Gamma generation per episode.
- Retry: maximum one, only after identifying a concrete hard failure.
- Before retrying, write the exact failed gate and the exact correction. Do not regenerate just because the design could be prettier.
