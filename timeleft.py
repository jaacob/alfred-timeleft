#!/usr/bin/env python3
import calendar
import json
from datetime import date, timedelta

today = date.today()

weekday = today.isoweekday()
week_elapsed = min(weekday, 5)
week_total = 5

days_in_month = calendar.monthrange(today.year, today.month)[1]
month_total = sum(
    1 for d in range(1, days_in_month + 1)
    if date(today.year, today.month, d).isoweekday() <= 5
)
month_elapsed = sum(
    1 for d in range(1, today.day + 1)
    if date(today.year, today.month, d).isoweekday() <= 5
)

dec1 = date(today.year, 12, 1)
first_friday_day = 1 + ((5 - dec1.isoweekday()) % 7)
year_end = date(today.year, 12, first_friday_day) + timedelta(days=14)

y_start = date(today.year, 1, 1)
y_total = (year_end - y_start).days + 1
y_elapsed = min((today - y_start).days + 1, y_total)


def fmt(label, elapsed, total):
    pct = elapsed / total * 100
    rem = 100 - pct
    return f"{label}: {pct:.2f}% | {rem:.2f}% | {elapsed}/{total}"


rows = [
    ("Week", week_elapsed, week_total, f"Day {week_elapsed} of 5 (Mon-Fri)"),
    ("Month", month_elapsed, month_total, today.strftime("%B %Y")),
    ("Year", y_elapsed, y_total, str(today.year)),
]

items = []
for label, elapsed, total, subtitle in rows:
    line = fmt(label, elapsed, total)
    items.append({
        "title": line,
        "subtitle": subtitle,
        "arg": line,
        "text": {"copy": line, "largetype": line},
        "valid": True,
    })

# Add a combined "copy all" entry at the bottom
all_lines = "\n".join(fmt(label, elapsed, total) for label, elapsed, total, _ in rows)
items.append({
    "title": "Copy all",
    "subtitle": "Copy all three lines to clipboard",
    "arg": all_lines,
    "text": {"copy": all_lines, "largetype": all_lines},
    "valid": True,
})

print(json.dumps({"items": items}))
