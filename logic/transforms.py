from __future__ import annotations

from typing import Any

import pandas as pd

from config import DEFAULT_INDUSTRIES, DEFAULT_METRIC, DEFAULT_YEAR_WINDOW, MAX_COMPARISON_SERIES


def build_default_selection(options: dict[str, Any]) -> dict[str, Any]:
    min_year, max_year = options["year_range"]
    default_start_year = max(min_year, max_year - DEFAULT_YEAR_WINDOW + 1)

    industries = [
        industry
        for industry in DEFAULT_INDUSTRIES
        if industry in options["industries"]
    ] or options["industries"][:1]

    metric = DEFAULT_METRIC if DEFAULT_METRIC in options["metrics"] else options["metrics"][0]

    return {
        "industries": industries,
        "metric": metric,
        "year_range": (default_start_year, max_year),
    }


def chart_dataset(dataset: pd.DataFrame, selected_metric: str) -> pd.DataFrame:
    chart_df = dataset.loc[dataset["metric"] == selected_metric].dropna(subset=["value"]).copy()
    return chart_df.sort_values(["year", "industry"])


def latest_observations(chart_df: pd.DataFrame) -> pd.DataFrame:
    if chart_df.empty:
        return chart_df

    latest_year = int(chart_df["year"].max())
    return chart_df.loc[chart_df["year"] == latest_year].sort_values("value", ascending=False)


def build_indexed_comparison(chart_df: pd.DataFrame) -> pd.DataFrame:
    if chart_df.empty:
        return chart_df

    filtered = chart_df.sort_values(["industry", "year"]).copy()
    series_counts = filtered["industry"].nunique()
    if series_counts > MAX_COMPARISON_SERIES:
        top_industries = (
            latest_observations(filtered)["industry"].head(MAX_COMPARISON_SERIES).tolist()
        )
        filtered = filtered.loc[filtered["industry"].isin(top_industries)].copy()

    first_values = (
        filtered.groupby("industry", as_index=False)
        .first()[["industry", "value"]]
        .rename(columns={"value": "baseline_value"})
    )
    indexed = filtered.merge(first_values, on="industry", how="left")
    indexed["indexed_value"] = (indexed["value"] / indexed["baseline_value"]) * 100
    return indexed


def describe_selection(chart_df: pd.DataFrame, selected_metric: str) -> dict[str, str]:
    if chart_df.empty:
        return {
            "headline": f"No data available for {selected_metric.lower()} in the selected filters.",
            "comparison": "Adjust the filters to view a trend or benchmark comparison.",
        }

    min_year = int(chart_df["year"].min())
    max_year = int(chart_df["year"].max())
    industry_count = int(chart_df["industry"].nunique())

    industry_label = "industry" if industry_count == 1 else "industries"
    return {
        "headline": (
            f"This chart shows {selected_metric.lower()} from {min_year} to {max_year} "
            f"for the selected {industry_label}."
        ),
        "comparison": (
            "This comparison rebases each line to 100 at the start of the selected period, "
            "making relative growth easier to compare across industries."
        ),
    }
