# Brazilian Retail Intelligence Dashboard

This is the frontend dashboard for the Brazilian Retail Intelligence System. It visualizes data from the Olist E-commerce dataset using React, Plotly, and Supabase.

## Features

- **Executive Overview**: KPI cards showing Total Revenue, Total Orders, Unique Customers, and Average Order Value.
- **Analytics Tab**: Detailed revenue trends and order status distribution.
- **Customers Tab**: Geographic visualization of customer distribution and top locations.
- **Products Tab**: Top product categories and top-performing sellers.
- **Settings**: Customizable dashboard settings (Theme, Data Refresh).
- **Orange Theme**: Professional orange-themed UI matching the brand identity.

## Tech Stack

- **Framework**: React 19 + Vite 7
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Visualization**: Recharts, Lucide React
- **Backend/Data**: Supabase (PostgreSQL)
- **Runtime**: Bun

## Setup

1.  **Install Dependencies**:
    ```bash
    bun install
    ```

2.  **Environment Variables**:
    Ensure you have a `.env` file in the `dashboard` directory with your Supabase credentials:
    ```env
    VITE_SUPABASE_URL=your_supabase_url
    VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
    ```

3.  **Run Development Server**:
    ```bash
    bun run dev
    ```

4.  **Build for Production**:
    ```bash
    bun run build
    ```

## Project Structure

- `src/components/dashboard/`: Dashboard-specific components (Charts, KPI Cards).
- `src/hooks/`: Custom hooks for data fetching (`useDashboardData`).
- `src/lib/`: Utility functions and Supabase client configuration.
- `src/pages/`: Application pages (Dashboard, Home, SignIn).
