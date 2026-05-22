#!/usr/bin/env python3
import calendar
import json
from datetime import date

today = date.today()

weekday = today.isoweekday()
week_total = 7

month_total = calendar.monthrange(today.year, today.month)[1]
month_elapsed = today.day

quarter = (today.month - 1) // 3 + 1
q_start_month = (quarter - 1) * 3 + 1
q_end_month = q_start_month + 2
q_start = date(today.year, q_start_month, 1)
q_end = date(today.year, q_end_month, calendar.monthrange(today.year, q_end_month)[1])
q_total = (q_end - q_start).days + 1
q_elapsed = (today - q_start).days + 1

y_start = date(today.year, 1, 1)
y_end = date(today.year, 12, 31)
y_total = (y_end - y_start).days + 1
y_elapsed = (today - y_start).days + 1


def fmt(label, elapsed, total):
    pct = elapsed / total * 100
    rem = 100 - pct
    return f"{label}: {pct:.2f}% | {rem:.2f}% | {elapsed}/{total}"


rows = [
    ("Week", weekday, week_total, "Day {} of 7 (Mon-Sun)".format(weekday)),
    ("Month", month_elapsed, month_total, today.strftime("%B %Y")),
    ("Quarter", q_elapsed, q_total, f"Q{quarter} {today.year}"),
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
    "subtitle": "Copy all four lines to clipboard",
    "arg": all_lines,
    "text": {"copy": all_lines, "largetype": all_lines},
    "valid": True,
})

print(json.dumps({"items": items}))
