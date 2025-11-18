import { ArrowRight, BarChart3, Database, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Home() {
  return (
    <div className="h-screen bg-white flex flex-col overflow-hidden">
      <nav className="py-2 px-8 mt-0 flex items-center justify-between shrink-0">
        <div className="text-2xl font-bold">
          <span className="text-black">Brazil</span>
          <span className="text-orange-600">BI</span>
        </div>
        <Link
          to="/signin"
          className="px-6 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors font-medium"
        >
          Sign In
        </Link>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-8 overflow-auto">
        <div className="max-w-5xl w-full grid lg:grid-cols-2 gap-16 items-center py-12">
          {/* Left: Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl font-bold text-black leading-tight">
                Brazilian Retail
                <br />
                <span className="text-orange-600">Business Intelligence</span>
              </h1>
              <p className="text-lg text-gray-600 leading-relaxed">
                Comprehensive retail analytics platform with 1.2M+ records across 8 data tables. Real-time insights into sales, revenue, and customer behavior.
              </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <div className="text-2xl font-bold text-black">1.2M+</div>
                <p className="text-sm text-gray-600">Records</p>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-black">$8.2M</div>
                <p className="text-sm text-gray-600">Revenue</p>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-black">97.6K</div>
                <p className="text-sm text-gray-600">Orders</p>
              </div>
            </div>

            {/* CTA */}
            <div className="flex gap-4">
              <Link
                to="/signin"
                className="px-8 py-3 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors font-semibold flex items-center gap-2"
              >
                Get Started <ArrowRight size={18} />
              </Link>
            </div>

            {/* Tech Stack */}
            <div className="pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500 mb-3">Built with</p>
              <div className="flex flex-wrap gap-3 text-sm">
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full">React</span>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full">TypeScript</span>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full">PostgreSQL</span>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full">Python</span>
              </div>
            </div>
          </div>

          {/* Right: Visual */}
          <div className="hidden lg:block relative">
            {/* Background shapes */}
            <div className="absolute -top-8 -right-8 w-64 h-64 bg-orange-600/5 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-8 -left-8 w-64 h-64 bg-black/5 rounded-full blur-3xl"></div>

            {/* Feature Cards */}
            <div className="relative space-y-4">
              <div className="bg-white border-2 border-black rounded-xl p-6 shadow-lg">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-orange-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <BarChart3 size={24} className="text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-black mb-1">Analytics Dashboard</h3>
                    <p className="text-sm text-gray-600">Real-time KPIs and revenue tracking</p>
                  </div>
                </div>
              </div>

              <div className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gray-900 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Database size={24} className="text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-black mb-1">Data Processing</h3>
                    <p className="text-sm text-gray-600">ETL pipeline with 8 data tables</p>
                  </div>
                </div>
              </div>

              <div className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-orange-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <TrendingUp size={24} className="text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-black mb-1">Insights & Reports</h3>
                    <p className="text-sm text-gray-600">Category analysis and trends</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-200 px-8 py-4 flex items-center justify-between text-sm text-gray-600 flex-shrink-0">
        <p>&copy; 2024 BrazilBI</p>
        <div className="flex gap-6">
          <a href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System" className="hover:text-black transition">GitHub</a>
          <a href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System/tree/main/docs" className="hover:text-black transition">Docs</a>
        </div>
      </footer>
    </div>
  )
}
