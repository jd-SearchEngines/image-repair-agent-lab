# EP04 Local Repair Backend Gate

Status: `LOCAL_REPAIR_BACKEND_BLOCKED`

## Scope

This gate checks for a real mask-conditioned editing/inpainting backend in the
current Apple Silicon environment. The existing Qwen MFlux route is not reused
for a masked repair: its installed CLI has no explicit `--mask-path` or
equivalent mask argument, and the prior EP04 attempt is retained as failure
evidence.

## Inventory from `/Users/jingdong/Downloads/Google_image`

| Backend / artifact | Explicit mask support | Apple Silicon | RAM / VRAM | Install complexity | License | Current readiness |
|---|---|---|---|---|---|---|
| Local Qwen Image Edit via MFlux q8 at `/Users/jingdong/.cache/modelscope/qwen-image-edit-2511-8bit` | No; instruction-only adapter | Runs on M3 Max through MLX | 64 GB unified memory; prior load passed | Already installed | Local model metadata; not re-licensed here | `READY_FOR_UNMASKED_ONLY` |
| Local Qwen Diffusers `QwenImageEditInpaintPipeline` using `/Users/jingdong/.cache/modelscope/Qwen-Image-Edit-2511` | Yes: `mask_image`; white mask pixels are repainted and black pixels preserved | PyTorch MPS path is available; smoke required | 64 GB unified memory; no discrete VRAM | Low: reuse `qa_judge_dpo/.venvs/sft-bench-hf` (`diffusers 0.40.0`) | Local model license must be checked against its upstream terms before production use | `PRECHECK_PASS / SMOKE_PENDING` |
| PowerPaint | Yes; object-removal/inpainting mask route | Official project is CUDA-oriented; MPS compatibility not established here | Requires model download and unified-memory headroom | High; separate environment and weights | MIT in upstream repository | `NOT_READY_NO_LOCAL_WEIGHTS` |
| BrushNet | Yes; explicit mask-conditioned inpainting | MPS compatibility not established here | Requires SD1.5/SDXL base plus BrushNet checkpoint | High; separate environment and multiple weights | Upstream terms apply | `NOT_READY_NO_LOCAL_WEIGHTS` |
| Generic Diffusers SD/SDXL inpaint | Yes at API level | MPS API path exists | Depends on local checkpoint size | Medium | Depends on checkpoint | `NOT_READY_NO_LOCAL_INPAINT_WEIGHTS` |
| Apple Core ML inpainting route | Possible with VAE encoder + inpaint model | Apple Silicon compatible in principle | Depends on converted artifacts | High; no compiled inpaint artifact found | Depends on converted model | `NOT_READY_NO_COREML_ARTIFACT` |

## Candidate decision

The only candidate found locally that can satisfy the explicit-mask contract is
the Qwen Diffusers inpaint pipeline. It receives one smoke case only. A smoke
success proves backend execution and mask plumbing, not that EP04 is a
successful content example. The original EP04 MFlux failure remains immutable.

## Official references

- [PowerPaint](https://github.com/open-mmlab/PowerPaint)
- [BrushNet](https://github.com/TencentARC/BrushNet)
- [Diffusers MPS documentation](https://huggingface.co/docs/diffusers/v0.35.0/en/optimization/mps)
- [Apple ml-stable-diffusion](https://github.com/apple/ml-stable-diffusion)

## Smoke provenance

- Input: `data/controlled_variants/product_defect_before.png`
- Explicit mask: `data/controlled_variants/defect_mask.png`
- Local model: `/Users/jingdong/.cache/modelscope/Qwen-Image-Edit-2511`
- Python: `/Users/jingdong/Downloads/Google_image/qa_judge_dpo/.venvs/sft-bench-hf/bin/python`
- Intended pipeline: `diffusers.QwenImageEditInpaintPipeline`
- Smoke budget: exactly one real backend attempt; no fallback to instruction-only editing
- Run result: `runs/skill_series/EP04/backend_smoke_qwen_diffusers/result.json`

## Smoke result

`SMOKE_STATUS = BLOCKED_BEFORE_INFERENCE`

- Candidate pipeline import succeeded and the environment reported MPS.
- The loader read the five transformer shards, then failed on
  `/Users/jingdong/.cache/modelscope/Qwen-Image-Edit-2511/text_encoder/` because
  there is no Diffusers-compatible `model.safetensors` or `pytorch_model.bin`.
- The directory contains only two `.safetensors.incomplete` text-encoder shards;
  the remaining shards are absent. The MFlux 8-bit text encoder is a different
  layout and was not substituted.
- Therefore no image inference occurred and no EP04 masked Before/After success
  is claimed. The original MFlux `MASK_NOT_SUPPORTED` failure remains the
  canonical EP04 content failure.
- Smoke parameters were recorded even though inference did not start:
  `num_inference_steps=8`, `strength=0.9`, `seed=8804`, `cost=null`.

`LOCAL_REPAIR_BACKEND_BLOCKED = YES`
