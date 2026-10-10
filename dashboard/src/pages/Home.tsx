import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { ArrowRight, ArrowUpRight, Check, Copy, LayoutDashboard, Search } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { BbiLogo } from '../components/bbi-logo'
import { prefersReducedMotion, useCountUp } from '../hooks/use-count-up'

const GH_REPO = 'https://github.com/TADSTech/Brazilian-Retail-Intelligence-System'
const GH_DOCS = `${GH_REPO}/tree/main/docs`
const TEST_LINE = 'python -m pytest tests -q'
const QUICKSTART = [
  'pip install -r requirements-dev.txt',
  'python -m etl',
  'uvicorn api.main:app --reload',
]

function CopyBtn({ text }: { text: string }) {
  const [done, setDone] = useState(false)
  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setDone(true)
      window.setTimeout(() => setDone(false), 1200)
    } catch {
      // clipboard unavailable — stay silent
    }
  }
  return (
    <button
      type="button"
      className="copy-btn"
      aria-label={`Copy: ${text}`}
      data-state={done ? 'done' : undefined}
      onClick={onCopy}
    >
      {done ? <Check size={16} aria-hidden /> : <Copy size={16} aria-hidden />}
    </button>
  )
}

type PaletteEntry = {
  label: string
  hint: string
  run: () => void
}

