# Cinematic Scene Skill v2

## Model role

Change only lighting, weather, reflections, contrast, and atmosphere while
preserving the original building, yellow door/windows, storefront geometry,
perspective, and scene identity.

## Hard text boundary

Do not generate new text. Do not rewrite storefront signage. Preserve the sign
region where possible. If the original sign triggers text rewriting, use a
controlled deterministic text-safe variant before inference: neutralize only a
small declared signage text region without changing the main building geometry.
The controlled variant must never be described as the original photograph.

## QA and provenance

Keep `scene_text_safe_before.png`, `signage_mask.png`, and
`variant_manifest.json` when preprocessing is used. Record the single real
Qwen attempt and inspect malformed-text risk separately from the cinematic
change. This is controlled content evidence, not a production-quality claim.
