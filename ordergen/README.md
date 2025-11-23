# Order Generator (OrderGen)

This tool generates synthetic data for the Brazilian Retail Intelligence System. It learns from the existing dataset to create realistic new orders, customers, and reviews.

## Features

-   **Training**: Learns distributions (products, prices, locations) from the CSV files in `data/`.
-   **NLP**: Uses a lightweight Markov Chain model to generate realistic review comments.
-   **Integration**: Automatically transforms generated data and loads it into Supabase using the production ETL pipeline.

## Usage

Run the generator from the project root:

```bash
python -m ordergen.main --count <number_of_orders>
```

### Examples

Generate 10 new orders:
```bash
python -m ordergen.main --count 10
```

Generate 100 new orders:
```bash
python -m ordergen.main --count 100
```

## How it works

1.  **Train**: The `OrderGenerator` reads the CSV files to understand:
    -   Valid Product IDs and their prices.
    -   Valid Seller IDs.
    -   Real zip codes and cities (for realistic customer locations).
    -   Review text patterns (for generating comments).
2.  **Generate**: It creates new entities (Customers, Orders, Items, Payments, Reviews) using probability distributions and `Faker`.
3.  **Transform**: The generated data is passed through the standard `etl_prod` transformers to ensure schema compliance and data quality.
4.  **Load**: The transformed data is upserted into Supabase using the `load_incremental` function.
