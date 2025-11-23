import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

// Helper to fetch data in batches to avoid URL length limits
async function fetchInBatches(
  table: string,
  select: string,
  inColumn: string,
  ids: any[],
  batchSize: number = 50
) {
  let results: any[] = [];
  // Remove duplicates from ids to optimize fetching
  const uniqueIds = [...new Set(ids)];
  
  for (let i = 0; i < uniqueIds.length; i += batchSize) {
    const batch = uniqueIds.slice(i, i + batchSize);
    const { data, error } = await supabase
      .from(table)
      .select(select)
      .in(inColumn, batch);
      
    if (error) throw error;
    if (data) results = [...results, ...data];
  }
  return results;
}

export function useDashboardData() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
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
        
        // 1. Executive Overview KPIs
        // Total Revenue
        const { data: revenueData, error: revenueError } = await supabase
          .from('order_items')
          .select('price, freight_value');
        
        if (revenueError) throw revenueError;
        
        const totalRevenue = revenueData.reduce((sum, item) => sum + (item.price || 0) + (item.freight_value || 0), 0);

        // Total Orders
        const { count: totalOrders, error: ordersError } = await supabase
          .from('orders')
          .select('*', { count: 'exact', head: true })
          .eq('order_status', 'delivered');
          
        if (ordersError) throw ordersError;

        // Unique Customers
        const { count: uniqueCustomers, error: customersError } = await supabase
          .from('customers')
          .select('*', { count: 'exact', head: true });
          
        if (customersError) throw customersError;

        // Average Order Value
        const avgOrderValue = totalOrders ? totalRevenue / totalOrders : 0;

        // 2. Revenue Trend
        const { data: ordersData, error: ordersDataError } = await supabase
          .from('orders')
          .select('order_id, order_purchase_timestamp')
          .eq('order_status', 'delivered')
          .order('order_purchase_timestamp', { ascending: true })
          .limit(1000);

        if (ordersDataError) throw ordersDataError;

        const orderIds = ordersData.map(o => o.order_id);
        
        const orderItemsData = await fetchInBatches(
          'order_items',
          'order_id, price, freight_value',
          'order_id',
          orderIds
        );

        // Group items by order_id
        const itemsByOrder = new Map();
        orderItemsData.forEach((item: any) => {
          if (!itemsByOrder.has(item.order_id)) {
            itemsByOrder.set(item.order_id, []);
          }
          itemsByOrder.get(item.order_id).push(item);
        });

        const revenueTrend = ordersData.map(order => {
          const items = itemsByOrder.get(order.order_id) || [];
          const revenue = items.reduce((sum: number, item: any) => sum + (item.price || 0) + (item.freight_value || 0), 0);
          return {
            date: order.order_purchase_timestamp,
            revenue
          };
        });

        // 3. Category Revenue
        const { data: categoryItemsData, error: categoryItemsError } = await supabase
          .from('order_items')
          .select('product_id, price, freight_value')
          .limit(1000);

        if (categoryItemsError) throw categoryItemsError;

        const productIds = [...new Set(categoryItemsData.map((item: any) => item.product_id))];

        const productsData = await fetchInBatches(
          'products',
          'product_id, product_category_name_english',
          'product_id',
          productIds
        );

        const productMap = new Map();
        productsData.forEach((p: any) => {
          productMap.set(p.product_id, p.product_category_name_english);
        });

        const categoryMap = new Map();
        categoryItemsData.forEach((item: any) => {
          const cat = productMap.get(item.product_id) || 'Unknown';
          const val = (item.price || 0) + (item.freight_value || 0);
          categoryMap.set(cat, (categoryMap.get(cat) || 0) + val);
        });

        const categoryRevenue = Array.from(categoryMap.entries())
          .map(([category, revenue]) => ({ category, revenue }))
          .sort((a, b) => b.revenue - a.revenue)
          .slice(0, 10);

        // 4. Customer Geolocation
        // Get customer counts by zip
        const { data: customerZips, error: customerZipError } = await supabase
          .from('customers')
          .select('customer_zip_code_prefix');

        if (customerZipError) throw customerZipError;

        const zipCounts = new Map();
        customerZips.forEach((c: any) => {
          const zip = c.customer_zip_code_prefix;
          zipCounts.set(zip, (zipCounts.get(zip) || 0) + 1);
        });

        // Get geolocation data for all customer zips
        const customerZipList = Array.from(zipCounts.keys());
        
        const allGeoData = await fetchInBatches(
          'geolocation',
          'geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state',
          'geolocation_zip_code_prefix',
          customerZipList
        );

        // Aggregate by unique location (deduplicate multiple entries per zip)
        const locationMap = new Map();
        allGeoData.forEach((g: any) => {
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
          .filter(loc => loc.count > 0)
          .sort((a, b) => b.count - a.count)
          .slice(0, 300); // Limit to top 300 locations for performance

        // 5. Order Status Distribution
        const { data: statusData, error: statusError } = await supabase
          .from('orders')
          .select('order_status');

        if (statusError) throw statusError;

        const statusMap = new Map();
        statusData.forEach((item: any) => {
          const status = item.order_status;
          statusMap.set(status, (statusMap.get(status) || 0) + 1);
        });

        const orderStatus = Array.from(statusMap.entries())
          .map(([status, count]) => ({ status, count }))
          .sort((a, b) => b.count - a.count);

        // 6. Top Sellers
        const { data: sellerItems, error: sellerItemsError } = await supabase
          .from('order_items')
          .select('seller_id, price')
          .limit(2000);

        if (sellerItemsError) throw sellerItemsError;

        const sellerRevenueMap = new Map();
        sellerItems.forEach((item: any) => {
          sellerRevenueMap.set(item.seller_id, (sellerRevenueMap.get(item.seller_id) || 0) + item.price);
        });

        const topSellers = Array.from(sellerRevenueMap.entries())
          .map(([seller, revenue]) => ({ seller, revenue }))
          .sort((a, b) => b.revenue - a.revenue)
          .slice(0, 5);

        // 7. Customer Behavior Analytics
        // Repeat purchase rate - get all orders and aggregate by customer
        const { data: allCustomerOrders, error: allOrdersError } = await supabase
          .from('orders')
          .select('order_id, customer_id')
          .eq('order_status', 'delivered');
        
        let repeatRate = 0;
        if (!allOrdersError && allCustomerOrders) {
          const customerOrderMap = new Map();
          allCustomerOrders.forEach((order: any) => {
            customerOrderMap.set(order.customer_id, (customerOrderMap.get(order.customer_id) || 0) + 1);
          });
          
          const repeatCustomers = Array.from(customerOrderMap.values()).filter(count => count > 1).length;
          const totalCustomers = customerOrderMap.size;
          repeatRate = totalCustomers > 0 ? (repeatCustomers / totalCustomers) * 100 : 0;
        }

        // New vs Returning customers over time
        const { data: customerOrders, error: customerOrdersError } = await supabase
          .from('orders')
          .select('order_id, order_purchase_timestamp, customer_id')
          .eq('order_status', 'delivered')
          .order('order_purchase_timestamp');

        let newVsReturning: any[] = [];
        if (!customerOrdersError && customerOrders) {
          const customerFirstOrder = new Map();
          const monthlyData = new Map();

          customerOrders.forEach((order: any) => {
            const month = new Date(order.order_purchase_timestamp).toISOString().slice(0, 7);
            const isNew = !customerFirstOrder.has(order.customer_id);
            
            if (isNew) {
              customerFirstOrder.set(order.customer_id, order.order_purchase_timestamp);
            }

            if (!monthlyData.has(month)) {
              monthlyData.set(month, { new: 0, returning: 0 });
            }

            const monthData = monthlyData.get(month);
            if (isNew) {
              monthData.new++;
            } else {
              monthData.returning++;
            }
          });

          newVsReturning = Array.from(monthlyData.entries())
            .map(([month, data]) => ({ month, ...data }))
            .sort((a, b) => a.month.localeCompare(b.month));
        }

        // 8. Customer Satisfaction Analytics
        // Average review score
        const { data: reviewData, error: reviewError } = await supabase
          .from('order_reviews')
          .select('review_score');
        
        let avgScore = 0;
        let scoreDistribution: any[] = [];
        if (!reviewError && reviewData) {
          avgScore = reviewData.reduce((sum, r) => sum + r.review_score, 0) / reviewData.length;
          
          const scoreCounts = new Map();
          reviewData.forEach((r: any) => {
            scoreCounts.set(r.review_score, (scoreCounts.get(r.review_score) || 0) + 1);
          });
          
          scoreDistribution = Array.from(scoreCounts.entries())
            .map(([score, count]) => ({ score, count }))
            .sort((a, b) => b.score - a.score);
        }

        // Delivery delay vs review score
        const { data: deliveredOrders, error: deliveredOrdersError } = await supabase
          .from('orders')
          .select('order_id, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date')
          .eq('order_status', 'delivered')
          .not('order_delivered_customer_date', 'is', null)
          .not('order_estimated_delivery_date', 'is', null);

        const { data: allReviews, error: allReviewsError } = await supabase
          .from('order_reviews')
          .select('order_id, review_score');

        let deliveryCorrelation: any[] = [];
        if (!deliveredOrdersError && !allReviewsError && deliveredOrders && allReviews) {
          // Create a map of order_id to review_score
          const reviewMap = new Map();
          allReviews.forEach((review: any) => {
            reviewMap.set(review.order_id, review.review_score);
          });

          const onTimeOrders: any[] = [];
          const delayedOrders: any[] = [];

          deliveredOrders.forEach((order: any) => {
            const reviewScore = reviewMap.get(order.order_id);
            if (reviewScore !== undefined) {
              const delivered = new Date(order.order_delivered_customer_date);
              const estimated = new Date(order.order_estimated_delivery_date);
              const isDelayed = delivered > estimated;
              
              if (isDelayed) {
                delayedOrders.push(reviewScore);
              } else {
                onTimeOrders.push(reviewScore);
              }
            }
          });

          const avgOnTime = onTimeOrders.length > 0 ? onTimeOrders.reduce((a, b) => a + b, 0) / onTimeOrders.length : 0;
          const avgDelayed = delayedOrders.length > 0 ? delayedOrders.reduce((a, b) => a + b, 0) / delayedOrders.length : 0;

          deliveryCorrelation = [
            { status: 'On Time', avgScore: avgOnTime, count: onTimeOrders.length },
            { status: 'Delayed', avgScore: avgDelayed, count: delayedOrders.length }
          ];
        }

        // 9. Product Performance Analytics
        // Product performance metrics
        const { data: productItems, error: productItemsError } = await supabase
          .from('order_items')
          .select('product_id, price, freight_value, order_id');

        const { data: allProducts, error: productsError } = await supabase
          .from('products')
          .select('product_id, product_category_name_english');

        let topProducts: any[] = [];
        let categoryPerformance: any[] = [];
        if (!productItemsError && !productsError && productItems && allProducts) {
          // Create product lookup map
          const productMap = new Map();
          allProducts.forEach((p: any) => {
            productMap.set(p.product_id, p.product_category_name_english || 'Unknown');
          });

          // Calculate top products by units sold
          const productStats = new Map();
          productItems.forEach((item: any) => {
            const pid = item.product_id;
            if (!productStats.has(pid)) {
              productStats.set(pid, {
                product_id: pid,
                units_sold: 0,
                total_revenue: 0,
                orders: new Set(),
                category: productMap.get(pid) || 'Unknown'
              });
            }
            const stats = productStats.get(pid);
            stats.units_sold++;
            stats.total_revenue += (item.price || 0) + (item.freight_value || 0);
            stats.orders.add(item.order_id);
          });

          topProducts = Array.from(productStats.values())
            .map(p => ({
              product_id: p.product_id,
              category: p.category,
              units_sold: p.units_sold,
              total_revenue: p.total_revenue,
              unique_orders: p.orders.size,
              avg_price: p.total_revenue / p.units_sold
            }))
            .sort((a, b) => b.units_sold - a.units_sold)
            .slice(0, 20);

          // Category performance
          const categoryStats = new Map();
          productItems.forEach((item: any) => {
            const cat = productMap.get(item.product_id) || 'Unknown';
            if (!categoryStats.has(cat)) {
              categoryStats.set(cat, {
                category: cat,
                items_sold: 0,
                total_revenue: 0,
                orders: new Set()
              });
            }
            const stats = categoryStats.get(cat);
            stats.items_sold++;
            stats.total_revenue += (item.price || 0) + (item.freight_value || 0);
            stats.orders.add(item.order_id);
          });

          categoryPerformance = Array.from(categoryStats.values())
            .map(c => ({
              category: c.category,
              order_count: c.orders.size,
              items_sold: c.items_sold,
              total_revenue: c.total_revenue,
              avg_order_value: c.total_revenue / c.orders.size
            }))
            .sort((a, b) => b.order_count - a.order_count)
            .slice(0, 15);
        }

        // Sales concentration (Pareto analysis)
        let salesConcentration: any[] = [];
        if (topProducts.length > 0) {
          const sortedProducts = [...topProducts].sort((a, b) => b.total_revenue - a.total_revenue);
          const totalRevenue = sortedProducts.reduce((sum, p) => sum + p.total_revenue, 0);
          let cumulativeRevenue = 0;
          
          salesConcentration = sortedProducts.map((p, index) => {
            cumulativeRevenue += p.total_revenue;
            const cumulativePercentage = (cumulativeRevenue / totalRevenue) * 100;
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
        // Average delivery time
        const { data: deliveryOrders, error: deliveryOrdersError } = await supabase
          .from('orders')
          .select('order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date')
          .eq('order_status', 'delivered')
          .not('order_delivered_customer_date', 'is', null)
          .not('order_purchase_timestamp', 'is', null);

        let avgDeliveryDays = 0;
        let onTimeDeliveryRate = 0;
        let deliveryDistribution: any[] = [];
        
        if (!deliveryOrdersError && deliveryOrders) {
          // Calculate average delivery time
          const deliveryTimes = deliveryOrders.map((order: any) => {
            const purchase = new Date(order.order_purchase_timestamp);
            const delivered = new Date(order.order_delivered_customer_date);
            return (delivered.getTime() - purchase.getTime()) / (1000 * 60 * 60 * 24);
          });
          avgDeliveryDays = deliveryTimes.reduce((a, b) => a + b, 0) / deliveryTimes.length;

          // Calculate on-time delivery rate
          const onTimeCount = deliveryOrders.filter((order: any) => {
            if (!order.order_estimated_delivery_date) return false;
            return new Date(order.order_delivered_customer_date) <= new Date(order.order_estimated_delivery_date);
          }).length;
          onTimeDeliveryRate = (onTimeCount / deliveryOrders.length) * 100;

          // Delivery time distribution
          const distMap = new Map();
          deliveryTimes.forEach(days => {
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
            .filter(r => distMap.has(r))
            .map(range => ({ range, count: distMap.get(range) }));
        }

        // Payment analytics
        const { data: payments, error: paymentsError } = await supabase
          .from('order_payments')
          .select('payment_type, payment_installments, payment_value');

        let paymentMethods: any[] = [];
        let topPaymentMethod: any = null;
        let installmentDistribution: any[] = [];
        let avgInstallments = 0;

        if (!paymentsError && payments) {
          // Payment methods distribution
          const methodMap = new Map();
          payments.forEach((p: any) => {
            methodMap.set(p.payment_type, (methodMap.get(p.payment_type) || 0) + 1);
          });

          const totalPayments = payments.length;
          paymentMethods = Array.from(methodMap.entries())
            .map(([type, count]) => ({
              type,
              count,
              percentage: (count / totalPayments) * 100
            }))
            .sort((a, b) => b.count - a.count);

          topPaymentMethod = paymentMethods[0] || null;

          // Installment distribution
          const installmentMap = new Map();
          let totalInstallments = 0;
          payments.forEach((p: any) => {
            const inst = p.payment_installments || 1;
            installmentMap.set(inst, (installmentMap.get(inst) || 0) + 1);
            totalInstallments += inst;
          });

          avgInstallments = totalInstallments / payments.length;

          installmentDistribution = Array.from(installmentMap.entries())
            .map(([installments, count]) => ({ installments, count }))
            .sort((a, b) => a.installments - b.installments)
            .slice(0, 12); // Top 12 installment options
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

      } catch (err: any) {
        console.error('Error fetching dashboard data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  return { loading, error, data };
}
