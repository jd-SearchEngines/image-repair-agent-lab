# EP03 Content QA

`P1_CONTENT_STATUS = PARTIAL`

- All four deterministic clutter objects are visibly reduced or removed from the immediate product area.
- The bottle, cap, centered position, and broad background framing remain recognizable.
- Faint residual traces/ghosts of the paper card, cable, cup, and packaging remain in the After background.
- The result demonstrates the cleanup direction but does not satisfy a strict “only clutter disappears” content-ready bar.

Attempts: 1. No second attempt was spent; the remaining clutter is retained as a real-model limitation.

## Content polish second pass

`CONTENT_USABLE_EP03 = YES`

- Input to the second pass was the current v1 After image, not the original cluttered mother image.
- QA residual regions were declared before the call: upper-left card ghost, lower-left cable ghost, upper-right packaging ghost, and lower-right cup ghost.
- Exactly one real Qwen second-pass call was made. A feathered deterministic composite accepts only a limited blend of model pixels inside those regions; the bottle, cap, position, framing, and central region remain from v1.
- Outputs: `after_v1.png`, `after_v2.png`, `compare_v1_v2.png`, and `final_compare_board.png` under `runs/skill_series/EP03/v2_targeted_second_pass/`; asset board: `assets/skill_series/ep03/final_compare_board.png`.
- v1 residual-ghost finding remains retained above.
