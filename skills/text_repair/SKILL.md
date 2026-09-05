# Chinese Text Repair Skill v1

- Keep `wrong_text`, `correct_text`, and `text_bbox` in the request.
- Change only the text-safe region; preserve product, background, layout, and lighting.
- OCR must be run before making a text-correctness claim.
- If OCR is absent or wrong, report the failure as content evidence.
