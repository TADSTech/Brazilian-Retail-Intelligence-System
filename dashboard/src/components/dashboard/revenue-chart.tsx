import Plot from 'react-plotly.js';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface RevenueChartProps {
  data: { date: string; revenue: number }[];
}

export function RevenueChart({ data }: RevenueChartProps) {
  // Prepare data for Plotly
  const dates = data.map(d => d.date);
  const revenues = data.map(d => d.revenue);

  return (
    <Card className="col-span-1 sm:col-span-2 md:col-span-2 lg:col-span-4">
      <CardHeader>
        <CardTitle>Revenue Trend</CardTitle>
      </CardHeader>
      <CardContent className="pl-2">
        <div className="h-[250px] sm:h-[300px] md:h-[350px] w-full">
          <Plot
            data={[
              {
                x: dates,
                y: revenues,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: '#ea580c' },
                line: { shape: 'spline', color: '#ea580c' },
                fill: 'tozeroy',
                fillcolor: 'rgba(234, 88, 12, 0.1)',
              },
            ]}
            layout={{
              autosize: true,
              margin: { l: 50, r: 20, t: 20, b: 40 },
              showlegend: false,
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              xaxis: {
                showgrid: false,
                zeroline: false,
                tickfont: { color: 'hsl(var(--muted-foreground))' },
              },
              yaxis: {
                showgrid: true,
                gridcolor: 'hsla(var(--border), 0.5)',
                zeroline: false,
                tickfont: { color: 'hsl(var(--muted-foreground))' },
                tickprefix: 'R$ ',
              },
            }}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%' }}
            config={{ displayModeBar: false }}
          />
        </div>
      </CardContent>
    </Card>
  );
}
