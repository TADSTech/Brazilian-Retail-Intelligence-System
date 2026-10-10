# Design — Brazilian Retail Intelligence System (BRIS)

A locked design system for this app. Every page redesign reads this file before
emitting code. Do not regenerate per page — extend or amend this file when the
system needs to grow.

## Genre

modern-minimal

## Macrostructure family

Pick one base macrostructure for marketing pages, one for app pages, one for
content pages (if applicable). Pages within a family share the family's shape;
they vary only in component archetypes.

- Marketing pages: **Stat-Led** — hero is the giant figure `99,441` paired with a worded headline; variation knobs: supporting-stat count (3–4), terminal card presence, dark-band presence.
- App pages:       **Bento Grid** — hairline cells, mixed spans (1×1, 2×1, 1×2, 2×2); variation knobs: cell spans, tile count per tab (6–12), hero tile = primary KPI.
- Content pages:   none — docs live in the GitHub `docs/` tree, not in-app.

## Theme

Cobalt (cool engineered light ground · one electric cobalt signal · code/terminal as focal chrome).

- `--color-paper`   oklch(98.5% 0.004 250)
- `--color-paper-2` oklch(96.8% 0.006 250)
- `--color-paper-3` oklch(94.5% 0.008 250)
- `--color-ink`     oklch(24% 0.02 258)
- `--color-ink-2`   oklch(34% 0.018 257)
- `--color-muted`   oklch(50% 0.02 257)
- `--color-rule`    oklch(91% 0.005 250)
- `--color-rule-2`  oklch(86.5% 0.007 250)
- `--color-rule-strong` oklch(62% 0.012 252)   (input/control borders — ≥3:1 on paper and paper-3)
- `--color-accent`  oklch(56% 0.20 256)        (theme nominal is 58%; darkened to clear 4.5:1 as text on paper and behind accent-ink labels)
- `--color-accent-ink` oklch(98.5% 0.004 250)  (labels on accent fills — verified 4.7:1)
- `--color-accent-on-dark` oklch(74% 0.14 256) (accent text/links on graphite surfaces)
- `--color-focus`   oklch(56% 0.20 256)        (with 2px offset, sits on paper; inside graphite use `--color-accent-on-dark`)
- `--color-graphite`  oklch(22% 0.016 260)     (code card)
- `--color-graphite-2` oklch(20% 0.016 260)    (the one full-bleed dark band)
- `--color-graphite-ink` oklch(92% 0.01 250)
- `--color-error`   oklch(55% 0.19 25)
- `--color-success` oklch(61% 0.13 155)

## Typography

- Display: Space Grotesk, weight 500/600, style **normal** (roman — italic headers banned)
- Body:    Inter, weight 400/500
- Mono:    JetBrains Mono, weight 400/500 — labels UPPERCASE, `letter-spacing: 0.06em`
- Display tracking: `-0.02em`; body measure ≤ 66ch
- Type scale anchor: `--text-display` = `clamp(2.5rem, 5vw + 1rem, 4rem)`; hero figure `--text-figure` = `clamp(3.5rem, 11vw, 8.5rem)` with `font-variant-numeric: tabular-nums`
- Loaded via Google Fonts link in `dashboard/index.html` (theme required dependency)

## Spacing

4-point named scale. The values are in `dashboard/src/tokens.css`. Pages must use
named tokens (`var(--space-md)`), never raw values.

## Motion

- Easings: `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`, `--ease-in: cubic-bezier(0.7, 0, 0.84, 0)`, `--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)`
- Reveal pattern: **Home only** — one-shot fade + 10px rise (`.reveal` / `.is-in`, ~600ms) + one hero terminal type-in (plays once). App pages: no reveals.
- Reduced-motion fallback: opacity-only, ≤ 150 ms; type-in and counters render final state instantly.
- ≤ 3 animation primitives per page. Never animate layout properties.

## Microinteractions stance

