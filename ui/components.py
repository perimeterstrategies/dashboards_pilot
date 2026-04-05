from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_sidebar_filters(options: dict, defaults: dict) -> dict:
    st.sidebar.header("Filters")

    metric = st.sidebar.selectbox(
        "Metric",
        options["metrics"],
        index=options["metrics"].index(defaults["metric"]),
    )
    industries = st.sidebar.multiselect(
        "Industry",
        options["industries"],
        default=defaults["industries"],
    )
    year_range = st.sidebar.slider(
        "Year range",
        min_value=options["year_range"][0],
        max_value=options["year_range"][1],
        value=defaults["year_range"],
    )

    if not industries:
        industries = defaults["industries"]

    return {
        "metric": metric,
        "industries": industries,
        "year_range": year_range,
    }


def render_metric_cards(cards: list[dict[str, str]]) -> None:
    if not cards:
        return

    columns = st.columns(len(cards))
    for column, card in zip(columns, cards):
        column.metric(card["label"], card["value"], card["delta"])


def render_line_chart(
    dataset: pd.DataFrame,
    value_column: str,
    title: str,
    description: str,
    y_axis_title: str,
) -> None:
    st.subheader(title)
    st.write(description)

    if dataset.empty:
        st.info("No data matches the current selection.")
        return

    fig = px.line(
        dataset,
        x="year",
        y=value_column,
        color="industry",
        markers=False,
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title_text="Industry",
        yaxis_title=y_axis_title,
        xaxis_title="Year",
    )
    st.plotly_chart(fig, use_container_width=True)
