---
name: create-xiaohongshu-knowledge-carousel
description: Create complete Chinese Xiaohongshu educational carousel images from a topic, source document, notes, or an existing page concept. Use when Codex must plan every definition and meaning without compressing knowledge points, maintain a recurring character and visual system, directly render fully typeset 3:4 final pages without a standalone wordless-base stage, validate readability, and deliver only numbered final PNG pages.
---

# Create Xiaohongshu Knowledge Carousel

Create a coherent educational carousel whose knowledge is complete, illustrations are consistent, Chinese text is reliable, and deliverables contain only final effect images.

## Non-negotiable rules

1. Preserve every source definition, meaning, cause, mechanism, step, condition, limitation, warning, exception, and verification requirement. Never fold several distinct knowledge points into a vague summary. Add pages when the copy would otherwise be compressed.
2. Complete visual generation and exact Chinese typesetting as one final-render operation. Do not create, review, display, or deliver a standalone wordless illustration-base stage.
3. Keep one approved character identity, outfit, prop set, palette, print texture, safe margin, and corner-label system throughout the series.
4. Use exactly two full-page background roles in the bundled house style: vintage blue `#287F98` for the cover and old-paper yellow `#EFE4CC` for every interior page. Never rotate orange-red, mustard, blue, or other full-page interior backgrounds.
5. Make the fully typeset final page the first reviewable and user-visible image. Call `generatedImage` only for finished pages, never for a raw visual layer.
6. If an image tool technically returns a temporary visual layer, consume it immediately inside the same final-render operation and delete it after composition. It must not become a named workflow step, review checkpoint, saved project asset, or deliverable.
7. Never delete user source files unless the user explicitly asks. “Final-only delivery” means a clean deliverable directory; it does not authorize cleaning unrelated project files.

## Required references

- Before planning pages or writing copy, read [references/content-integrity.md](references/content-integrity.md).
- Before generating or editing images, read [references/visual-system.md](references/visual-system.md), then use the available image-generation skill/tool.
- When the topic is RAG or the user requests this exact series, read [references/rag-eight-page-example.md](references/rag-eight-page-example.md). Do not shorten its definitions or boundaries.

## Workflow

### 1. Resolve the brief

Identify the topic, audience, intended page count if fixed, source material, recurring character, visual references, copy language, output size, and destination. If the user provides no page count, derive it from knowledge density rather than forcing a fixed length.

If a stable character already exists, use the supplied images as identity anchors. Otherwise create an original character and record its invariant traits before making the series.

### 2. Build the coverage matrix

Extract the source into atomic knowledge points using the categories in `content-integrity.md`. Give every point a page assignment and a literal copy destination. Check that no definition or meaning disappears between extraction and page copy.

Recommended narrative order:

1. Cover and central question
2. Exact definition
3. Why it matters or what problem it solves
4. Each process step on its own page when necessary
5. Underlying mechanism or preparation
6. Limitations, failure sources, permissions, and verification
7. Final complete recap and actionable checklist

This order is a starting point, not a reason to remove domain-specific material.

### 3. Lock the series system

Write a short production specification containing:

- exact canvas and safe margins;
- palette hex codes and the allowed role of every color;
- character identity and approved outfit;
- recurring props and what each prop means;
- top and bottom copy zones;
- fixed background roles: blue cover and paper-yellow interiors;
- fixed corner labels;
- texture and medium;
- prohibitions such as text, logos, watermarks, extra people, and unsafe references.

Reuse `assets/style-anchor-cover.png` and `assets/style-anchor-interior.png` only when the user wants the bundled Jaimo/RAG house style. Treat their visible text as non-reference material.

### 4. Render fully typeset final pages directly

Produce one distinct final page per page specification. Label each input image role in the prompt: identity anchor, style anchor, composition reference, or edit target. Require an exact 3:4 portrait, quiet copy bands, four quiet corners, and a composition that supports the exact page copy. Use vintage blue only for the cover background. Use old-paper yellow for every interior background, with blue title and explanation panels.

For several pages, perform one final-render operation per page rather than using one generic prompt. Repeat all character and clothing invariants in every operation. Apply the manifest copy with `scripts/typeset_carousel.py` immediately, before exposing or saving any reviewable artifact.

The final page must be the first visible output:

- do not pause for a raw illustration review;
- do not create a `bases/` deliverable or a wordless page set;
- do not present temporary artwork paths;
- save and display only numbered `*-final.png` pages.

Inside the same operation, create a JSON manifest modeled on `assets/manifest.example.json`. Each line in the manifest must be intentional; do not rely on automatic paragraph summarization.

Run the deterministic final composer immediately after the visual tool returns:

```bash
python scripts/typeset_carousel.py path/to/manifest.json --output-dir path/to/final
```

Use a Python environment that provides Pillow. In Codex desktop, load the bundled workspace dependencies when the system Python lacks Pillow.

The script supports centered text panels and labeled grid cards. Use grid cards for dense mechanisms, comparisons, failure sources, or checklists. Prefer adding a page over shrinking important text below comfortable mobile-reading size. Remove any transient visual layer after its final page has been saved and checked.

### 5. Inspect every final page

Render or view every final image. Check:

- literal text accuracy and punctuation;
- no clipped or overflowing text;
- readable size and contrast on a phone;
- no panel hides the main action;
- recurring character face, clothing, and proportions remain stable;
- illustrations match the copy’s meaning;
- definitions and limitations remain present;
- filenames and sequence are complete.

If one page fails, make one targeted correction and recheck that page. Do not regenerate the entire series unnecessarily.

### 6. Validate final-only delivery

Run:

```bash
python scripts/verify_deliverables.py path/to/final --expected-count N
```

The command must report only numbered `*-final.png` files, identical canvas dimensions, and the expected page count. Deliver the folder path and a compact page list. Mention the image-generation path and deterministic typesetting path used.

## Output contract

Use filenames such as:

```text
01-cover-final.png
02-definition-final.png
03-why-final.png
04-step-one-final.png
```

The final directory contains only final PNG images. Keep manifests and source references in the working or skill directory, not inside the final deliverable directory.
