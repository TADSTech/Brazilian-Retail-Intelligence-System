import { useSearchParams } from 'react-router-dom';
import { AppSidebar } from '@/components/layout/app-sidebar';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';
import { Separator } from '@/components/ui/separator';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';
import { useDashboardData } from '@/hooks/use-dashboard-data';
import { Loader2 } from 'lucide-react';
import { OverviewTab } from '@/components/dashboard/tabs/overview-tab';
import { AnalyticsTab } from '@/components/dashboard/tabs/analytics-tab';
import { CustomersTab } from '@/components/dashboard/tabs/customers-tab';
import { ProductsTab } from '@/components/dashboard/tabs/products-tab';
import { SettingsTab } from '@/components/dashboard/tabs/settings-tab';

export function Dashboard() {
  const { data, loading, error } = useDashboardData();
  const [searchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';

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
      <AppSidebar metrics={data?.kpis?.totalRevenue ? {
        revenue: data.kpis.totalRevenue,
        orders: data.kpis.totalOrders,
        customers: data.kpis.uniqueCustomers
      } : undefined} />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4 bg-background">
          <SidebarTrigger className="-ml-1" />
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
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0 bg-muted/20">
          <div className="flex items-center justify-between py-4">
            <h1 className="text-3xl font-bold tracking-tight text-foreground">{getTitle()}</h1>
          </div>

          {loading ? (
            <div className="flex h-[50vh] items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : error ? (
            <div className="rounded-lg border border-destructive/20 bg-destructive/10 p-4 text-destructive">
              Error loading dashboard data: {error}
            </div>
          ) : (
            renderTab()
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
