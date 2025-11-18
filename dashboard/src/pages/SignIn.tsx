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
    <div className="h-screen bg-white flex items-center justify-center px-4">
      {/* Background decoration */}
      <div className="absolute top-20 right-20 w-96 h-96 bg-orange-600/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 left-20 w-96 h-96 bg-black/5 rounded-full blur-3xl"></div>

      {/* Sign In Card */}
      <div className="relative w-full max-w-md">
        <div className="bg-white border-2 border-gray-200 rounded-xl p-8 shadow-lg">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-3xl font-bold mb-2">
              <span className="text-black">Brazil</span>
              <span className="text-orange-600">BI</span>
            </div>
            <p className="text-gray-600">Sign in to access your dashboard</p>
          </div>

          {/* Form */}
          <form onSubmit={handleDemoAccess} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="demo@brazilbi.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-600 focus:border-transparent outline-none transition"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-600 focus:border-transparent outline-none transition"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <>
                  Sign In <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          {/* Demo note */}
          <div className="mt-6 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <p className="text-sm text-orange-900 text-center">
              Demo mode: Enter any credentials to access
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
