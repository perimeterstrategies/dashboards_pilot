from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "3610020801-eng.csv"

APP_TITLE = "Canadian Productivity Dashboard"
APP_ICON = "📈"

DEFAULT_METRIC = "Labour productivity"
DEFAULT_INDUSTRIES = ["Business sector"]
DEFAULT_YEAR_WINDOW = 15

MAX_COMPARISON_SERIES = 6
