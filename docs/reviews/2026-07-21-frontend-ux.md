# Frontend review — design / layout / UX

**Date:** 2026-07-21  
**Scope:** Authenticated career module (`/projects`, `/experiences`, `/skills`, `/languages`, `/cv-versions`, `/profile`, `/achievements`, `/certifications`)  
**Context:** Mid-development walkthrough in browser (~830×437 viewport). Language: PL. Theme: light + dark. Seeded profile data. Some UI may still be in flux.

---

## Verdict

Solid app-shell and clear section pattern (title + subtitle + primary CTA + list). Dark mode and i18n chrome work. Main UX gaps are **raw data presentation** (ISO dates, snake_case enums, English Zod messages), **heavy modal forms**, and a recurring **dialog stacking / bleed-through** issue that hurts readability.

---

## Critical / high

### 1. Dialog content bleeds through background

On **Edit project** and **Add CV version**, page content (headings, cards, sidebar labels) remains visually readable through the modal. Overlay and dialog content both report `z-index: 50`. Forms become hard to scan.

**Suggest:** Ensure overlay sits below content (e.g. overlay `z-40`, content `z-50`), opaque `bg-background` on dialog content, and no mid-animation transparency that leaves text readable underneath.

### 2. Validation messages: English Zod, shown too early

Opening empty/required dialogs shows raw messages like:

> `String must contain at least 1 character(s)`

…while the rest of the UI is Polish. Errors also appear before the user has interacted meaningfully.

**Suggest:** Map Zod errors through i18n; validate on blur/submit, not on open.

### 3. Raw enums in list views

On **Experience**, employment type is shown as `full_time` / `freelance` / `part_time` instead of localized labels. In CV form language rows: `Polish · NATIVE`. Contrast: achievements use localized badge `Inne` — good pattern to reuse.

**Suggest:** Shared label maps for enums (employment type, visibility, language proficiency, project status/category).

### 4. Dates shown as ISO strings

Everywhere: `2010-12-01 – 2011-08-01`, `2021-11-01`, etc. Reads as API dump, not CV-ready copy. Day precision is rarely needed for careers UI.

**Suggest:** Locale-aware month/year (e.g. `gru 2010 – sie 2011` / `Dec 2010 – Aug 2011`), keep day only where expiry/exact date matters.

---

## Medium

### 5. Icon actions without accessible names

Projects list alone had ~100 unnamed `<button>`s (reorder / edit / delete). Screen readers and automation get empty names.

**Suggest:** `aria-label` on every icon-only control (Move up / Move down / Edit / Delete).

### 6. Modal forms are too long for a single dialog

**Edit project** and **Add CV version** are tall scrollable surfaces (~1.8k px content in a ~400 px dialog). Sticky section titles (e.g. “Linked experiences”) replace the dialog title when scrolling — user loses “what am I editing?” context.

**Suggest:** Tabs / accordion sections; sticky dialog header with title always visible; optional “advanced” fields collapsed by default.

### 7. CV version builder: flat mega-checklist

One long list of experiences + projects + skills + education + certifications + achievements + languages. No select-all per section, no search/filter, easy to miss items with 20+ projects.

**Suggest:** Collapsible sections with “select all / none”, counts, and search for long lists.

### 8. Profile page: duplicated chrome

`Mój profil` + the same subtitle appear as page **H1** and again as card **H3**. Nested card-in-card wastes vertical space and looks redundant.

**Suggest:** Page header once; card holds form only (or drop outer page subtitle duplicate).

### 9. Polish pluralization: `1 lat`

Skills duration shows **“1 lat”** — should be **“1 rok”** (2–4: lata, 5+: lat).

### 10. Long lists with no findability

Projects (~23 cards) → page height ~7800 px. No search, filter by status/year, or collapse. Same pattern risk on skills/certifications as data grows.

**Suggest:** Search + filters; optional compact density; virtualize or paginate later.

### 11. Inconsistent list density

| Section        | Pattern                         |
|----------------|---------------------------------|
| Skills         | Compact rows (good density)     |
| Projects / Exp / Languages / Certs | Full cards + 4 icon actions |

Not wrong, but skills feel like a different product. Consider shared list-row component with optional expand.

### 12. Nested “card in card”

Outer content shell (white/dark rounded panel) + inner item cards. On small viewports this eats width and adds double borders.

**Suggest:** Flatten: shell = page background; items = single surface.

### 13. Narrow viewport / sidebar

At ~830 px width, sidebar labels truncate (`Projec…`, `Experi…`). Duplicate “Toggle sidebar” controls exist in the a11y tree.

**Suggest:** Auto-collapse sidebar earlier; icon-only rail with tooltips; one toggle control.

### 14. Mixed locale in chrome vs messages

Dialog close control labeled **“Close”** while buttons are **Anuluj / Zapisz**. Zod strings in EN (see above).

---

## Low / polish

- **Empty state (CV versions)** — clear icon + copy + primary CTA. Good reference for other empty sections.
- **Dark mode** — works; accent and active nav remain readable.
- **Active nav** — purple highlight + left border is clear in both themes.
- **Languages CEFR** — levels localized well (`B2 — Średnio zaawansowany wyższy`). Language *names* stay English (`Polish`, `English`) — OK if intentional ISO names, otherwise localize.
- **Profile completeness** — `80% · /p/jan-madeyski` is useful; a thin progress bar would make 80% scannable.
- **Ongoing ranges** — `2018-01-01 – Obecnie tu pracuję` mixes machine date with sentence; prefer `sty 2018 – obecnie`.
- **Footer** after very long lists — lots of scroll before footer; not blocking, just noisy on data-heavy pages.

---

## What works well

1. Consistent section template: title, one-line purpose, primary “Dodaj …” CTA.
2. Reorder affordances on list items (when labeled properly, this is the right model for CV ordering).
3. Tech tags on project cards are scannable.
4. Seeded data makes the product feel real during development.
5. i18n of shell (sidebar, buttons, empty states) is largely in place — remaining gaps are mostly **data formatting**, not missing keys.

---

## Suggested priority order

1. Dialog opacity / z-index (readability)
2. Humanize dates + enums
3. i18n Zod / defer validation
4. `aria-label` on icon buttons
5. Slim down / section CV + project modals
6. Profile header dedupe + skills pluralization
7. Search/filter on long lists

---

## Pages not deeply exercised

- Education detail / edit dialogs  
- Public profile `/p/:slug`  
- Mobile (&lt;640 px) layout  
- Delete confirmations / toasts after save  

Worth a second pass once forms stabilize.
