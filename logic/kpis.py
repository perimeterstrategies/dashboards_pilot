from __future__ import annotations

import math

import pandas as pd


def _format_value(value: float | None, unit: str) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    if unit == "Dollars":
        return f"${value:,.0f}"
    if unit == "Hours":
        return f"{value:,.0f}"
    return f"{value:,.1f}"


def _format_delta(value: float | None, suffix: str = "") -> str:
    if value is None or pd.isna(value):
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:,.1f}{suffix}"


def summarize_metric(chart_df: pd.DataFrame) -> list[dict[str, str]]:
    if chart_df.empty:
        return []

    latest_year = int(chart_df["year"].max())
    latest_slice = chart_df.loc[chart_df["year"] == latest_year]
    prior_slice = chart_df.loc[chart_df["year"] == latest_year - 1]
    starting_year = int(chart_df["year"].min())
    starting_slice = chart_df.loc[chart_df["year"] == starting_year]

    latest_avg = latest_slice["value"].mean()
    prior_avg = prior_slice["value"].mean() if not prior_slice.empty else math.nan
    starting_avg = starting_slice["value"].mean() if not starting_slice.empty else math.nan
    unit = latest_slice["unit"].dropna().iloc[0] if not latest_slice.empty else ""

    year_over_year = latest_avg - prior_avg if pd.notna(prior_avg) else math.nan
    period_change_pct = (
        ((latest_avg / starting_avg) - 1) * 100 if pd.notna(starting_avg) and starting_avg else math.nan
    )

    return [
        {
            "label": f"Average in {latest_year}",
            "value": _format_value(latest_avg, unit),
            "delta": _format_delta(year_over_year),
        },
        {
            "label": "Selected industries",
            "value": f"{chart_df['industry'].nunique()}",
            "delta": f"{starting_year}-{latest_year}",
        },
        {
            "label": "Change since start",
            "value": _format_delta(period_change_pct, "%"),
            "delta": "Average change",
        },
    ]
