---
name: douyin-gamma-production
description: Use this skill whenever creating or regenerating Douyin social-image Gamma content from project evidence, code screenshots, before/after images, logs, or external references. It enforces evidence-first asset selection, image relevance gates, provenance, layout planning, truthful claims, Gamma 4:5 social output, and post-generation QA. Do not use it for ordinary PPT decks or unrelated image generation.
owner: jd-SearchEngines
tags: [douyin, gamma, content-production, qa, evidence]
license: MIT
---

# Douyin Gamma Production

## Use When
- Creating or regenerating a Douyin 图文 Gamma for an episode/topic.
- Turning project evidence, GitHub assets, code screenshots, logs, tests, before/after images, or web references into social cards.
- The user asks for “图文 Gamma”, “4:5 图文”, “配图”, “重新生成某一集”, or similar.

## Don't Use When
- The user wants a normal presentation/PPT course deck.
- The user wants a standalone image or cover only.
- There is no evidence source and the task is purely creative copywriting.

## Workflow
1. **Lock the episode claim first.** Write one sentence: “这一集到底要证明什么？” Every card must support this claim or a necessary sub-claim.
2. **Read evidence before designing cards.** Inspect the current episode’s raw project assets, source files, code/log/test evidence, and content notes. Do not start from an old PPT/Gamma page.
3. **Build an internal asset map before generation.** For every candidate image record: source, provenance, what claim it supports, what the reader should look at, relevance score, and whether it should be used.
4. **Apply the image relevance gate.** Only use an image when it scores 4/5 or 5/5 on the rubric in `references/ASSET_QA.md`. If no image passes, make that card text-only.
5. **Use source priority in this order:**
   - A. Raw project evidence under `assets/skill_series/<episode>/` or equivalent source directories.
   - B. Direct code/log/test screenshots or generated metric charts from the actual project.
   - C. External images only when they materially clarify the claim and have clear provenance; prefer official docs, public-domain, or reusable sources.
   - D. Decorative images are optional and must never substitute for evidence.
6. **Explicitly reject artifact recycling.** Never use an old PPT screenshot, previous Gamma card, contact sheet, or composite presentation page as the evidence image unless the user explicitly asks to show that artifact itself.
7. **Design cards around evidence, not around a quota.** Default to 6 cards for this series, but the number of image cards is flexible. A good default is 3–4 evidence-image cards and 2–3 text/diagram/checklist cards. Do not force one image per card.
8. **For every image card, define the image-reader relationship.** The card must visually or textually answer both:
   - “这张图证明什么？”
   - “读者应该看哪里？”
   Use a short caption, arrow, crop, highlight, before/after label, code callout, or one-line interpretation. Do not dump a screenshot without explanation.
9. **Keep claims truthful and evidence-bounded.** Never infer unsupported metrics or statuses. If evidence says only `CONTENT_USABLE=YES`, do not invent `TARGET_MATCH=YES`. If the model failed and a deterministic tool produced the final output, say so explicitly.
10. **Plan layout before Gamma generation.** For each card choose one layout intent: hero evidence, side-by-side before/after, annotated screenshot, code + interpretation, metric + takeaway, or text-only checklist. Avoid the repeated “image on top, paragraph below” pattern across all cards.
11. **Generate Gamma with hard format settings.** Use `format=social`, `cardOptions.dimensions=4x5`, explicit `---` card breaks, and `cardSplit=inputTextBreaks`. Use Chinese. When card copy is fully specified, use `textMode=preserve`.
12. **Do not ask Gamma to add filler visuals.** Inline the approved evidence URLs where needed. Do not use random AI/web images merely to fill space. If external visuals are needed, select them deliberately before the Gamma call.
13. **Resource guardrail.** One normal Gamma generation per episode. Retry at most once, and only for a hard failure such as wrong aspect ratio, missing/incorrect evidence image, broken rendering, or a material factual error.
14. **Post-generation QA before calling it done.** Check the generated Gamma against `references/ASSET_QA.md`. If any hard gate fails, do not describe the artifact as final.

## Rules
- Always start from the episode’s claim and evidence, not from layout aesthetics.
- Always prefer raw project assets over old PPT/Gamma screenshots.
- Always explain the meaning of an inserted screenshot or image.
- Always allow a text-only card when no image adds value.
- Always keep image provenance traceable.
- Never insert an image only because the page “needs a picture”.
- Never reuse a contact sheet or old presentation page as the main visual unless explicitly requested.
- Never claim an image is related without naming the exact relation.
- Never silently replace a failed model step with a different tool and still attribute success to the model.
- Never generate multiple retries casually; diagnose first.

## Examples
- “帮我生成 EP03 图文 Gamma” → read EP03 evidence → asset map → relevance gate → 4:5 social Gamma → QA.
- “这一页要不要配图？” → use a relevant evidence image only if it strengthens the claim; otherwise keep text-only.
- “可以网上找图” → external image is allowed only if directly relevant, provenance is clear, and it beats available project evidence for communication value.
- “第五集别再贴 PPT” → reject PPT/contact-sheet assets; use raw source evidence, code/log screenshots, or no image.

## Edge Cases
- If project assets exist but are unclear → inspect source notes/logs before using them.
- If an image is visually attractive but only loosely related → reject it.
- If the strongest evidence is code/log text → use an annotated code/log screenshot rather than a decorative image.
- If no evidence image supports a card → use a text-only logic/checklist card.
- If Gamma cannot naturally integrate an image with copy → simplify the card or split the reasoning; do not keep a visually detached screenshot.
- If external image rights/provenance are uncertain → prefer project evidence or a text-only/diagram card.

## References
See `references/ASSET_QA.md` for the mandatory relevance rubric, provenance rules, layout checks, and pre/post-generation gates.