export function Home() {
  const navigate = useNavigate()
  const rootRef = useRef<HTMLDivElement>(null)
  const [frost, setFrost] = useState(false)
  const [paletteOpen, setPaletteOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [cursor, setCursor] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)

  const orders = useCountUp(99441)
  const headline = 'real Olist orders, one pipeline to dashboards.'

  /* one-shot section reveals (Home only) */
  useEffect(() => {
    const root = rootRef.current
    if (!root) return
    const nodes = Array.from(root.querySelectorAll<HTMLElement>('.reveal'))
    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
      nodes.forEach((n) => n.classList.add('is-in'))
      return
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-in')
            io.unobserve(e.target)
          }
        })
      },
      { threshold: 0.15 }
    )
    nodes.forEach((n) => io.observe(n))
    return () => io.disconnect()
  }, [])

  /* N1b frost-on-scroll */
  useEffect(() => {
    const onScroll = () => setFrost(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  /* hero terminal — one-shot type-in of a single line */
  const [typed, setTyped] = useState(() =>
    prefersReducedMotion() ? TEST_LINE : ''
  )
  useEffect(() => {
    if (prefersReducedMotion()) return
    let i = 0
    const id = window.setInterval(() => {
      i += 1
      setTyped(TEST_LINE.slice(0, i))
      if (i >= TEST_LINE.length) window.clearInterval(id)
    }, 28)
    return () => window.clearInterval(id)
  }, [])
  const typedDone = typed.length >= TEST_LINE.length

  const scrollToSection = useCallback((id: string) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: prefersReducedMotion() ? 'auto' : 'smooth',
      block: 'start',
    })
  }, [])

  /* command palette — keyboard-managed dialog */
  const entries: PaletteEntry[] = useMemo(
    () => [
      {
        label: 'Open dashboard',
        hint: 'route',
        run: () => navigate('/dashboard'),
      },
      { label: 'Sign in', hint: 'route', run: () => navigate('/signin') },
      { label: 'Dataset', hint: 'section', run: () => scrollToSection('dataset') },
      { label: 'Backend', hint: 'section', run: () => scrollToSection('backend') },
      {
        label: 'Quickstart',
        hint: 'section',
        run: () => scrollToSection('start'),
      },
      { label: 'Source on GitHub', hint: 'external', run: () => window.open(GH_REPO, '_blank', 'noopener') },
    ],
    [navigate, scrollToSection]
  )

  const filtered = entries.filter((e) =>
    e.label.toLowerCase().includes(query.trim().toLowerCase())
  )

  const closePalette = useCallback(() => {
    setPaletteOpen(false)
    setQuery('')
    setCursor(0)
    triggerRef.current?.focus()
  }, [])

  const openPalette = useCallback(() => {
    setPaletteOpen(true)
    setCursor(0)
  }, [])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        if (paletteOpen) closePalette()
        else openPalette()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [paletteOpen, closePalette, openPalette])

  useEffect(() => {
    if (paletteOpen) inputRef.current?.focus()
  }, [paletteOpen])

  const onPaletteKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      e.preventDefault()
      closePalette()
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      setCursor((c) => (filtered.length ? (c + 1) % filtered.length : 0))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setCursor((c) => (filtered.length ? (c - 1 + filtered.length) % filtered.length : 0))
    } else if (e.key === 'Enter') {
      e.preventDefault()
      const entry = filtered[cursor]
      if (entry) {
        closePalette()
        entry.run()
      }
    }
  }

  const stats = [
    { value: '1.55M', label: 'Rows (8 tables)' },
    { value: '8', label: 'Tables, FK-ordered' },
    { value: '2', label: 'Load backends' },
    { value: '23', label: 'Tests passing' },
  ]

  return (
    <div ref={rootRef} className="min-h-screen bg-background">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-[6px] focus:border focus:border-border focus:bg-background focus:px-4 focus:py-2 focus:text-sm"
      >
        Skip to content
      </a>

      {/* N1b SaaS three-section nav */}
      <header className={`nav ${frost ? 'is-scrolled' : ''}`}>
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2 text-lg font-semibold tracking-tight" style={{ fontFamily: 'var(--font-display)' }}>
            <BbiLogo className="size-7" />
            <span className="text-foreground">Brazil</span>
            <span className="text-primary">BI</span>
          </Link>

          <nav aria-label="Sections" className="hidden items-center gap-6 md:flex">
            <button type="button" className="nav-link" onClick={() => scrollToSection('dataset')}>
              Dataset
            </button>
            <button type="button" className="nav-link" onClick={() => scrollToSection('backend')}>
              Backend
            </button>
            <button type="button" className="nav-link" onClick={() => scrollToSection('start')}>
              Quickstart
            </button>
          </nav>

          <div className="flex items-center gap-2 sm:gap-3">
            <button
              ref={triggerRef}
              type="button"
              className="kbd-chip"
              aria-label="Open command menu (Control K)"
              onClick={openPalette}
            >
              <Search size={13} aria-hidden />
              <span className="hidden sm:inline">Search</span>
              <span className="kbd hidden sm:inline" aria-hidden>Ctrl K</span>
            </button>
            <Link to="/signin" className="btn btn-primary">
              Sign in
            </Link>
          </div>
        </div>
      </header>

      <main id="main">
        {/* Stat-led hero */}
        <section className="mx-auto max-w-6xl px-4 pt-12 pb-16 sm:px-6 sm:pt-16 sm:pb-24">
          <div className="grid items-start gap-10 lg:grid-cols-2 lg:gap-12">
            <div className="reveal">
              <p className="label">Olist public dataset · 2016–2018</p>
              <h1 className="mt-4">
                <span className="figure block">{orders.toLocaleString('en-US')}</span>
                <span
                  className="mt-3 block text-[clamp(1.35rem,3.5vw,2rem)] font-medium leading-snug tracking-[-0.01em] text-ink-2"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  {headline}
                </span>
              </h1>
              <p className="mt-5 max-w-[46ch] text-[15px] leading-relaxed text-muted-foreground">
                ETL pipeline, FastAPI control plane, and React dashboard on the
                public Brazilian e-commerce dataset. Rows load in FK order into
                Supabase or Postgres.
              </p>
              <div className="mt-7 flex flex-wrap items-center gap-3">
                <Link to="/dashboard" className="btn btn-primary">
                  Open the dashboard <ArrowRight size={16} aria-hidden />
                </Link>
                <a
                  href={GH_REPO}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline"
                >
                  View source <ArrowUpRight size={16} aria-hidden />
                </a>
              </div>
              <div className="mt-6">
                <span className="chip chip-ok">23 tests passing · 2026-10-10</span>
              </div>
            </div>

            {/* graphite code block (Cobalt theme chrome — content only, no window frame) */}
            <div className="code-card reveal">
              <div className="cc-body">
                <div>
                  <span className="cc-prompt">$ </span>
                  <span className={typedDone ? '' : 'caret'}>{typed}</span>
                </div>
                {typedDone && (
                  <div className="cc-out">
                    <span className="cc-ok">15 passed</span> in 0.94s
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* supporting stats — hairline row */}
        <section id="dataset" aria-labelledby="dataset-h" className="reveal">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <h2 id="dataset-h" className="label mb-3">
              The dataset
            </h2>
            <div className="stat-row">
              {stats.map((s) => (
                <div key={s.label} className="stat">
                  <div className="stat-value">{s.value}</div>
                  <p className="label mt-1">{s.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* backend — asymmetric feature rows */}
        <section id="backend" aria-labelledby="backend-h" className="mx-auto max-w-6xl px-4 pt-14 sm:px-6">
          <div className="reveal">
            <h2 id="backend-h" className="label mb-3">
              The backend
            </h2>
            <div className="feature-grid">
              <div className="feature">
                <p className="label">ETL</p>
                <h3 className="mt-2 text-xl">
                  FK-ordered loads, pure transforms
                </h3>
                <p className="mt-3 max-w-[52ch] text-sm leading-relaxed text-muted-foreground">
                  One package, two load backends. <span className="mono text-ink-2">TABLE_ORDER</span> in{' '}
                  <span className="mono text-ink-2">etl/config.py</span> fixes the
                  load sequence for all 8 tables; every transform is a pure
                  DataFrame-in, DataFrame-out function with unit tests.
                </p>
                <ul className="mt-4 flex flex-wrap gap-2">
                  <li className="chip">supabase</li>
                  <li className="chip">postgres</li>
                  <li className="chip">CLI: python -m etl</li>
                </ul>
              </div>
              <div className="feature-narrow">
                <p className="label">API</p>
                <h3 className="mt-2 text-lg">3 endpoints</h3>
                <ul className="mono mt-3 space-y-1.5 text-xs text-muted-foreground">
                  <li>GET /health</li>
                  <li>POST /etl/run</li>
                  <li>POST /orders/generate</li>
                </ul>
              </div>
              <div className="feature-narrow">
                <p className="label">OrderGen</p>
                <h3 className="mt-2 text-lg">Synthetic orders</h3>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  A Markov model trained on live table distributions generates
                  plausible orders for demos.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* the one graphite band — quickstart */}
        <section id="start" aria-labelledby="start-h" className="band mt-16">
          <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
            <div className="reveal on-graphite">
              <h2 id="start-h" className="label">
                Quickstart
              </h2>
              <p className="mt-3 text-[clamp(1.5rem,4vw,2.25rem)] font-semibold tracking-[-0.02em]" style={{ fontFamily: 'var(--font-display)' }}>
                Three commands.
              </p>
              <div className="mt-6 max-w-2xl space-y-3">
                {QUICKSTART.map((cmd, i) => (
                  <div key={cmd} className="cmd-row">
                    <span className="text-graphite-muted" aria-hidden>
                      {i + 1}
                    </span>
                    <code className="min-w-0 flex-1 break-words">{cmd}</code>
                    <CopyBtn text={cmd} />
                  </div>
                ))}
              </div>
              <p className="mt-5 text-sm text-graphite-muted">
                Needs <span className="mono">data/</span> CSVs and database
                credentials in <span className="mono">.env</span>.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Ft2 inline single-line footer */}
      <footer className="border-t border-border">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-5 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <p>
            © 2026 BrazilBI · Olist public dataset (Kaggle, 2016–2018)
          </p>
          <div className="flex gap-5">
            <a href={GH_REPO} target="_blank" rel="noopener noreferrer" className="link-grow">
              GitHub
            </a>
            <a href={GH_DOCS} target="_blank" rel="noopener noreferrer" className="link-grow">
              Docs
            </a>
          </div>
        </div>
      </footer>

      {/* ⌘K palette */}
      {paletteOpen && (
        <div
          className="palette-overlay"
          onClick={(e) => {
            if (e.target === e.currentTarget) closePalette()
          }}
        >
          <div
            className="palette"
            role="dialog"
            aria-modal="true"
            aria-label="Command menu"
            onKeyDown={(e) => onPaletteKeyDown(e)}
          >
            <input
              ref={inputRef}
              className="palette-input"
              placeholder="Type a command…"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value)
                setCursor(0)
              }}
              aria-label="Command"
              aria-controls="palette-list"
            />
            <div className="palette-list" id="palette-list" role="listbox" aria-label="Results">
              {filtered.map((entry, i) => (
                <button
                  key={entry.label}
                  type="button"
                  role="option"
                  aria-selected={i === cursor}
                  className="palette-item"
                  onMouseEnter={() => setCursor(i)}
                  onClick={() => {
                    closePalette()
                    entry.run()
                  }}
                >
                  <span className="inline-flex items-center gap-2">
                    <LayoutDashboard size={14} aria-hidden className="text-muted-foreground" />
                    {entry.label}
                  </span>
                  <span className="label">{entry.hint}</span>
                </button>
              ))}
              {filtered.length === 0 && (
                <p className="px-3 py-4 text-sm text-muted-foreground">No matches.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
