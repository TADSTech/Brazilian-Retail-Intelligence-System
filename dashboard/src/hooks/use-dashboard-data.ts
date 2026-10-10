import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

// PostgREST returns at most 1000 rows per request (db-max-rows), so every
// full-table read must be paginated or it is silently truncated.
const PAGE_SIZE = 1000;
const MAX_ATTEMPTS = 4;

interface OrderItemRow {
  order_id: string;
  product_id: string;
  seller_id: string;
  price: number;
  freight_value: number;
}

interface OrderRow {
  order_id: string;
  customer_id: string;
  order_status: string;
  order_purchase_timestamp: string | null;
  order_delivered_customer_date: string | null;
  order_estimated_delivery_date: string | null;
}

type DeliveredDatedOrder = OrderRow & {
  order_purchase_timestamp: string;
  order_delivered_customer_date: string;
};

interface CustomerRow {
  customer_id: string;
  customer_unique_id: string;
  customer_city: string;
  customer_state: string;
  // Stored as varchar in the database (may be "14409", never "014409").
  customer_zip_code_prefix: string;
}

interface ReviewRow {
  order_id: string;
  review_score: number;
}

interface PaymentRow {
  payment_type: string;
  payment_installments: number | null;
}

interface ProductRow {
  product_id: string;
  product_category_name_english: string | null;
}

interface GeoRow {
  geolocation_zip_code_prefix: number;
  geolocation_lat: number;
  geolocation_lng: number;
  geolocation_city: string;
  geolocation_state: string;
}

interface ProductStat {
  product_id: string;
  units_sold: number;
  total_revenue: number;
  orders: Set<string>;
  category: string;
}

interface CategoryStat {
  category: string;
  items_sold: number;
  total_revenue: number;
  orders: Set<string>;
}

interface SalesPoint {
  rank: number;
  product_id: string;
  category: string;
  revenue: number;
  cumulative_percentage: number;
  pareto_group: string;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function withRetry<T extends { error: unknown }>(fn: () => Promise<T>): Promise<T> {
  let lastError: unknown = null;
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    try {
      const result = await fn();
      if (!result.error) return result;
      lastError = result.error;
    } catch (err) {
      lastError = err;
    }
    if (attempt < MAX_ATTEMPTS - 1) await sleep(500 * 2 ** attempt);
  }
  if (lastError instanceof Error) throw lastError;
  if (typeof lastError === 'object' && lastError !== null && 'message' in lastError) {
    throw new Error(String((lastError as { message: unknown }).message));
  }
  throw new Error(String(lastError));
}

async function fetchAllRows<T>(table: string, select: string): Promise<T[]> {
  if (!supabase) throw new Error('Supabase client not initialized. Please check your .env file.');
  const rows: T[] = [];
  for (let from = 0; ; from += PAGE_SIZE) {
    const page = await withRetry(async () => {
      const query = supabase!.from(table).select(select);
      return query.range(from, from + PAGE_SIZE - 1);
    });
    const data = (page.data ?? []) as T[];
    rows.push(...data);
    if (data.length < PAGE_SIZE) break;
  }
  return rows;
}

async function fetchInBatches<T>(
  table: string,
  select: string,
  inColumn: string,
  ids: Array<string | number>,
  batchSize: number = 50
): Promise<T[]> {
  if (!supabase) throw new Error('Supabase client not initialized. Please check your .env file.');
  const uniqueIds = [...new Set(ids)];
  const results: T[] = [];
  for (let i = 0; i < uniqueIds.length; i += batchSize) {
    const batch = uniqueIds.slice(i, i + batchSize);
    for (let from = 0; ; from += PAGE_SIZE) {
      const page = await withRetry(async () => {
        const query = supabase!.from(table).select(select).in(inColumn, batch);
        return query.range(from, from + PAGE_SIZE - 1);
      });
      const data = (page.data ?? []) as T[];
      results.push(...data);
      if (data.length < PAGE_SIZE) break;
    }
  }
  return results;
}

