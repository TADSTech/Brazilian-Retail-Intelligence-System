import { RevenueChart } from '../revenue-chart';
import { OrderStatusChart } from '../order-status-chart';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import Plot from 'react-plotly.js';
import { Package, Clock, CreditCard, Truck } from 'lucide-react';

interface AnalyticsTabProps {
  data: any;
}

export function AnalyticsTab({ data }: AnalyticsTabProps) {
  const { revenueTrend, orderStatus, analytics } = data;

  if (!analytics) {
    return (
      <div className="space-y-4">
        <Card>
          <CardContent className="py-8">
            <p className="text-center text-muted-foreground">Loading analytics...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Delivery Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.avgDeliveryDays.toFixed(1)} days</div>
            <p className="text-xs text-muted-foreground">From purchase to delivery</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">On-Time Delivery</CardTitle>
            <Truck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.onTimeDeliveryRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">Orders delivered on time</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Top Payment Method</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">{analytics.topPaymentMethod?.type || 'N/A'}</div>
            <p className="text-xs text-muted-foreground">{analytics.topPaymentMethod?.percentage.toFixed(1)}% of transactions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Installments</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.avgInstallments.toFixed(1)}x</div>
            <p className="text-xs text-muted-foreground">Average payment splits</p>
          </CardContent>
        </Card>
      </div>

      {/* Revenue and Order Status */}
      <div className="grid gap-4 md:grid-cols-1">
        <RevenueChart data={revenueTrend} />
      </div>
      
      <div className="grid gap-4 md:grid-cols-2">
        <OrderStatusChart data={orderStatus} />
        
        {/* Payment Methods Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Payment Methods</CardTitle>
            <CardDescription>Distribution by transaction count</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <Plot
                data={[
                  {
                    values: analytics.paymentMethods.map((p: any) => p.count),
                    labels: analytics.paymentMethods.map((p: any) => p.type),
                    type: 'pie',
                    marker: {
                      colors: ['#ea580c', '#fb923c', '#fdba74', '#fed7aa']
                    },
                    textinfo: 'label+percent',
                    textposition: 'outside',
                    automargin: true
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 20, r: 20, t: 20, b: 20 },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  showlegend: false,
                  font: {
                    color: 'hsl(var(--muted-foreground))'
                  }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Delivery Performance & Installment Distribution */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Delivery Lead Time Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Delivery Lead Time</CardTitle>
            <CardDescription>Order distribution by delivery time</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <Plot
                data={[
                  {
                    x: analytics.deliveryDistribution.map((d: any) => d.range),
                    y: analytics.deliveryDistribution.map((d: any) => d.count),
                    type: 'bar',
                    marker: { color: '#ea580c' }
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 50, r: 20, t: 20, b: 80 },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  xaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                  },
                  yaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                    title: { text: 'Number of Orders' }
                  }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Installment Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Payment Installments</CardTitle>
            <CardDescription>Distribution of payment splits</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <Plot
                data={[
                  {
                    x: analytics.installmentDistribution.map((i: any) => `${i.installments}x`),
                    y: analytics.installmentDistribution.map((i: any) => i.count),
                    type: 'bar',
                    marker: { color: '#ea580c' }
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 50, r: 20, t: 20, b: 60 },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  xaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                  },
                  yaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                    title: { text: 'Number of Payments' }
                  }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
