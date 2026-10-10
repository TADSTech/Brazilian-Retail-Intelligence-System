# data/ — Olist dataset goes here

This folder ships empty on purpose: the CSVs are gitignored (~190 MB uncompressed) and must be added locally.

## Quick setup

Download `brazilian-ecommerce.zip` from the
[GitHub releases page](../../releases), then extract it **into this folder**
(the zip contains the CSVs at its root, not a `data/` folder):

```bash
unzip brazilian-ecommerce.zip -d data/        # macOS/Linux
# PowerShell: Expand-Archive brazilian-ecommerce.zip -DestinationPath data
```

No GitHub download? Use Kaggle instead — see
[dataset setup](../docs/dataset_setup.md) for the `kaggle` CLI steps.

## Expected files (9)

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv    # optional
```

## Verify

```bash
ls data/    # expect 9 CSV files (plus this README)
python -m etl --tables orders             # smoke test on one table
```

The ETL fails fast with the exact path it expected if a file is missing.
See [dataset setup](../docs/dataset_setup.md) for details and overrides (`DATA_DIR`).
