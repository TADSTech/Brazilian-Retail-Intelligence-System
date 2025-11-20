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
} from '@/components/ui/sidebar'

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

export function AppSidebar() {
  const location = useLocation()

  return (
    <Sidebar collapsible="icon" className="border-r border-gray-200 bg-white">
      <SidebarHeader className="border-b border-gray-200 bg-white">
        <SidebarMenu>
          <SidebarMenuItem>
            <Link to="/" className="w-full">
              <SidebarMenuButton size="lg" tooltip="BrazilBI" className="hover:bg-gray-50 transition-colors w-full group-data-[collapsible=icon]:justify-center">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-orange-600 text-white shrink-0">
                  <Home className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none group-data-[collapsible=icon]:hidden">
                  <span className="font-semibold text-sm text-gray-900">BrazilBI</span>
                  <span className="text-xs text-gray-500">Retail Analytics</span>
                </div>
              </SidebarMenuButton>
            </Link>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      
      <SidebarContent className="px-2">
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium text-gray-500 uppercase tracking-wide px-2">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="gap-1">
              {menuItems.map((item) => {
                const isActive = location.pathname === item.url.split('?')[0]
                return (
                  <SidebarMenuItem key={item.title}>
                    <Link to={item.url} className="w-full">
                      <SidebarMenuButton
                        tooltip={item.title}
                        className={`w-full transition-colors group-data-[collapsible=icon]:justify-center ${
                          isActive
                            ? 'bg-orange-50 text-orange-700 hover:bg-orange-100'
                            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                        }`}
                      >
                        <item.icon className="size-5 shrink-0" />
                        <span className="font-medium group-data-[collapsible=icon]:hidden">{item.title}</span>
                        {item.badge && isActive && (
                          <span className="ml-auto inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium bg-orange-100 text-orange-700 border border-orange-200 group-data-[collapsible=icon]:hidden">
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

        <div className="my-4 h-px bg-gray-200 mx-2" />

        <div className="px-2 pb-3 group-data-[collapsible=icon]:hidden">
          <div className="bg-orange-50 rounded-lg p-3 border border-orange-100">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="size-4 text-orange-600" />
              <p className="text-xs font-semibold text-gray-900">Key Metrics</p>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-600">Revenue</span>
                <span className="font-semibold text-gray-900">$8.2M</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Orders</span>
                <span className="font-semibold text-gray-900">97.6K</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Records</span>
                <span className="font-semibold text-gray-900">1.2M+</span>
              </div>
            </div>
          </div>
        </div>
      </SidebarContent>
      
      <SidebarFooter className="border-t border-gray-200 bg-white">
        <SidebarMenu>
          <SidebarMenuItem>
            <Link to="/" className="w-full">
              <SidebarMenuButton tooltip="Logout" className="hover:bg-red-50 hover:text-red-700 transition-colors text-gray-700 w-full group-data-[collapsible=icon]:justify-center">
                <div className="flex items-center justify-center rounded-md bg-red-50 p-1.5 shrink-0">
                  <LogOut className="size-4 text-red-600" />
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