export function useDashboardData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [data, setData] = useState<any>({
    kpis: {},
    revenueTrend: [],
    categoryRevenue: [],
    customerGeo: [],
    orderStatus: [],
    topSellers: [],
    customerBehavior: {
      repeatRate: 0,
      newVsReturning: []
    },
    customerSatisfaction: {
      avgScore: 0,
      scoreDistribution: [],
      deliveryCorrelation: []
    },
    productPerformance: {
      topProducts: [],
      categoryPerformance: [],
      salesConcentration: []
    },
    analytics: {
      avgDeliveryDays: 0,
      onTimeDeliveryRate: 0,
      deliveryDistribution: [],
      paymentMethods: [],
      topPaymentMethod: null,
      installmentDistribution: [],
      avgInstallments: 0
    }
  });

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);

        if (!supabase) {
          throw new Error('Supabase client not initialized. Please check your .env file.');
        }

        const [items, orders, customers, reviews, payments, products] = await Promise.all([
          fetchAllRows<OrderItemRow>('order_items', 'order_id, product_id, seller_id, price, freight_value'),
          fetchAllRows<OrderRow>(
            'orders',
            'order_id, customer_id, order_status, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date'
          ),
          fetchAllRows<CustomerRow>(
            'customers',
            'customer_id, customer_unique_id, customer_city, customer_state, customer_zip_code_prefix'
          ),
          fetchAllRows<ReviewRow>('order_reviews', 'order_id, review_score'),
          fetchAllRows<PaymentRow>('order_payments', 'payment_type, payment_installments'),
          fetchAllRows<ProductRow>('products', 'product_id, product_category_name_english')
        ]);

        const deliveredOrders = orders.filter((o) => o.order_status === 'delivered');

        const itemsByOrder = new Map<string, OrderItemRow[]>();
        items.forEach((item) => {
          const list = itemsByOrder.get(item.order_id);
          if (list) list.push(item);
          else itemsByOrder.set(item.order_id, [item]);
        });

        const productCategory = new Map<string, string | null>();
        products.forEach((p) => {
          productCategory.set(p.product_id, p.product_category_name_english);
        });

        // 1. Executive Overview KPIs
        const totalRevenue = items.reduce((sum, item) => sum + (item.price || 0) + (item.freight_value || 0), 0);
        const totalOrders = deliveredOrders.length;
        const uniqueCustomers = customers.length;
        const avgOrderValue = totalOrders ? totalRevenue / totalOrders : 0;

        // 2. Revenue Trend (monthly, delivered orders)
        const monthlyRevenue = new Map<string, number>();
        deliveredOrders.forEach((order) => {
          if (!order.order_purchase_timestamp) return;
          const month = order.order_purchase_timestamp.slice(0, 7);
          const orderRevenue = (itemsByOrder.get(order.order_id) || []).reduce(
            (sum, item) => sum + (item.price || 0) + (item.freight_value || 0),
            0
          );
          monthlyRevenue.set(month, (monthlyRevenue.get(month) || 0) + orderRevenue);
        });
        const revenueTrend = Array.from(monthlyRevenue.entries())
          .map(([date, revenue]) => ({ date, revenue }))
          .sort((a, b) => a.date.localeCompare(b.date));

        // 3. Category Revenue
        const categoryMap = new Map<string, number>();
        items.forEach((item) => {
          const cat = productCategory.get(item.product_id) || 'Unknown';
          const val = (item.price || 0) + (item.freight_value || 0);
          categoryMap.set(cat, (categoryMap.get(cat) || 0) + val);
        });
        const categoryRevenue = Array.from(categoryMap.entries())
          .map(([category, revenue]) => ({ category, revenue }))
          .sort((a, b) => b.revenue - a.revenue)
          .slice(0, 10);

        // 4. Customer Geolocation
        // customers.customer_zip_code_prefix is varchar while
        // geolocation.geolocation_zip_code_prefix is integer, so keys are
        // normalized to numbers on both sides before joining.
        const zipCounts = new Map<number, number>();
        customers.forEach((c) => {
          const zip = Number(c.customer_zip_code_prefix);
          if (!Number.isFinite(zip)) return;
          zipCounts.set(zip, (zipCounts.get(zip) || 0) + 1);
        });

        // The map renders at most 300 points, so coordinates are only needed
        // for the highest-count zips instead of all ~19k customer zips.
        const topZips = Array.from(zipCounts.entries())
          .sort((a, b) => b[1] - a[1])
          .slice(0, 500)
          .map(([zip]) => zip);

        const geoRows = await fetchInBatches<GeoRow>(
          'geolocation',
          'geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state',
          'geolocation_zip_code_prefix',
          topZips,
          25
        );

        const locationMap = new Map<
          string,
          { zip: number; lat: number; lon: number; city: string; state: string; count: number }
        >();
        geoRows.forEach((g) => {
          const key = `${g.geolocation_zip_code_prefix}`;
          if (!locationMap.has(key)) {
            locationMap.set(key, {
              zip: g.geolocation_zip_code_prefix,
              lat: g.geolocation_lat,
              lon: g.geolocation_lng,
              city: g.geolocation_city,
              state: g.geolocation_state,
              count: zipCounts.get(g.geolocation_zip_code_prefix) || 0
            });
          }
        });

        const customerGeo = Array.from(locationMap.values())
          .filter((loc) => loc.count > 0)
          .sort((a, b) => b.count - a.count)
          .slice(0, 300);

        // Exact top cities by each customer's own city/state (full table,
        // no zip cap) for the "Top Customer Locations" list.
        const cityCounts = new Map<string, { city: string; state: string; count: number }>();
        customers.forEach((c) => {
          const key = `${c.customer_city.toLowerCase()}, ${c.customer_state.toLowerCase()}`;
          const entry = cityCounts.get(key);
          if (entry) entry.count += 1;
          else cityCounts.set(key, { city: c.customer_city, state: c.customer_state, count: 1 });
        });
        const topCustomerCities = Array.from(cityCounts.values())
          .sort((a, b) => b.count - a.count)
          .slice(0, 10);

        // 5. Order Status Distribution
        const statusMap = new Map<string, number>();
        orders.forEach((o) => {
          statusMap.set(o.order_status, (statusMap.get(o.order_status) || 0) + 1);
        });
        const orderStatus = Array.from(statusMap.entries())
          .map(([status, count]) => ({ status, count }))
          .sort((a, b) => b.count - a.count);

        // 6. Top Sellers
        const sellerRevenueMap = new Map<string, number>();
        items.forEach((item) => {
          sellerRevenueMap.set(
            item.seller_id,
            (sellerRevenueMap.get(item.seller_id) || 0) + (item.price || 0)
          );
        });
        const topSellers = Array.from(sellerRevenueMap.entries())
          .map(([seller, revenue]) => ({ seller, revenue }))
          .sort((a, b) => b.revenue - a.revenue)
          .slice(0, 5);

        // 7. Customer Behavior Analytics
        // Olist's orders.customer_id is a per-order hash (one per order), so
        // repeat/new-vs-returning metrics must group by customer_unique_id.
        const uniqueIdByCustomerId = new Map<string, string>();
        customers.forEach((c) => uniqueIdByCustomerId.set(c.customer_id, c.customer_unique_id));
        const uniqueOf = (customerId: string): string =>
          uniqueIdByCustomerId.get(customerId) ?? customerId;

        const customerOrderMap = new Map<string, number>();
        deliveredOrders.forEach((order) => {
          const uid = uniqueOf(order.customer_id);
          customerOrderMap.set(uid, (customerOrderMap.get(uid) || 0) + 1);
        });
        const repeatCustomers = Array.from(customerOrderMap.values()).filter((c) => c > 1).length;
        const totalCustomersWithOrders = customerOrderMap.size;
        const repeatRate =
          totalCustomersWithOrders > 0 ? (repeatCustomers / totalCustomersWithOrders) * 100 : 0;

        const customerFirstOrder = new Map<string, string>();
        const monthlyData = new Map<string, { new: number; returning: number }>();
        const newVsReturningOrders = [...deliveredOrders].sort((a, b) =>
          String(a.order_purchase_timestamp).localeCompare(String(b.order_purchase_timestamp))
        );
        newVsReturningOrders.forEach((order) => {
          if (!order.order_purchase_timestamp) return;
          const uid = uniqueOf(order.customer_id);
          const month = new Date(order.order_purchase_timestamp).toISOString().slice(0, 7);
          const isNew = !customerFirstOrder.has(uid);
          if (isNew) {
            customerFirstOrder.set(uid, order.order_purchase_timestamp);
          }
          if (!monthlyData.has(month)) {
            monthlyData.set(month, { new: 0, returning: 0 });
          }
          const monthData = monthlyData.get(month)!;
          if (isNew) monthData.new++;
          else monthData.returning++;
        });
        const newVsReturning = Array.from(monthlyData.entries())
          .map(([month, counts]) => ({ month, ...counts }))
          .sort((a, b) => a.month.localeCompare(b.month));

        // 8. Customer Satisfaction Analytics
        const avgScore =
          reviews.length > 0
            ? reviews.reduce((sum, r) => sum + r.review_score, 0) / reviews.length
            : 0;
        const scoreCounts = new Map<number, number>();
        reviews.forEach((r) => {
          scoreCounts.set(r.review_score, (scoreCounts.get(r.review_score) || 0) + 1);
        });
        const scoreDistribution = Array.from(scoreCounts.entries())
          .map(([score, count]) => ({ score, count }))
          .sort((a, b) => a.score - b.score);

        const reviewMap = new Map<string, number>();
        reviews.forEach((review) => {
          reviewMap.set(review.order_id, review.review_score);
        });
        const onTimeOrders: number[] = [];
        const delayedOrders: number[] = [];
        deliveredOrders.forEach((order) => {
          if (!order.order_delivered_customer_date || !order.order_estimated_delivery_date) return;
          const reviewScore = reviewMap.get(order.order_id);
          if (reviewScore === undefined) return;
          const delivered = new Date(order.order_delivered_customer_date);
          const estimated = new Date(order.order_estimated_delivery_date);
          if (delivered > estimated) delayedOrders.push(reviewScore);
          else onTimeOrders.push(reviewScore);
        });
        const avgOnTime =
          onTimeOrders.length > 0 ? onTimeOrders.reduce((a, b) => a + b, 0) / onTimeOrders.length : 0;
        const avgDelayed =
          delayedOrders.length > 0
            ? delayedOrders.reduce((a, b) => a + b, 0) / delayedOrders.length
            : 0;
        const deliveryCorrelation = [
          { status: 'On Time', avgScore: avgOnTime, count: onTimeOrders.length },
          { status: 'Delayed', avgScore: avgDelayed, count: delayedOrders.length }
        ];

        // 9. Product Performance Analytics
        const productStats = new Map<string, ProductStat>();
        items.forEach((item) => {
          const pid = item.product_id;
          if (!productStats.has(pid)) {
            productStats.set(pid, {
              product_id: pid,
              units_sold: 0,
              total_revenue: 0,
              orders: new Set<string>(),
              category: productCategory.get(pid) || 'Unknown'
            });
          }
          const stats = productStats.get(pid)!;
          stats.units_sold++;
          stats.total_revenue += (item.price || 0) + (item.freight_value || 0);
          stats.orders.add(item.order_id);
        });
        const topProducts = Array.from(productStats.values())
          .map((p) => ({
            product_id: p.product_id,
            category: p.category,
            units_sold: p.units_sold,
            total_revenue: p.total_revenue,
            unique_orders: p.orders.size,
            avg_price: p.total_revenue / p.units_sold
          }))
          .sort((a, b) => b.units_sold - a.units_sold)
          .slice(0, 20);

        const categoryStats = new Map<string, CategoryStat>();
        items.forEach((item) => {
          const cat = productCategory.get(item.product_id) || 'Unknown';
          if (!categoryStats.has(cat)) {
            categoryStats.set(cat, {
              category: cat,
              items_sold: 0,
              total_revenue: 0,
              orders: new Set<string>()
            });
          }
          const stats = categoryStats.get(cat)!;
          stats.items_sold++;
          stats.total_revenue += (item.price || 0) + (item.freight_value || 0);
          stats.orders.add(item.order_id);
        });
        const categoryPerformance = Array.from(categoryStats.values())
          .map((c) => ({
            category: c.category,
            order_count: c.orders.size,
            items_sold: c.items_sold,
            total_revenue: c.total_revenue,
            avg_order_value: c.total_revenue / c.orders.size
          }))
          .sort((a, b) => b.order_count - a.order_count)
          .slice(0, 15);

        let salesConcentration: SalesPoint[] = [];
        if (topProducts.length > 0) {
          const sortedProducts = [...topProducts].sort((a, b) => b.total_revenue - a.total_revenue);
          const paretoTotal = sortedProducts.reduce((sum, p) => sum + p.total_revenue, 0);
          let cumulativeRevenue = 0;
          salesConcentration = sortedProducts.map((p, index) => {
            cumulativeRevenue += p.total_revenue;
            const cumulativePercentage = (cumulativeRevenue / paretoTotal) * 100;
            return {
              rank: index + 1,
              product_id: p.product_id,
              category: p.category,
              revenue: p.total_revenue,
              cumulative_percentage: cumulativePercentage,
              pareto_group: cumulativePercentage <= 80 ? 'Top 20%' : 'Bottom 80%'
            };
          });
        }

        // 10. Logistics & Payment Analytics
        const deliveryOrders = deliveredOrders.filter(
          (order): order is DeliveredDatedOrder =>
            Boolean(order.order_delivered_customer_date && order.order_purchase_timestamp)
        );
        let avgDeliveryDays = 0;
        let onTimeDeliveryRate = 0;
        let deliveryDistribution: Array<{ range: string; count: number }> = [];
        if (deliveryOrders.length > 0) {
          const deliveryTimes = deliveryOrders.map((order) => {
            const purchase = new Date(order.order_purchase_timestamp);
            const delivered = new Date(order.order_delivered_customer_date);
            return (delivered.getTime() - purchase.getTime()) / (1000 * 60 * 60 * 24);
          });
          avgDeliveryDays = deliveryTimes.reduce((a, b) => a + b, 0) / deliveryTimes.length;

          const onTimeCount = deliveryOrders.filter((order) => {
            if (!order.order_estimated_delivery_date) return false;
            return (
              new Date(order.order_delivered_customer_date) <=
              new Date(order.order_estimated_delivery_date)
            );
          }).length;
          onTimeDeliveryRate = (onTimeCount / deliveryOrders.length) * 100;

          const distMap = new Map<string, number>();
          deliveryTimes.forEach((days) => {
            let range = '';
            if (days <= 5) range = '0-5 days';
            else if (days <= 10) range = '6-10 days';
            else if (days <= 15) range = '11-15 days';
            else if (days <= 20) range = '16-20 days';
            else if (days <= 30) range = '21-30 days';
            else range = '30+ days';
            distMap.set(range, (distMap.get(range) || 0) + 1);
          });
          const rangeOrder = ['0-5 days', '6-10 days', '11-15 days', '16-20 days', '21-30 days', '30+ days'];
          deliveryDistribution = rangeOrder
            .filter((r) => distMap.has(r))
            .map((range) => ({ range, count: distMap.get(range)! }));
        }

        let paymentMethods: Array<{ type: string; count: number; percentage: number }> = [];
        let topPaymentMethod: { type: string; count: number; percentage: number } | null = null;
        let installmentDistribution: Array<{ installments: number; count: number }> = [];
        let avgInstallments = 0;
        if (payments.length > 0) {
          const methodMap = new Map<string, number>();
          payments.forEach((p) => {
            methodMap.set(p.payment_type, (methodMap.get(p.payment_type) || 0) + 1);
          });
          paymentMethods = Array.from(methodMap.entries())
            .map(([type, count]) => ({
              type,
              count,
              percentage: (count / payments.length) * 100
            }))
            .sort((a, b) => b.count - a.count);
          topPaymentMethod = paymentMethods[0] || null;

          const installmentMap = new Map<number, number>();
          let totalInstallments = 0;
          payments.forEach((p) => {
            const inst = p.payment_installments || 1;
            installmentMap.set(inst, (installmentMap.get(inst) || 0) + 1);
            totalInstallments += inst;
          });
          avgInstallments = totalInstallments / payments.length;
          installmentDistribution = Array.from(installmentMap.entries())
            .map(([installments, count]) => ({ installments, count }))
            .sort((a, b) => a.installments - b.installments)
            .slice(0, 12);
        }

        setData({
          kpis: {
            totalRevenue,
            totalOrders,
            uniqueCustomers,
            avgOrderValue
          },
          revenueTrend,
          categoryRevenue,
          customerGeo,
          topCustomerCities,
          orderStatus,
          topSellers,
          customerBehavior: {
            repeatRate,
            newVsReturning
          },
          customerSatisfaction: {
            avgScore,
            scoreDistribution,
            deliveryCorrelation
          },
          productPerformance: {
            topProducts,
            categoryPerformance,
            salesConcentration
          },
          analytics: {
            avgDeliveryDays,
            onTimeDeliveryRate,
            deliveryDistribution,
            paymentMethods,
            topPaymentMethod,
            installmentDistribution,
            avgInstallments
          }
        });

      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError(err instanceof Error ? err.message : String(err));
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [attempt]);

  return { loading, error, data, retry: () => setAttempt((a) => a + 1) };
}
