import { useSearchParams } from 'react-router-dom';
import { AppSidebar } from '../components/layout/app-sidebar';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '../components/ui/sidebar';
import { Separator } from '../components/ui/separator';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '../components/ui/breadcrumb';
import { useDashboardData } from '../hooks/use-dashboard-data';
import { OverviewTab } from '../components/dashboard/tabs/overview-tab';
import { AnalyticsTab } from '../components/dashboard/tabs/analytics-tab';
import { CustomersTab } from '../components/dashboard/tabs/customers-tab';
import { ProductsTab } from '../components/dashboard/tabs/products-tab';
import { SettingsTab } from '../components/dashboard/tabs/settings-tab';
import { OverviewTabSkeleton, AnalyticsTabSkeleton, CustomersTabSkeleton, ProductsTabSkeleton } from '../components/dashboard/skeleton-loaders';

export function Dashboard() {
  const { data, loading, error, retry } = useDashboardData();
  const [searchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';

  const renderSkeleton = () => {
    switch (tab) {
      case 'analytics':
        return <AnalyticsTabSkeleton />;
      case 'customers':
        return <CustomersTabSkeleton />;
      case 'products':
        return <ProductsTabSkeleton />;
      case 'settings':
        return null;
      default:
        return <OverviewTabSkeleton />;
    }
  };

  const renderTab = () => {
    switch (tab) {
      case 'analytics':
        return <AnalyticsTab data={data} />;
      case 'customers':
        return <CustomersTab data={data} />;
      case 'products':
        return <ProductsTab data={data} />;
      case 'settings':
        return <SettingsTab />;
      default:
        return <OverviewTab data={data} />;
    }
  };

  const getTitle = () => {
    switch (tab) {
      case 'analytics': return 'Analytics';
      case 'customers': return 'Customers';
      case 'products': return 'Products';
      case 'settings': return 'Settings';
      default: return 'Dashboard Overview';
    }
  };

  return (
    <SidebarProvider>
      <a
        href="#dashboard-main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-[6px] focus:border focus:border-border focus:bg-background focus:px-4 focus:py-2 focus:text-sm"
      >
        Skip to content
      </a>
      <AppSidebar metrics={data?.kpis?.totalRevenue ? {
        revenue: data.kpis.totalRevenue,
        orders: data.kpis.totalOrders,
        customers: data.kpis.uniqueCustomers
      } : undefined} />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b border-border px-4 bg-background">
          <SidebarTrigger className="-ml-1" aria-label="Toggle sidebar" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink href="/">Home</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              {tab !== 'overview' && (
                <>
                  <BreadcrumbSeparator />
                  <BreadcrumbItem>
                    <BreadcrumbPage className="capitalize">{tab}</BreadcrumbPage>
                  </BreadcrumbItem>
                </>
              )}
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div id="dashboard-main" className="flex flex-1 flex-col gap-4 p-4 bg-background">
          <div className="flex flex-col gap-1 pt-2">
            <p className="label">Olist dataset · 2016–2018</p>
            <h1 className="text-2xl font-semibold tracking-[-0.02em]" style={{ fontFamily: 'var(--font-display)' }}>
              {getTitle()}
            </h1>
          </div>

          {loading ? (
            <div className="space-y-4">
              {renderSkeleton()}
            </div>
          ) : error ? (
            <div className="flex flex-col items-start gap-3 rounded-[10px] border border-destructive/40 bg-destructive/5 p-4" role="alert">
              <div>
                <p className="text-sm font-medium text-destructive">Dashboard data unavailable</p>
                <p className="mono mt-1 break-all text-xs text-muted-foreground">{error}</p>
              </div>
              <button type="button" className="btn btn-outline" onClick={retry}>
                Retry
              </button>
            </div>
          ) : (
            <div key={tab} className="tab-panel">
              {renderTab()}
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
