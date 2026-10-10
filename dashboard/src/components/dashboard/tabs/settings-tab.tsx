import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';

const DATASET_TABLES: [string, string][] = [
  ['geolocation', '738,332'],
  ['order_items', '112,650'],
  ['order_payments', '103,886'],
  ['orders', '99,441'],
  ['customers', '99,441'],
  ['order_reviews', '98,167'],
  ['products', '32,951'],
  ['sellers', '3,095'],
];

export function SettingsTab() {
  return (
    <div className="space-y-4">
      <Card className="gap-4 rounded-[10px] py-5 shadow-none">
        <CardHeader className="px-5">
          <CardTitle className="text-base" style={{ fontFamily: 'var(--font-display)' }}>
            Dataset
          </CardTitle>
          <CardDescription>
            Olist public Brazilian e-commerce dataset (Kaggle, 2016–2018) — 1,287,963 rows loaded across 8 tables.
          </CardDescription>
        </CardHeader>
        <CardContent className="px-5">
          <dl className="grid grid-cols-1 gap-x-8 sm:grid-cols-2">
            {DATASET_TABLES.map(([table, rows]) => (
              <div
                key={table}
                className="flex items-baseline justify-between gap-3 border-b border-border py-2 last:border-b-0"
              >
                <dt className="mono text-sm text-ink-2">{table}</dt>
                <dd className="tnum text-sm font-medium">{rows}</dd>
              </div>
            ))}
          </dl>
        </CardContent>
      </Card>

      <Card className="gap-4 rounded-[10px] py-5 shadow-none">
        <CardHeader className="px-5">
          <CardTitle className="text-base" style={{ fontFamily: 'var(--font-display)' }}>
            Project
          </CardTitle>
          <CardDescription>Repository facts, current as of 2026-10-10.</CardDescription>
        </CardHeader>
        <CardContent className="px-5">
          <ul className="flex flex-wrap gap-2">
            <li className="chip">3 API endpoints</li>
            <li className="chip">23 tests passing</li>
            <li className="chip">2 load backends</li>
            <li className="chip">
              <a
                href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System"
                target="_blank"
                rel="noopener noreferrer"
                className="link-grow"
              >
                Source
              </a>
            </li>
            <li className="chip">
              <a
                href="https://github.com/TADSTech/Brazilian-Retail-Intelligence-System/tree/main/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="link-grow"
              >
                Docs
              </a>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
