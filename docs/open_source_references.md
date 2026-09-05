# Open-source engineering references

Reviewed 2026-09-05. These are engineering takeaways, not copied implementations.

| Project | Official source | What we actually borrow |
|---|---|---|
| Step1X-Edit | https://github.com/stepfun-ai/Step1X-Edit | Treat editing as instruction following with explicit reasoning/reflection opportunities; our equivalent is a logged diagnosis and bounded retry, not hidden chain-of-thought. |
| BrushEdit | https://github.com/TencentARC/BrushEdit | Separate task classification, target identification, mask and edit instruction; this directly motivates our `diagnose -> route -> repair` split. |
| MagicQuill | https://github.com/ant-research/MagicQuill | Make local edits and human interaction first-class; our mask artifact and comparison board are the minimal audit surface. |
| PowerPaint | https://github.com/open-mmlab/PowerPaint | Keep inpainting, object removal, and outpainting as distinct capabilities; our routes distinguish local repair from global regeneration. |
| AnyEdit | https://github.com/DCDmllm/AnyEdit | Use an editing taxonomy rather than one universal prompt; our six error classes drive route distribution in EXP-D. |
| Qwen-Image / Qwen-Image-Edit | https://github.com/QwenLM/Qwen-Image | Track text rendering, semantic editing, and preservation as separate model capabilities; a future adapter must record model/version and verify text rather than assume it. |

## Boundary

The references suggest product directions, not evidence that this repository ran those models. No external code, checkpoint, or result is included here. Real model reproduction remains blocked until an explicitly versioned runtime and weights/API are available.