- **Silent success** — no "Done!" toasts; `sonner` reserved for load errors with a retry.
- Tooltip: 800 ms delay on hover, 0 ms on focus.
- Forms: labels above inputs; validate on blur (touched pattern); errors replace helper text (stable `min-height: 1lh`); `aria-invalid` + `aria-describedby`.
- Buttons: press = `translateY(1px)` 100 ms; focus ring appears instantly, never animated.
- Tabs: content crossfade 150 ms (no sideways slide, no height animation).
- Command palette (Home): instant open, indicator `translateY` 120 ms, Esc/backdrop closes, focus-managed `role="dialog"`.

## CTA voice

- Primary CTA: solid cobalt fill, **6px radius**, `--color-accent` bg + `--color-accent-ink` label, verb + named destination ("Open the dashboard").
- Secondary CTA: hairline-outlined chip (6px) or text link with cobalt underline-grow on hover. Never a pill, never a gradient.

## Per-page allowances

- Marketing pages MAY use enrichment (Tier-A CSS art only — the graphite terminal card qualifies as theme chrome).
- App pages MUST NOT use enrichment — function carries the page.
- Content pages: typography only.

## What pages MUST share

- The wordmark: `Brazil` (ink) + `BI` (cobalt), Space Grotesk 600.
- The accent colour and its placement (≤ 5 % per viewport).
- The display + body + mono fonts.
- The CTA voice (6px radius, fill/outline pair, verb-first copy).
- Hairline divider language (1px `--color-rule`), 6px control radii / 10px card radii, mono uppercase labels.

## What pages MAY differ on

