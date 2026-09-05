# EP06 Content QA

`CONTENT_USABLE = NO`

- The yellow door remains clearly visible in the After image.
- The storefront windows, facade divisions, perspective, and broad building geometry remain related to the Mother B input.
- The rainy cinematic transformation is clear: evening palette, warm windows, wet road, and reflections are present.
- Generated storefront/sign text is visibly malformed, which is an obvious content artifact for a production-facing image.
- No structural benchmark or blind human panel was run.

The image is valuable as a controlled transformation example but is not content-ready under the requested artifact check.

## Content polish v2

`CONTENT_USABLE_EP06 = YES`

- The v2 real Qwen call used a disclosed deterministic text-safe Mother B variant, not the original photograph.
- The variant preserves the main building, yellow door/windows, perspective, and framing while neutralizing only the declared storefront text band.
- The rainy-night transformation, warm windows, and wet-road reflections remain strong; malformed storefront glyphs are not visible in the final board.
- Required provenance: `assets/skill_series/ep06/scene_text_safe_before.png`, `assets/skill_series/ep06/signage_mask.png`, and `assets/skill_series/ep06/variant_manifest.json`.
- Best comparison board: `assets/skill_series/ep06/compare_board_v2.png`.
- The v1 malformed-text failure remains retained above and is not overwritten.
