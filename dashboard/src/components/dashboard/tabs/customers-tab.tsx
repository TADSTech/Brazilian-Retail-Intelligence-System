import { CustomerMap } from '../customer-map';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import Plot from 'react-plotly.js';

interface CustomersTabProps {
  data: any;
}

export function CustomersTab({ data }: CustomersTabProps) {
  const { customerGeo, customerBehavior, customerSatisfaction } = data;

  return (
    <div className="space-y-4">
      {/* Customer Distribution Map and Top Locations */}
      <div className="grid gap-4 md:grid-cols-2">
        <CustomerMap data={customerGeo} />
        
        <Card>
          <CardHeader>
            <CardTitle>Top Customer Locations</CardTitle>
            <CardDescription>Cities with the highest number of customers</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {customerGeo.slice(0, 10).map((item: any, index: number) => (
                <div key={item.zip} className="flex items-center">
                  <div className="w-8 font-medium text-muted-foreground">{index + 1}</div>
                  <div className="flex-1 font-medium">{item.city}, {item.state}</div>
                  <div className="text-muted-foreground">{item.count.toLocaleString()} customers</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Customer Behavior Analytics */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Repeat Purchase Rate */}
        <Card>
          <CardHeader>
            <CardTitle>Customer Loyalty</CardTitle>
            <CardDescription>Repeat purchase rate</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-primary">
                {customerBehavior.repeatRate.toFixed(1)}%
              </div>
              <p className="text-sm text-muted-foreground">
                Customers who made more than one purchase
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Average Review Score */}
        <Card>
          <CardHeader>
            <CardTitle>Customer Satisfaction</CardTitle>
            <CardDescription>Average review score</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-primary">
                {customerSatisfaction.avgScore.toFixed(2)} / 5.0
              </div>
              <p className="text-sm text-muted-foreground">
                Based on {customerSatisfaction.scoreDistribution.reduce((sum: number, s: any) => sum + s.count, 0).toLocaleString()} reviews
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* New vs Returning Customers */}
      <Card>
        <CardHeader>
          <CardTitle>Customer Acquisition Trends</CardTitle>
          <CardDescription>New vs returning customers over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <Plot
              data={[
                {
                  x: customerBehavior.newVsReturning.map((d: any) => d.month),
                  y: customerBehavior.newVsReturning.map((d: any) => d.new),
                  name: 'New Customers',
                  type: 'scatter',
                  mode: 'lines+markers',
                  line: { color: '#ea580c', width: 2 },
                  marker: { size: 6 }
                },
                {
                  x: customerBehavior.newVsReturning.map((d: any) => d.month),
                  y: customerBehavior.newVsReturning.map((d: any) => d.returning),
                  name: 'Returning Customers',
                  type: 'scatter',
                  mode: 'lines+markers',
                  line: { color: '#0ea5e9', width: 2 },
                  marker: { size: 6 }
                }
              ]}
              layout={{
                autosize: true,
                margin: { l: 50, r: 20, t: 20, b: 40 },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                xaxis: {
                  color: 'hsl(var(--muted-foreground))',
                  gridcolor: 'hsla(var(--border), 0.3)',
                },
                yaxis: {
                  color: 'hsl(var(--muted-foreground))',
                  gridcolor: 'hsla(var(--border), 0.3)',
                  title: { text: 'Number of Customers' }
                },
                legend: {
                  font: { color: 'hsl(var(--muted-foreground))' },
                  orientation: 'h',
                  y: 1.1
                },
                hovermode: 'x unified'
              }}
              config={{ displayModeBar: false }}
              style={{ width: '100%', height: '100%' }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Review Score Distribution & Delivery Impact */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Review Score Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Review Score Distribution</CardTitle>
            <CardDescription>Breakdown of customer ratings</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <Plot
                data={[
                  {
                    x: customerSatisfaction.scoreDistribution.map((d: any) => `${d.score} Stars`),
                    y: customerSatisfaction.scoreDistribution.map((d: any) => d.count),
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
                    title: { text: 'Number of Reviews' }
                  }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Delivery Performance Impact */}
        <Card>
          <CardHeader>
            <CardTitle>Delivery Impact on Satisfaction</CardTitle>
            <CardDescription>Review scores by delivery status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <Plot
                data={[
                  {
                    x: customerSatisfaction.deliveryCorrelation.map((d: any) => d.status),
                    y: customerSatisfaction.deliveryCorrelation.map((d: any) => d.avgScore),
                    type: 'bar',
                    marker: { color: ['#22c55e', '#ef4444'] },
                    text: customerSatisfaction.deliveryCorrelation.map((d: any) => d.avgScore.toFixed(2)),
                    textposition: 'outside'
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
                    title: { text: 'Average Review Score' },
                    range: [0, 5]
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
