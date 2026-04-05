import csv
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

from config import DATA_FILE


HEADER_METRIC_ROW = 9
HEADER_YEAR_ROW = 10
HEADER_UNIT_ROW = 11
DATA_START_ROW = 12


def _clean_metric_name(name: str) -> str:
    """Strip StatsCan footnote markers while preserving readable labels."""
    return re.sub(r"\s+\d+$", "", name).strip()


def _clean_numeric(value: str) -> float | None:
    value = value.strip()
    if value in {"", ".."}:
        return None

    normalized = value.replace(",", "")
    numeric_match = re.search(r"-?\d+(?:\.\d+)?", normalized)
    if not numeric_match:
        return None

    return float(numeric_match.group(0))


def _read_csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


@lru_cache(maxsize=1)
def load_productivity_dataset(path: str | None = None) -> pd.DataFrame:
    """
    Load the StatsCan wide-format CSV and convert it to a tidy dataframe.

    Output columns:
    - industry
    - metric
    - unit
    - year
    - value
    """
    source_path = Path(path) if path else DATA_FILE
    rows = _read_csv_rows(source_path)

    metric_row = rows[HEADER_METRIC_ROW]
    year_row = rows[HEADER_YEAR_ROW]
    unit_row = rows[HEADER_UNIT_ROW]

    headers: list[tuple[int, str, str, int]] = []
    current_metric = ""
    current_unit = ""
    for index in range(1, len(year_row)):
        if metric_row[index]:
            current_metric = _clean_metric_name(metric_row[index])
        if unit_row[index]:
            current_unit = unit_row[index].strip()

        headers.append((index, current_metric, current_unit, int(year_row[index])))

    records: list[dict[str, object]] = []
    for row in rows[DATA_START_ROW:]:
        if not row or not row[0].strip():
            break

        industry = _clean_metric_name(row[0])
        for column_index, metric, unit, year in headers:
            records.append(
                {
                    "industry": industry,
                    "metric": metric,
                    "unit": unit,
                    "year": year,
                    "value": _clean_numeric(row[column_index]),
                }
            )

    dataset = pd.DataFrame.from_records(records)
    dataset["year"] = dataset["year"].astype(int)
    dataset["metric"] = dataset["metric"].astype(str)
    dataset["industry"] = dataset["industry"].astype(str)
    dataset["unit"] = dataset["unit"].fillna("").astype(str)
    dataset["value"] = pd.to_numeric(dataset["value"], errors="coerce")

    return dataset
