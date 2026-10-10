"""Shared transform helpers."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Brazilian state initials -> full names (UTF-8 source of truth, single copy).
STATE_NAMES: dict[str, str] = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}


def map_state_initials(series: pd.Series) -> pd.Series:
    """Map UF initials to full state names; unknown values become NA."""
    return series.map(STATE_NAMES)


def finalize(data: pd.DataFrame) -> pd.DataFrame:
    """Shared cleanup: drop rows with more than one missing value, then dedupe."""
    data = data.dropna(thresh=max(len(data.columns) - 1, 1))
    return data.drop_duplicates()


def load_category_translations(data_dir: str | Path) -> dict[str, str]:
    """Load the optional PT->EN product category lookup. Missing file is non-fatal."""
    path = Path(data_dir) / "product_category_name_translation.csv"
    if not path.exists():
        logger.warning("Category translation file missing at %s; English labels skipped", path)
        return {}
    df = pd.read_csv(path)
    return dict(zip(df["product_category_name"], df["product_category_name_english"]))


def strip_timezone(series: pd.Series) -> pd.Series:
    """Parse datetimes and drop any timezone info so Postgres/JSON accept them."""
    parsed = pd.to_datetime(series, errors="coerce")
    if hasattr(parsed.dtype, "tz") and parsed.dtype.tz is not None:
        parsed = parsed.dt.tz_localize(None)
    return parsed


def nat_to_none(series: pd.Series) -> pd.Series:
    """Convert NaT entries to None so JSON serialization works."""
    mask = pd.isna(series)
    if not mask.any():
        return series
    series = series.astype("object")
    series.loc[mask] = None
    return series
