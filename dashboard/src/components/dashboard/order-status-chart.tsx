import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

interface OrderStatusChartProps {
  data: { status: string; count: number }[];
}

export function OrderStatusChart({ data }: OrderStatusChartProps) {
  return (
    <Card className="col-span-4">
      <CardHeader>
        <CardTitle>Order Status Distribution</CardTitle>
        <CardDescription>Breakdown of orders by their current status</CardDescription>
      </CardHeader>
      <CardContent className="pl-2">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <XAxis
              dataKey="status"
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip 
                contentStyle={{ backgroundColor: 'white', borderRadius: '8px' }}
                cursor={{ fill: 'transparent' }}
            />
            <Bar dataKey="count" fill="#ea580c" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
