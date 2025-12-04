import Plot from 'react-plotly.js';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface CategoryChartProps {
  data: { category: string; revenue: number }[];
}

export function CategoryChart({ data }: CategoryChartProps) {
  const categories = data.map(d => d.category.replace(/_/g, ' '));
  const revenues = data.map(d => d.revenue);

  return (
    <Card className="col-span-1 sm:col-span-2 md:col-span-2 lg:col-span-2">
      <CardHeader>
        <CardTitle>Top Categories by Revenue</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[250px] sm:h-[300px] md:h-[350px] w-full">
          <Plot
            data={[
              {
                x: revenues,
                y: categories,
                type: 'bar',
                orientation: 'h',
                marker: {
                  color: '#ea580c',
                  opacity: 0.8,
                },
              },
            ]}
            layout={{
              autosize: true,
              margin: { l: 150, r: 20, t: 20, b: 40 },
              showlegend: false,
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              xaxis: {
                showgrid: true,
                gridcolor: 'hsla(var(--border), 0.5)',
                zeroline: false,
                tickfont: { color: 'hsl(var(--muted-foreground))' },
                tickprefix: 'R$ ',
              },
              yaxis: {
                showgrid: false,
                zeroline: false,
                tickfont: { color: 'hsl(var(--muted-foreground))', size: 10 },
                automargin: true,
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
