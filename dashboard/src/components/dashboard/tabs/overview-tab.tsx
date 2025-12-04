import { KPICards } from '../kpi-cards';
import { RevenueChart } from '../revenue-chart';
import { CategoryChart } from '../category-chart';

interface OverviewTabProps {
  data: any;
}

export function OverviewTab({ data }: OverviewTabProps) {
  return (
    <div className="space-y-4">
      <KPICards kpis={data.kpis} />
      
      <div className="grid gap-2 sm:gap-3 md:gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-7">
        <div className="col-span-4">
          <RevenueChart data={data.revenueTrend} />
        </div>
        <div className="col-span-3">
          <CategoryChart data={data.categoryRevenue} />
        </div>
      </div>
    </div>
  );
}
