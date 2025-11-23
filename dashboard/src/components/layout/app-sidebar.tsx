import { Home, LayoutDashboard, Users, Package, Settings, BarChart3, LogOut, Zap } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
} from '../ui/sidebar'

interface AppSidebarProps extends React.ComponentProps<typeof Sidebar> {
  metrics?: {
    revenue: number;
    orders: number;
    customers: number;
  }
}

const menuItems = [
  {
    title: 'Dashboard',
    url: '/dashboard',
    icon: LayoutDashboard,
    badge: 'Live',
  },
  {
    title: 'Analytics',
    url: '/dashboard?tab=analytics',
    icon: BarChart3,
  },
  {
    title: 'Customers',
    url: '/dashboard?tab=customers',
    icon: Users,
  },
  {
    title: 'Products',
    url: '/dashboard?tab=products',
    icon: Package,
  },
  {
    title: 'Settings',
    url: '/dashboard?tab=settings',
    icon: Settings,
  },
]

export function AppSidebar({ metrics, ...props }: AppSidebarProps) {
  const location = useLocation()

  const formatValue = (val: number, prefix = '') => {
    if (val >= 1000000) return `${prefix}${(val / 1000000).toFixed(1)}M`;
    if (val >= 1000) return `${prefix}${(val / 1000).toFixed(1)}K`;
    return `${prefix}${val}`;
  }

  const revenueDisplay = metrics ? formatValue(metrics.revenue, '$') : '$8.2M';
  const ordersDisplay = metrics ? formatValue(metrics.orders) : '97.6K';
  const customersDisplay = metrics ? formatValue(metrics.customers) : '1.2M+';

  return (
    <Sidebar collapsible="icon" className="border-r border-border bg-sidebar" {...props}>
      <SidebarHeader className="border-b border-border bg-sidebar">
        <SidebarMenu>
          <SidebarMenuItem>
            <Link to="/" className="w-full">
              <SidebarMenuButton size="lg" tooltip="BrazilBI" className="hover:bg-sidebar-accent transition-colors w-full group-data-[collapsible=icon]:justify-center">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground shrink-0">
                  <Home className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none group-data-[collapsible=icon]:hidden">
                  <span className="font-semibold text-sm text-sidebar-foreground">BrazilBI</span>
                  <span className="text-xs text-muted-foreground">Retail Analytics</span>
                </div>
              </SidebarMenuButton>
            </Link>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      
      <SidebarContent className="px-2">
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium text-muted-foreground uppercase tracking-wide px-2">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="gap-1">
              {menuItems.map((item) => {
                const currentTab = new URLSearchParams(location.search).get('tab') || 'overview'
                const itemTab = new URLSearchParams(item.url.split('?')[1] || '').get('tab') || 'overview'
                const isActive = location.pathname === item.url.split('?')[0] && currentTab === itemTab
                return (
                  <SidebarMenuItem key={item.title}>
                    <Link to={item.url} className="w-full">
                      <SidebarMenuButton
                        tooltip={item.title}
                        className={`w-full transition-colors group-data-[collapsible=icon]:justify-center ${
                          isActive
                            ? 'bg-sidebar-accent text-sidebar-accent-foreground hover:bg-sidebar-accent/90'
                            : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                        }`}
                      >
                        <item.icon className="size-5 shrink-0" />
                        <span className="font-medium group-data-[collapsible=icon]:hidden">{item.title}</span>
                        {item.badge && isActive && (
                          <span className="ml-auto inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium bg-primary/10 text-primary border border-primary/20 group-data-[collapsible=icon]:hidden">
                            {item.badge}
                          </span>
                        )}
                      </SidebarMenuButton>
                    </Link>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <div className="my-4 h-px bg-border mx-2" />

        <div className="px-2 pb-3 group-data-[collapsible=icon]:hidden">
          <div className="bg-sidebar-accent/50 rounded-lg p-3 border border-sidebar-border">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="size-4 text-primary" />
              <p className="text-xs font-semibold text-sidebar-foreground">Key Metrics</p>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Revenue</span>
                <span className="font-semibold text-sidebar-foreground">{revenueDisplay}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Orders</span>
                <span className="font-semibold text-sidebar-foreground">{ordersDisplay}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Customers</span>
                <span className="font-semibold text-sidebar-foreground">{customersDisplay}</span>
              </div>
            </div>
          </div>
        </div>
      </SidebarContent>
      
      <SidebarFooter className="border-t border-border bg-sidebar">
        <SidebarMenu>
          <SidebarMenuItem>
            <Link to="/" className="w-full">
              <SidebarMenuButton tooltip="Logout" className="hover:bg-destructive/10 hover:text-destructive transition-colors text-sidebar-foreground w-full group-data-[collapsible=icon]:justify-center">
                <div className="flex items-center justify-center rounded-md bg-destructive/10 p-1.5 shrink-0">
                  <LogOut className="size-4 text-destructive" />
                </div>
                <span className="font-medium group-data-[collapsible=icon]:hidden">Logout</span>
              </SidebarMenuButton>
            </Link>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
