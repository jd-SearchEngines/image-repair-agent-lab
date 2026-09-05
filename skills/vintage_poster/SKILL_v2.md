# Vintage Poster Skill v2

## Model role

The real image model may change only the visual treatment and composition:

- vintage travel-poster palette
- aged print, grain, lithograph, and screen-print feeling
- hierarchy and scene-preserving composition
- original cafe/street geometry, perspective, door, and window identity

## Hard content boundary

The model must not generate text, rewrite text, generate typography, or generate
storefront/signage lettering. The prompt must explicitly request a completely
text-free result. Any required title is added after inference by a deterministic
PIL renderer, never by the image model. The optional deterministic title is
`OLD STREET CAFE`.

## QA and provenance

Keep the v1 output untouched. Record the v2 request, the single real-model
attempt, deterministic post-processing (if used), and a before/after board.
This is content evidence on the canonical scene mother image, not a claim that
the model can render reliable typography.
