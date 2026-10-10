import Plot from 'react-plotly.js';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { CHART } from "../../lib/chart-colors";

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
          <div className="h-[250px] sm:h-[300px] md:h-[350px] w-full" role="img" aria-label="Revenue trend over time">
          <Plot
            data={[
              {
                x: dates,
                y: revenues,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: CHART.accent },
                line: { shape: 'spline', color: CHART.accent },
                fill: 'tozeroy',
                fillcolor: CHART.accentSoft,
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
                tickfont: { color: CHART.text },
              },
              yaxis: {
                showgrid: true,
                gridcolor: CHART.grid,
                zeroline: false,
                tickfont: { color: CHART.text },
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
