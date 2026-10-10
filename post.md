# BrazilBI Showcase Post

Post copy for the dashboard redesign showcase. Primary audience: recruiters and developers.

## LinkedIn

> I rebuilt my retail analytics dashboard around one rule: no number on screen that can't be proven.
>
> BrazilBI is a full data platform on the public Olist Brazilian e-commerce dataset — and I just redesigned the entire React front end from a single design system.
>
> That one rule changed how every screen got built:
>
> → **Real metrics only.** 99,441 orders · 1.55M rows · 8 tables — all sourced from the actual dataset. If the database is unreachable, the KPIs render "—" with an honest error state. No placeholder "$8.2M revenue" cards. Ever.
>
> → **One design system, zero drift.** A single design.md + oklch token file ("Cobalt") drives the marketing page, dashboard, and sign-in. Consistency by construction, not by review.
>
> → **Verification, not vibes.** The final pass ran 58 quality gates: rendered Playwright checks from 320px to 1920px (zero horizontal scroll, zero wrapping button labels), 29/29 contrast pairs, aria-labels on all 12 charts, complete reduced-motion paths — plus a build/lint/test suite that stays green (15 pytest).
>
> The boring parts are the point: FK-safe load order, pure transforms with unit tests, a FastAPI control plane, and a dashboard that tells the truth even when the data layer fails.
>
> Design earns the first 10 seconds. Engineering honesty earns the next 10 minutes.
>
> Stack: Python · pandas · FastAPI · Postgres/Supabase · React 19 · Vite · Tailwind 4 · Recharts/Plotly
>
> Repo + walkthrough in the comments 👇

## X / Twitter (≤280 chars)

```
I rebuilt my portfolio dashboard around one rule:

No number on screen that can't be proven.

99,441 real orders — or "—" plus an honest error state.

One design system. 58 quality gates. Playwright-verified 320px → 1920px.

23 tests green. No fake KPIs.
```

## Posting notes

- **Image:** attach `home-1280-fold.png` or `dashboard-1280.png`
  (captured at `C:\Users\TADS\AppData\Local\Temp\opencode\hallmark-shots\`).
  A before/after collage outperforms a single shot.
- **Hashtags (LinkedIn, pick 3):** `#DataEngineering` `#React` `#Portfolio` `#FastAPI` `#DesignSystems`
- **Link:** put the GitHub URL in the first comment — LinkedIn suppresses in-post links.
- **Fact-check before posting:**
  - 99,441 orders / 1.55M rows / 8 tables — public Olist dataset counts
  - 23 tests — `python -m pytest tests -q`, verified 2026-10-10
  - 29/29 contrast pairs — `contrast_gate40.py`
  - 58 quality gates — Hallmark slop-test checklist
  - Playwright verified 320–1920px — `render_check.py` / `wrap_check.py`
