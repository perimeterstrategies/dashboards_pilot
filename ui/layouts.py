import streamlit as st

from config import APP_ICON, APP_TITLE


def configure_page() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
    )


def render_header() -> None:
    st.title(APP_TITLE)
    st.caption(
        "A streamlined view of Statistics Canada productivity, GDP, labour, and capital trends "
        "for the Canadian business sector and major industries."
    )