- Macrostructure within the page-type family (Home is Stat-Led; a future marketing route could be Workbench — still the same type, colour, and CTA voice).
- Hero archetype (within the family's allowance).
- Bento tile count and spans per tab.

## Honest metrics

Every number shown in the UI must come from this table or be replaced by a
`—` placeholder labelled "metric to confirm". No invented metrics (slop-test gate 46).

| Metric | Value | Source |
|---|---|---|
| Orders (Olist public dataset) | 99,441 | Kaggle `olistbr/brazilian-ecommerce` + DataHub row table |
| Rows across the 8 `TABLE_ORDER` tables | 1,287,963 ("1.29M") | verified 2026-10-10: Supabase row counts match transformed source (geolocation deduped to 738,332; reviews keep score-only rows) |
| Order items | 112,650 | DataHub row table |
| Tables | 8 | `etl/config.py::TABLE_ORDER` |
| Tests passing | 23 | `pytest tests -q` (2026-10-10) |
| API endpoints | 3 | `docs/API_ENDPOINTS.md` |
| Load backends | 2 (supabase, postgres) | `etl/config.py::ETL_BACKEND` |

Dropped as unverifiable: "1.2M+ records", "$8.2M revenue", "97.6K orders".

## Exports

Drop-in formats for re-using this design system in other projects.
See [`export-formats.md`](../.agents/skills/hallmark/references/export-formats.md) (in the Hallmark skill) for the canonical mapping.

### tokens.css

The live copy is `dashboard/src/tokens.css` — keep this block and that file identical.

```css
:root {
  /* paper / ink */
  --color-paper:        oklch(98.5% 0.004 250);
  --color-paper-2:      oklch(96.8% 0.006 250);
  --color-paper-3:      oklch(94.5% 0.008 250);
  --color-ink:          oklch(24% 0.02 258);
  --color-ink-2:        oklch(34% 0.018 257);
  --color-muted:        oklch(50% 0.02 257);
  --color-rule:         oklch(91% 0.005 250);
  --color-rule-2:       oklch(86.5% 0.007 250);
  --color-rule-strong:  oklch(62% 0.012 252);

  /* the one signal */
  --color-accent:        oklch(56% 0.20 256);
  --color-accent-ink:    oklch(98.5% 0.004 250);
  --color-accent-on-dark: oklch(74% 0.14 256);
  --color-focus:         oklch(56% 0.20 256);

  /* graphite (code card + the one dark band) */
  --color-graphite:      oklch(22% 0.016 260);
  --color-graphite-2:    oklch(20% 0.016 260);
  --color-graphite-ink:  oklch(92% 0.01 250);
  --color-graphite-muted: oklch(65% 0.02 258);

  /* status */
  --color-error:   oklch(55% 0.19 25);
  --color-success: oklch(61% 0.13 155);

  /* data-viz (accent family + cool neutrals) */
  --color-chart-1: oklch(56% 0.20 256);
  --color-chart-2: oklch(44% 0.11 262);
  --color-chart-3: oklch(72% 0.13 238);
  --color-chart-4: oklch(62% 0.13 295);
  --color-chart-5: oklch(55% 0.03 255);

  /* type */
  --font-display: "Space Grotesk", system-ui, sans-serif;
  --font-body:    "Inter", system-ui, sans-serif;
  --font-mono:    "JetBrains Mono", ui-monospace, monospace;

  /* 4pt spacing */
  --space-3xs: 0.25rem;  --space-2xs: 0.5rem;  --space-xs: 0.75rem;
  --space-sm:  1rem;     --space-md:  1.5rem;  --space-lg: 2rem;
  --space-xl:  3rem;     --space-2xl: 4.5rem;  --space-3xl: 7rem;

  /* text scale */
  --text-xs: 0.75rem;   --text-sm: 0.875rem;  --text-md: 1.125rem;
  --text-lg: 1.375rem;  --text-xl: 1.75rem;   --text-2xl: 2.25rem;
  --text-display: clamp(2.5rem, 5vw + 1rem, 4rem);
  --text-figure:  clamp(3.5rem, 11vw, 8.5rem);

  /* motion */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --dur-fast: 150ms; --dur-mid: 250ms; --dur-slow: 600ms;

  /* geometry */
  --radius-control: 6px;
  --radius-card: 10px;
}
```

### Tailwind v4 `@theme`

```css
@theme inline {
  --color-paper: var(--color-paper);
  --color-ink: var(--color-ink);
  --color-accent: var(--color-accent);
  --font-display: var(--font-display);
  --font-body: var(--font-body);
  --font-mono: var(--font-mono);
  /* mirror the rest of tokens.css with --spacing-* and --text-* for Tailwind utilities */
}
```

### DTCG `tokens.json`

```json
{
  "color": {
    "paper":  { "$value": "oklch(98.5% 0.004 250)", "$type": "color" },
    "ink":    { "$value": "oklch(24% 0.02 258)", "$type": "color" },
    "accent": { "$value": "oklch(56% 0.20 256)", "$type": "color" }
  },
  "font": {
    "display": { "$value": "Space Grotesk", "$type": "fontFamily" },
    "body":    { "$value": "Inter", "$type": "fontFamily" },
    "mono":    { "$value": "JetBrains Mono", "$type": "fontFamily" }
  },
  "space": {
    "md": { "$value": "1.5rem", "$type": "dimension" }
  }
}
```

### shadcn/ui CSS variables

Mapped in `dashboard/src/index.css` (`:root`, referencing the Hallmark tokens by name).

```css
:root {
  --background:        var(--color-paper);
  --foreground:        var(--color-ink);
  --card:              var(--color-paper);
  --card-foreground:   var(--color-ink);
  --popover:           var(--color-paper);
  --popover-foreground: var(--color-ink);
  --primary:           var(--color-accent);
  --primary-foreground: var(--color-accent-ink);
  --secondary:         var(--color-paper-3);
  --secondary-foreground: var(--color-ink-2);
  --muted:             var(--color-paper-3);
  --muted-foreground:  var(--color-muted);
  --accent:            var(--color-paper-3);
  --accent-foreground: var(--color-ink);
  --destructive:       var(--color-error);
  --border:            var(--color-rule);
  --input:             var(--color-rule-strong);
  --ring:              var(--color-focus);
  --radius:            6px;
  --sidebar:           var(--color-paper-2);
  --sidebar-foreground: var(--color-ink-2);
  --sidebar-primary:   var(--color-accent);
  --sidebar-accent:    var(--color-paper-3);
  --sidebar-border:    var(--color-rule);
  --chart-1:           var(--color-chart-1);
  --chart-2:           var(--color-chart-2);
  --chart-3:           var(--color-chart-3);
  --chart-4:           var(--color-chart-4);
  --chart-5:           var(--color-chart-5);
}
```
