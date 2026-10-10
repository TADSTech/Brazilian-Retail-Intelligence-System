import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { BbiLogo } from '../components/bbi-logo'

type FieldErrors = { email?: string; password?: string }

function validate(email: string, password: string): FieldErrors {
  const errors: FieldErrors = {}
  if (!email.trim()) errors.email = 'Email is required.'
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim()))
    errors.email = 'Enter a valid email address.'
  if (!password) errors.password = 'Password is required.'
  return errors
}

export function SignIn() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [touched, setTouched] = useState<{ email?: boolean; password?: boolean }>({})
  const [errors, setErrors] = useState<FieldErrors>({})
  const [isLoading, setIsLoading] = useState(false)

  const blur = (field: 'email' | 'password') => {
    setTouched((t) => ({ ...t, [field]: true }))
    setErrors(validate(email, password))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const found = validate(email, password)
    setErrors(found)
    setTouched({ email: true, password: true })
    if (Object.keys(found).length > 0) return
    setIsLoading(true)
    window.setTimeout(() => navigate('/dashboard'), 800)
  }

  const emailError = touched.email ? errors.email : undefined
  const passwordError = touched.password ? errors.password : undefined

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="flex h-14 shrink-0 items-center px-4 sm:px-6">
        <Link to="/" className="flex items-center gap-2 text-lg font-semibold tracking-tight" style={{ fontFamily: 'var(--font-display)' }}>
          <BbiLogo className="size-7" />
          <span className="text-foreground">Brazil</span>
          <span className="text-primary">BI</span>
        </Link>
      </header>

      <main className="flex flex-1 items-center justify-center px-4 py-10">
        <div className="w-full max-w-sm">
          {/* hairline card — 10px, no elevation */}
          <div className="rounded-[10px] border border-border bg-card p-6 sm:p-8">
            <p className="label">Account</p>
            <h1 className="mt-2 text-2xl" style={{ fontFamily: 'var(--font-display)' }}>
              Sign in
            </h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Demo mode — any credentials open the dashboard.
            </p>

            <form onSubmit={handleSubmit} noValidate className="mt-6 space-y-4">
              <div>
                <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-foreground">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  placeholder="demo@brazilbi.com"
                  className="field"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onBlur={() => blur('email')}
                  aria-invalid={emailError ? true : undefined}
                  aria-describedby="email-help"
                  disabled={isLoading}
                />
                <span
                  id="email-help"
                  className="field-help"
                  data-state={emailError ? 'error' : undefined}
                >
                  {emailError ?? ' '}
                </span>
              </div>

              <div>
                <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-foreground">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  placeholder="••••••••"
                  className="field"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onBlur={() => blur('password')}
                  aria-invalid={passwordError ? true : undefined}
                  aria-describedby="password-help"
                  disabled={isLoading}
                />
                <span
                  id="password-help"
                  className="field-help"
                  data-state={passwordError ? 'error' : undefined}
                >
                  {passwordError ?? ' '}
                </span>
              </div>

              <button type="submit" className="btn btn-primary w-full" disabled={isLoading} aria-busy={isLoading}>
                {isLoading ? (
                  <>
                    <span
                      className="size-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"
                      aria-hidden
                    />
                    Signing in…
                  </>
                ) : (
                  'Sign in'
                )}
              </button>
            </form>
          </div>

          <p className="mt-5 text-center text-sm text-muted-foreground">
            <Link to="/" className="link-grow">
              ← Back to overview
            </Link>
          </p>
        </div>
      </main>
    </div>
  )
}
