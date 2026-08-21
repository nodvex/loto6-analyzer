import csv
import io
import requests
from datetime import datetime

CSV_URL = "https://loto6.thekyo.jp/data/loto6.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
        "AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1"
    )
}


def get_csv():
    r = requests.get(CSV_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    # 日本語CSVでよく使われる文字コードを順番に試す
    for enc in ("cp932", "shift_jis", "utf-8-sig", "utf-8"):
        try:
            return r.content.decode(enc)
        except UnicodeDecodeError:
            pass

    raise RuntimeError("CSV encoding could not be detected")


def to_int(value):
    s = str(value).strip().replace(",", "")
    return int(s)


def normalize_date(value):
    s = str(value).strip()

    formats = (
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%Y年%m月%d日",
        "%Y.%m.%d",
    )

    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError(f"Unknown date format: {s}")


def find_column(headers, candidates):
    for h in headers:
        clean = h.replace(" ", "").replace("　", "").lower()
        for candidate in candidates:
            if candidate.lower() in clean:
                return h
    return None


def load_rows():
    text = get_csv()
    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames:
        raise ValueError("CSV has no header")

    fields = reader.fieldnames

    draw_col = find_column(fields, ["回", "開催回", "回号"])
    date_col = find_column(fields, ["抽選日", "抽せん日", "日付"])

    number_cols = []
    for i in range(1, 7):
        col = find_column(
            fields,
            [
                f"第{i}数字",
                f"本数字{i}",
                f"数字{i}",
            ],
        )
        if col:
            number_cols.append(col)

    bonus_col = find_column(
        fields,
        ["ボーナス", "bonus", "b数字", "bo"],
    )

    if not draw_col or not date_col:
        raise ValueError(f"Required columns not found: {fields}")

    if len(number_cols) != 6:
        raise ValueError(f"Six number columns not found: {fields}")

    if not bonus_col:
        raise ValueError(f"Bonus column not found: {fields}")

    out = []

    for row in reader:
        try:
            draw = to_int(row[draw_col])
            numbers = sorted(to_int(row[c]) for c in number_cols)
            bonus = to_int(row[bonus_col])
            date = normalize_date(row[date_col])

            if len(numbers) != 6:
                continue

            if len(set(numbers)) != 6:
                continue

            if not all(1 <= n <= 43 for n in numbers):
                continue

            if not 1 <= bonus <= 43:
                continue

            if bonus in numbers:
                continue

            out.append(
                {
                    "draw": draw,
                    "date": date,
                    "numbers": numbers,
                    "bonus": bonus,
                }
            )

        except Exception:
            continue

    out = list({x["draw"]: x for x in out}.values())
    out.sort(key=lambda x: x["draw"])

    if not out:
        raise ValueError("No valid Loto6 rows found")

    return out


def range_page(a, b):
    rows = load_rows()
    return [x for x in rows if a <= x["draw"] <= b]


def current():
    rows = load_rows()
    return rows[-20:]
