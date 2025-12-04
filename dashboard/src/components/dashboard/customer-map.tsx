import Plot from 'react-plotly.js';
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface CustomerMapProps {
  data: { zip: string; lat: number; lon: number; city: string; state: string; count: number }[];
}

export function CustomerMap({ data }: CustomerMapProps) {
  const lats = data.map(d => d.lat);
  const lons = data.map(d => d.lon);
  const counts = data.map(d => d.count);
  const texts = data.map(d => `${d.city}, ${d.state}: ${d.count} customers`);

  return (
    <Card className="col-span-1 sm:col-span-2 md:col-span-3 lg:col-span-3">
      <CardHeader>
        <CardTitle>Customer Distribution (Heatmap)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[250px] sm:h-[300px] md:h-[350px] w-full">
          <Plot
            data={[
              {
                type: 'scattergeo',
                mode: 'markers',
                lat: lats,
                lon: lons,
                text: texts,
                marker: {
                  size: counts,
                  sizemode: 'area',
                  sizeref: 2.0 * Math.max(...counts) / (20**2), // Adjusted size reference
                  color: counts,
                  colorscale: 'Oranges',
                  showscale: true,
                  opacity: 0.7,
                  colorbar: {
                    title: { text: 'Customers', font: { color: 'hsl(var(--muted-foreground))' } },
                    thickness: 10,
                    len: 0.8,
                    tickfont: { color: 'hsl(var(--muted-foreground))' },
                  },
                },
              },
            ]}
            layout={{
              autosize: true,
              margin: { l: 0, r: 0, t: 0, b: 0 },
              showlegend: false,
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)',
              geo: {
                scope: 'south america',
                resolution: 50,
                showland: true,
                landcolor: 'hsla(var(--muted), 0.2)',
                countrycolor: 'hsla(var(--border), 0.5)',
                coastlinecolor: 'hsla(var(--border), 0.5)',
                projection: { type: 'mercator' },
                center: { lat: -15, lon: -55 },
                lataxis: { range: [-35, 5] },
                lonaxis: { range: [-75, -30] },
                bgcolor: 'rgba(0,0,0,0)',
              },
            }}
            config={{ displayModeBar: false }}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </CardContent>
    </Card>
  );
}
