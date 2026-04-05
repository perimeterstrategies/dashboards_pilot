from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataFilters:
    industries: tuple[str, ...]
    metrics: tuple[str, ...]
    year_range: tuple[int, int]


def get_filter_options(dataset: pd.DataFrame) -> dict[str, list[str] | tuple[int, int]]:
    years = sorted(dataset["year"].dropna().unique().tolist())
    return {
        "industries": sorted(dataset["industry"].dropna().unique().tolist()),
        "metrics": sorted(dataset["metric"].dropna().unique().tolist()),
        "year_range": (int(min(years)), int(max(years))),
    }


def apply_filters(dataset: pd.DataFrame, filters: DataFilters) -> pd.DataFrame:
    start_year, end_year = filters.year_range
    mask = dataset["year"].between(start_year, end_year)

    if filters.industries:
        mask &= dataset["industry"].isin(filters.industries)
    if filters.metrics:
        mask &= dataset["metric"].isin(filters.metrics)

    return dataset.loc[mask].copy()
