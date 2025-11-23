import { ArrowRight, BarChart3, Database, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Home() {
  return (
    <div className="h-screen bg-background flex flex-col overflow-hidden">
      <nav className="py-2 px-8 mt-0 flex items-center justify-between shrink-0">
        <div className="text-2xl font-bold">
          <span className="text-foreground">Brazil</span>
          <span className="text-primary">BI</span>
        </div>
        <Link
          to="/signin"
          className="px-6 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors font-medium"
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
              <h1 className="text-5xl font-bold text-foreground leading-tight">
                Brazilian Retail
                <br />
                <span className="text-primary">Business Intelligence</span>
              </h1>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Comprehensive retail analytics platform with 1.2M+ records across 8 data tables. Real-time insights into sales, revenue, and customer behavior.
              </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <div className="text-2xl font-bold text-foreground">1.2M+</div>
                <p className="text-sm text-muted-foreground">Records</p>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-foreground">$8.2M</div>
                <p className="text-sm text-muted-foreground">Revenue</p>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-bold text-foreground">97.6K</div>
                <p className="text-sm text-muted-foreground">Orders</p>
              </div>
            </div>

            {/* CTA */}
            <div className="flex gap-4">
              <Link
                to="/signin"
                className="px-8 py-3 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors font-semibold flex items-center gap-2"
              >
                Get Started <ArrowRight size={18} />
              </Link>
            </div>

            {/* Tech Stack */}
            <div className="pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground mb-3">Built with</p>
              <div className="flex flex-wrap gap-3 text-sm">
                <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full">React</span>
                <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full">TypeScript</span>
                <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full">PostgreSQL</span>
                <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full">Python</span>
              </div>
            </div>
          </div>

          {/* Right: Visual */}
          <div className="hidden lg:block relative">
            {/* Background shapes */}
            <div className="absolute -top-8 -right-8 w-64 h-64 bg-primary/5 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-8 -left-8 w-64 h-64 bg-foreground/5 rounded-full blur-3xl"></div>

            {/* Feature Cards */}
            <div className="relative space-y-4">
              <div className="bg-card border-2 border-primary rounded-xl p-6 shadow-lg">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center shrink-0">
                    <BarChart3 size={24} className="text-primary-foreground" />
                  </div>
                  <div>
                    <h3 className="font-bold text-foreground mb-1">Analytics Dashboard</h3>
                    <p className="text-sm text-muted-foreground">Real-time KPIs and revenue tracking</p>
                  </div>
                </div>
              </div>

              <div className="bg-card border-2 border-border rounded-xl p-6 shadow-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-foreground rounded-lg flex items-center justify-center shrink-0">
                    <Database size={24} className="text-background" />
                  </div>
                  <div>
                    <h3 className="font-bold text-foreground mb-1">Data Processing</h3>
                    <p className="text-sm text-muted-foreground">ETL pipeline with 8 data tables</p>
                  </div>
                </div>
              </div>

              <div className="bg-card border-2 border-border rounded-xl p-6 shadow-md">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center shrink-0">
                    <TrendingUp size={24} className="text-primary-foreground" />
                  </div>
                  <div>
                    <h3 className="font-bold text-foreground mb-1">Insights & Reports</h3>
                    <p className="text-sm text-muted-foreground">Category analysis and trends</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-border px-8 py-4 flex items-center justify-between text-sm text-muted-foreground shrink-0">
        <p>&copy; 2024 BrazilBI</p>
        <div className="flex gap-6">
          <a href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System" className="hover:text-foreground transition">GitHub</a>
          <a href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System/tree/main/docs" className="hover:text-foreground transition">Docs</a>
        </div>
      </footer>
    </div>
  )
}
