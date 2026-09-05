# EP01 Content QA

`P1_CONTENT_STATUS = PARTIAL`

- Vintage travel-poster palette, aged print texture, grain, and screen-print feeling are clearly visible.
- The same cafe facade, windows, yellow door, and overall perspective remain recognizable.
- The model introduced large malformed English-like poster text and additional malformed storefront text.
- The scene-to-poster transformation is useful as a style demonstration, but the text artifacts prevent a clean content-ready pass.

Attempts: 1. No second attempt was spent because the core style conversion succeeded and the failure mode is visible evidence.

## Content polish v2

`CONTENT_USABLE_EP01 = YES`

- The v2 prompt explicitly prohibited generated text, typography, captions, logos, and storefront lettering.
- The one real Qwen v2 output is preserved at `runs/skill_series/EP01/v2_text_free/model_output_1080x1350.png`.
- Deterministic PIL post-processing replaced declared text bands with textured blank zones and added the optional title `OLD STREET CAFE`; no model-generated lettering is used in the final.
- Best comparison board: `assets/skill_series/ep01/compare_board_v2.png`.
- The v1 malformed-text failure remains retained above and is not overwritten.
