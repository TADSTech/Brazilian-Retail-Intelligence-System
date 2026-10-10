import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { CHART } from '../../lib/chart-colors';

interface OrderStatusChartProps {
  data: { status: string; count: number }[];
}

export function OrderStatusChart({ data }: OrderStatusChartProps) {
  return (
    <Card className="col-span-1 sm:col-span-2 md:col-span-2 lg:col-span-4">
      <CardHeader>
        <CardTitle>Order Status Distribution</CardTitle>
        <CardDescription>Breakdown of orders by their current status</CardDescription>
      </CardHeader>
      <CardContent className="pl-2">
        <div role="img" aria-label="Order status distribution chart">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <XAxis
              dataKey="status"
              stroke={CHART.text}
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke={CHART.text}
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip 
                contentStyle={{ backgroundColor: CHART.paper, border: `1px solid ${CHART.rule2}`, borderRadius: 6, fontSize: 12 }}
                cursor={{ fill: 'transparent' }}
            />
            <Bar dataKey="count" fill={CHART.accent} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
