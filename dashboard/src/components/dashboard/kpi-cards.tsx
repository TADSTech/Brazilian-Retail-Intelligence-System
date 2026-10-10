import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { DollarSign, ShoppingBag, Users, TrendingUp } from "lucide-react";
import { useCountUp } from "../../hooks/use-count-up";

interface KPICardsProps {
  kpis: {
    totalRevenue: number;
    totalOrders: number;
    uniqueCustomers: number;
    avgOrderValue: number;
  };
}

export function KPICards({ kpis }: KPICardsProps) {
  const revenue = useCountUp(kpis.totalRevenue);
  const orders = useCountUp(kpis.totalOrders);
  const customers = useCountUp(kpis.uniqueCustomers);
  const avgValue = useCountUp(kpis.avgOrderValue);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  const tiles = [
    {
      title: 'Total Revenue',
      value: formatCurrency(revenue),
      note: 'order_items: price + freight',
      Icon: DollarSign,
    },
    {
      title: 'Delivered Orders',
      value: formatNumber(orders),
      note: 'orders where status = delivered',
      Icon: ShoppingBag,
    },
    {
      title: 'Customers',
      value: formatNumber(customers),
      note: 'rows in the customers table',
      Icon: Users,
    },
    {
      title: 'Avg. Order Value',
      value: formatCurrency(avgValue),
      note: 'revenue ÷ delivered orders',
      Icon: TrendingUp,
    },
  ];

  return (
    <div className="bento grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
      {tiles.map(({ title, value, note, Icon }) => (
        <Card key={title} className="gap-3 rounded-none border-0 py-5 shadow-none">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 px-5 pb-0">
            <CardTitle className="label">{title}</CardTitle>
            <Icon className="size-4 text-primary" aria-hidden />
          </CardHeader>
          <CardContent className="px-5">
            <div
              className="tnum text-2xl font-medium tracking-[-0.02em]"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              {value}
            </div>
            <p className="mt-1 text-xs text-muted-foreground">{note}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
