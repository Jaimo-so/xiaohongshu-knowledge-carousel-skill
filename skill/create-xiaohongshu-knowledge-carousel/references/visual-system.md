# Visual system and image prompts

## Default bundled house style

- Canvas: 1080 × 1440, exact 3:4 portrait.
- Safe margin: keep important content inside 8% of every edge.
- Copy zones: reserve the top 19–22% for the headline and the bottom 27–32% for explanatory copy.
- Palette: vintage blue `#287F98`, mustard `#E9BC2B`, old-paper cream `#EFE4CC`, charcoal `#25231F`, orange-red `#D65F45`.
- Medium: retro 1970s–1990s printed publication collage; photorealistic soft-vinyl character mixed with hand-cut paper props; worn edges, tactile grain, subtle screenprint dots, and slight ink-offset misregistration.
- Character: original recurring Jaimo with fluffy deep-brown short hair, oversized round black glasses, large dark eyes, rosy cheeks, youthful curious temperament, and big-head-small-body vinyl-doll proportions.
- Outfit: dusty blue-gray work jacket, short practical collar, cream undershirt, two understated cream buttons, mustard notebook partly tucked into one pocket, black trousers, mustard-and-cream shoes; no badge, logo, or writing.
- AI prop: friendly cream retro desk-machine with a black rounded screen face, simple cream eyes, orange antenna tip, paper input/output, and blue/orange details.
- Fixed corner system: top-left year, top-right topic category, bottom-left character name, bottom-right series name.

When the user supplies another brand or character, replace these specifics with that system while preserving the workflow.

## Base-generation prompt scaffold

```text
Use case: illustration-story
Asset type: wordless Xiaohongshu educational carousel base, page <ID>, exact 3:4 portrait
Input images: Image 1 is the identity anchor; Image 2 is the series-style anchor. Ignore all visible text in the references.
Primary request: <one concrete visual story whose objects map to the page’s knowledge>
Scene/backdrop: <one flat palette color; graphic editorial tableau, not a realistic room>
Style/medium: retro printed-publication collage; soft-vinyl character plus hand-cut paper props; tactile grain, worn edges, screenprint dots, slight offset-print misregistration
Composition/framing: reserve top <X>% and bottom <Y>% as quiet copy bands; keep critical objects inside 8% safe margins; keep four corners quiet
Character invariants: <repeat face, hair, glasses, proportions, outfit, pocket prop, shoes>
Constraints: completely wordless; no readable text, letters, numbers, labels, logos, watermark, signature, arrows, speech bubbles, extra people, unrelated decoration; paper may show abstract horizontal rules only
```

## Visual semantics

Prefer physical metaphors that can be understood without text:

- retrieval: search shelves, index drawers, magnifying glass, selected snippets;
- augmentation: question card plus selected evidence assembled into one dossier, metadata color tabs, noisy scraps discarded;
- generation: machine reads the dossier and produces an answer with source clips;
- verification: magnifying glass comparing claims with original source cards;
- chunking: long roll cut into moderate paper cards;
- embeddings: colored geometric dot clusters representing semantic vectors without mathematical notation;
- indexing: matching cards and vector patterns filed together;
- similarity search: query card compared with candidate cards;
- reranking: selected cards reordered on a rack;
- permissions: locked archive or lockbox;
- stale data: dusty, frozen, or damaged material set aside;
- insufficient evidence: empty evidence tray.

## Consistency check

For every page compare face, hair silhouette, glasses, jacket color, collar, buttons, pocket notebook, trousers, shoes, machine face, antenna, palette, border wear, and copy-band locations against the approved anchors. Correct only the drifting attribute when possible.

## Typography rules

- Typeset Chinese locally after generation.
- Use a strong Chinese headline, lighter body copy, and a contrasting caution line.
- Keep literal English step words short and large enough to read.
- Use opaque or nearly opaque panels when the illustration reduces contrast.
- Never shrink away a definition. Move it to another page or use a labeled card grid.
