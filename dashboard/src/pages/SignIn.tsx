import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export function SignIn() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)

  const handleDemoAccess = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setTimeout(() => {
      navigate('/dashboard')
    }, 800)
  }

  return (
    <div className="h-screen bg-background flex items-center justify-center px-4">
      {/* Background decoration */}
      <div className="absolute top-20 right-20 w-96 h-96 bg-primary/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 left-20 w-96 h-96 bg-foreground/5 rounded-full blur-3xl"></div>

      {/* Sign In Card */}
      <div className="relative w-full max-w-md">
        <div className="bg-card border border-border rounded-xl p-8 shadow-lg">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-3xl font-bold mb-2">
              <span className="text-foreground">Brazil</span>
              <span className="text-primary">BI</span>
            </div>
            <p className="text-muted-foreground">Sign in to access your dashboard</p>
          </div>

          {/* Form */}
          <form onSubmit={handleDemoAccess} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="demo@brazilbi.com"
                className="w-full px-4 py-3 bg-background border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition text-foreground placeholder:text-muted-foreground"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-background border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition text-foreground placeholder:text-muted-foreground"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <>
                  Sign In <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* Demo note */}
          <div className="mt-6 p-3 bg-primary/10 border border-primary/20 rounded-lg">
            <p className="text-sm text-primary text-center">
              Demo mode: Enter any credentials to access
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
