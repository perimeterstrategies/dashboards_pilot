import streamlit as st

from data.connection import load_productivity_dataset
from data.queries import DataFilters, apply_filters, get_filter_options
from logic.kpis import summarize_metric
from logic.transforms import (
    build_default_selection,
    build_indexed_comparison,
    chart_dataset,
    describe_selection,
)
from ui.components import render_line_chart, render_metric_cards, render_sidebar_filters
from ui.layouts import configure_page, render_header


def main() -> None:
    configure_page()
    render_header()

    dataset = load_productivity_dataset()
    options = get_filter_options(dataset)
    defaults = build_default_selection(options)
    sidebar_state = render_sidebar_filters(options, defaults)

    filters = DataFilters(
        industries=tuple(sidebar_state["industries"]),
        metrics=(sidebar_state["metric"],),
        year_range=tuple(sidebar_state["year_range"]),
    )
    filtered_dataset = apply_filters(dataset, filters)
    metric_df = chart_dataset(filtered_dataset, sidebar_state["metric"])
    descriptions = describe_selection(metric_df, sidebar_state["metric"])

    render_metric_cards(summarize_metric(metric_df))

    unit = metric_df["unit"].dropna().iloc[0] if not metric_df.empty else "Value"
    render_line_chart(
        metric_df,
        value_column="value",
        title=f"{sidebar_state['metric']} over time",
        description=descriptions["headline"],
        y_axis_title=unit or "Value",
    )

    comparison_df = build_indexed_comparison(metric_df)
    render_line_chart(
        comparison_df,
        value_column="indexed_value",
        title="Indexed growth comparison",
        description=descriptions["comparison"],
        y_axis_title="Index (start year = 100)",
    )


if __name__ == "__main__":
    main()
