import { CategoryChart } from '@/components/dashboard/category-chart';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import Plot from 'react-plotly.js';

interface ProductsTabProps {
  data: any;
}

export function ProductsTab({ data }: ProductsTabProps) {
  const { categoryRevenue, topSellers, productPerformance } = data;

  if (!productPerformance || !productPerformance.topProducts) {
    return (
      <div className="space-y-4">
        <Card>
          <CardContent className="py-8">
            <p className="text-center text-muted-foreground">Loading product analytics...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Revenue by Category */}
      <div className="grid gap-4 md:grid-cols-2">
        <CategoryChart data={categoryRevenue} />
        
        <Card>
          <CardHeader>
            <CardTitle>Top Sellers</CardTitle>
            <CardDescription>Highest revenue generating sellers</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Seller ID</TableHead>
                  <TableHead className="text-right">Revenue</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {topSellers.map((seller: any) => (
                  <TableRow key={seller.seller}>
                    <TableCell className="font-mono text-xs">{seller.seller}</TableCell>
                    <TableCell className="text-right">
                      R${seller.revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Top Products Table */}
      <Card>
        <CardHeader>
          <CardTitle>Top-Selling Products</CardTitle>
          <CardDescription>Best performing products by units sold</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12">#</TableHead>
                  <TableHead>Product ID</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-right">Units Sold</TableHead>
                  <TableHead className="text-right">Revenue</TableHead>
                  <TableHead className="text-right">Avg Price</TableHead>
                  <TableHead className="text-right">Orders</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {productPerformance.topProducts.slice(0, 10).map((product: any, index: number) => (
                  <TableRow key={product.product_id}>
                    <TableCell className="font-medium text-muted-foreground">{index + 1}</TableCell>
                    <TableCell className="font-mono text-xs">{product.product_id.slice(0, 8)}...</TableCell>
                    <TableCell className="text-sm">{product.category}</TableCell>
                    <TableCell className="text-right font-medium">{product.units_sold.toLocaleString()}</TableCell>
                    <TableCell className="text-right">R${product.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                    <TableCell className="text-right">R${product.avg_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                    <TableCell className="text-right">{product.unique_orders.toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Category Performance & Sales Concentration */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Category Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Category Performance</CardTitle>
            <CardDescription>Order count by product category</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[350px]">
              <Plot
                data={[
                  {
                    x: productPerformance.categoryPerformance.map((c: any) => c.order_count),
                    y: productPerformance.categoryPerformance.map((c: any) => c.category),
                    type: 'bar',
                    orientation: 'h',
                    marker: { color: '#ea580c' }
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 120, r: 20, t: 20, b: 40 },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  xaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                    title: { text: 'Number of Orders' }
                  },
                  yaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    automargin: true
                  }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Sales Concentration (Pareto) */}
        <Card>
          <CardHeader>
            <CardTitle>Sales Concentration</CardTitle>
            <CardDescription>Pareto analysis (80/20 rule)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[350px]">
              <Plot
                data={[
                  {
                    x: productPerformance.salesConcentration.map((s: any) => s.rank),
                    y: productPerformance.salesConcentration.map((s: any) => s.cumulative_percentage),
                    type: 'scatter',
                    mode: 'lines+markers',
                    line: { color: '#ea580c', width: 2 },
                    marker: { size: 6 },
                    name: 'Cumulative %'
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
                    title: { text: 'Product Rank' }
                  },
                  yaxis: {
                    color: 'hsl(var(--muted-foreground))',
                    gridcolor: 'hsla(var(--border), 0.3)',
                    title: { text: 'Cumulative Revenue %' },
                    range: [0, 100]
                  },
                  shapes: [
                    {
                      type: 'line',
                      x0: 0,
                      x1: productPerformance.salesConcentration.length,
                      y0: 80,
                      y1: 80,
                      line: {
                        color: 'rgba(255, 99, 71, 0.5)',
                        width: 2,
                        dash: 'dash'
                      }
                    }
                  ],
                  annotations: [
                    {
                      x: productPerformance.salesConcentration.length / 2,
                      y: 80,
                      text: '80% Revenue Line',
                      showarrow: false,
                      yshift: 10,
                      font: { color: 'hsl(var(--muted-foreground))' }
                    }
                  ]
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top Categories by Revenue */}
      <Card>
        <CardHeader>
          <CardTitle>Category Revenue Breakdown</CardTitle>
          <CardDescription>Detailed performance metrics by category</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12">#</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-right">Orders</TableHead>
                  <TableHead className="text-right">Items Sold</TableHead>
                  <TableHead className="text-right">Total Revenue</TableHead>
                  <TableHead className="text-right">Avg Order Value</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {productPerformance.categoryPerformance.map((cat: any, index: number) => (
                  <TableRow key={cat.category}>
                    <TableCell className="font-medium text-muted-foreground">{index + 1}</TableCell>
                    <TableCell className="font-medium">{cat.category}</TableCell>
                    <TableCell className="text-right">{cat.order_count.toLocaleString()}</TableCell>
                    <TableCell className="text-right">{cat.items_sold.toLocaleString()}</TableCell>
                    <TableCell className="text-right">R${cat.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                    <TableCell className="text-right">R${cat.avg_order_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
