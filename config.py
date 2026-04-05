from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "3610020801-eng.csv"

APP_TITLE = "Canadian Productivity Dashboard"
APP_ICON = "📈"

DEFAULT_METRIC = "Labour productivity"
DEFAULT_INDUSTRIES = ["Business sector"]
DEFAULT_YEAR_WINDOW = 15

MAX_COMPARISON_SERIES = 6

DATA_SOURCE_CITATION = (
    "Statistics Canada. Table 36-10-0208-01  Multifactor productivity, value-added, "
    "capital input and labour input in the aggregate business sector and major "
    "sub-sectors, by industry"
)
DATA_SOURCE_URL = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610020801"
