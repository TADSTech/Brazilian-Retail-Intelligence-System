# Dataset Setup

The pipeline needs the Olist CSVs in `data/` (gitignored). Two ways to get them.

## Option A: GitHub release

1. Open the repository's [Releases](../../releases) page.
2. Download the dataset archive.
3. Extract the CSVs into `data/`.

## Option B: Kaggle

```bash
pip install kaggle
# Create an API token on Kaggle (Account -> API -> Create New API Token)
# Place kaggle.json in ~/.kaggle/ (chmod 600) or set KAGGLE_CONFIG_DIR

kaggle datasets download -d olistbr/brazilian-ecommerce
unzip brazilian-ecommerce.zip -d data/
```

`kaggle.json` contains credentials. Keep it out of git (`.gitignore` already covers it).

## Expected files in `data/`

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

Override the location with `DATA_DIR` if you store them elsewhere.

## Verify

```bash
ls data/
# expect 9 CSV files
```

## Next

```bash
python -m etl
```

If the directory is missing or a file name does not match, the CLI fails fast with the exact path it expected.
