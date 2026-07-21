# Design direction — CareerHub × Dimension.dev

Planning pack for a visual refresh. **CareerHub brief (below) is the source of truth.** The Dimension extract is inspiration only — do not apply it 1:1.

## CareerHub brief

Agreed direction (2026-07-21):

| Decision | Choice |
|----------|--------|
| **Look** | Light glassmorphism — frosted / semi-transparent panels over a multi-color gradient background |
| **Mood** | Warm, vivid — not dark void, not ~2% monochrome |
| **Palette direction** | Teal / green base + yellow / orange accent |
| **Layout** | Keep current CareerHub structure; restyle color, surfaces, accents |
| **Skip (for now)** | Floating bottom nav; literal Dimension dark canvas |
| **Scope** | Whole site shell (landing + authenticated app) |
| **Themes** | Light and dark with equal quality |
| **Gradient** | Always present; calmer / quieter in the app than on marketing |
| **Dark mode** | Same system, darkened (same gradient + glass, lower luminance) |
| **Success** | Modern, cohesive, attractive — not a Dimension clone |

### Do (CareerHub)

- Keep existing layout chrome (sidebar / top nav / page structure); restyle, don’t redesign IA
- Use frosted glass panels (blur + translucency) as the main elevated surface language
- Keep a visible background gradient everywhere; tone it down in the app
- Ship light and dark as first-class; dark = same recipe, darker
- Prefer teal/green surfaces with yellow/orange for accent / CTA moments

### Don't (CareerHub)

- Don’t adopt Dimension’s achromatic dark-first system or solid `#0a0a0a` as the default canvas
- Don’t use violet (`#6b62f2`) as the brand accent — that’s Dimension’s, not ours
- Don’t add floating bottom nav in the first pass
- Don’t rebuild page layouts just to mimic Dimension’s landing composition

### Open (later)

- Exact hex tokens for teal / green / yellow-orange (light + dark)
- How strong the app gradient is vs marketing
- Fonts: keep current stack vs borrow Dimension’s DM Sans / Geist restraint
- Which shadcn/ui tokens map to glass surfaces

---

## Reference extract — Dimension.dev

> Source material only. Useful for glass, pills, hairlines, spacing rhythm — **not** for palette or dark-void canvas.

Extracted from [dimension.dev](https://dimension.dev) via [Refero](https://styles.refero.design/style/fbcf9cbb-7c6b-449d-862a-bce521a8ab1d).

**Mismatch to remember:** Refero describes a dusk-lit matte-black (`#0a0a0a`) achromatic UI. The screenshot we care about reads as a warm multi-color gradient + frosted glass — that reading matches the CareerHub brief above.

### Assets

| File | Role |
|------|------|
| [DESIGN.md](./DESIGN.md) | Full Dimension style dump — tokens, components, prompts |
| [design-tokens.json](./design-tokens.json) | Machine-readable Dimension tokens |
| [tailwind-v4.css](./tailwind-v4.css) | Dimension Tailwind v4 `@theme` snippet |
| [dimension-dev.png](./dimension-dev.png) | Screenshot (gradient + glass — primary visual reference) |

### Dimension palette (reference only)

| Name | Value | Role in Dimension |
|------|-------|-------------------|
| Void Canvas | `#0a0a0a` | Their page background — **not** our target |
| Graphite | `#161616` | Elevated panels |
| Frosted Glass | `#d4d4d4` @ 10% | Translucent fill (technique we keep) |
| Snow White | `#ffffff` | CTA / headlines on dark |
| Bone | `#ededed` | Body on dark |
| Hairline | `#e5e5e5` | 1px borders |
| Dusk Violet | `#6b62f2` | Their accent — **not** ours |

### Useful techniques to borrow

- Frosted panels: translucency + backdrop blur + hairline border (not heavy drop shadow)
- Pill CTAs (9999px) where they already fit our UI
- Generous section rhythm; restrained headline weight where it helps
- Soft multi-stop background gradient as atmosphere (recolored to teal/green + warm accent)
