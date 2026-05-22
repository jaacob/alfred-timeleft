#!/usr/bin/env python3
import calendar
import json
import os
from datetime import date


def env_bool(name, default=True):
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return v == "1"


def weekdays_between(d_from, d_to):
    if d_to < d_from:
        return 0
    total_days = (d_to - d_from).days + 1
    full_weeks, remainder = divmod(total_days, 7)
    weekdays = full_weeks * 5
    weekday_start = d_from.isoweekday()
    for i in range(remainder):
        if ((weekday_start - 1 + i) % 7) < 5:
            weekdays += 1
    return weekdays


today = date.today()
notices = []
rows = []

raw_year_end = os.environ.get("YEAR_END_DATE", "").strip()
year_end = date(today.year, 12, 31)
if raw_year_end:
    try:
        parsed = date.fromisoformat(raw_year_end)
        if parsed.year == today.year:
            year_end = parsed
        else:
            notices.append({
                "title": f"Year-end date reset to Dec 31, {today.year}",
                "subtitle": f"Saved date {raw_year_end} is from a previous year. Update via Configure Workflow.",
                "arg": "",
                "valid": False,
            })
    except ValueError:
        notices.append({
            "title": f"Year-end date '{raw_year_end}' is invalid",
            "subtitle": "Use YYYY-MM-DD or leave blank. Update via Configure Workflow.",
            "arg": "",
            "valid": False,
        })

if env_bool("SHOW_WEEK"):
    weekday = today.isoweekday()
    if env_bool("WEEK_BUSINESS_DAYS"):
        elapsed, total = min(weekday, 5), 5
        subtitle = f"Day {elapsed} of 5 (Mon-Fri)"
    else:
        elapsed, total = weekday, 7
        subtitle = f"Day {elapsed} of 7"
    rows.append(("Week", elapsed, total, subtitle))

if env_bool("SHOW_MONTH"):
    last_day = calendar.monthrange(today.year, today.month)[1]
    m_start = date(today.year, today.month, 1)
    m_end = date(today.year, today.month, last_day)
    if env_bool("MONTH_BUSINESS_DAYS"):
        total = weekdays_between(m_start, m_end)
        elapsed = weekdays_between(m_start, today)
    else:
        total, elapsed = last_day, today.day
    rows.append(("Month", elapsed, total, today.strftime("%B %Y")))

if env_bool("SHOW_QUARTER"):
    quarter = (today.month - 1) // 3 + 1
    q_start = date(today.year, (quarter - 1) * 3 + 1, 1)
    q_end_month = (quarter - 1) * 3 + 3
    q_end = date(today.year, q_end_month, calendar.monthrange(today.year, q_end_month)[1])
    if env_bool("QUARTER_BUSINESS_DAYS"):
        total = weekdays_between(q_start, q_end)
        elapsed = weekdays_between(q_start, min(today, q_end))
    else:
        total = (q_end - q_start).days + 1
        elapsed = (min(today, q_end) - q_start).days + 1
    rows.append(("Quarter", elapsed, total, f"Q{quarter} {today.year}"))

if env_bool("SHOW_YEAR"):
    y_start = date(today.year, 1, 1)
    if env_bool("YEAR_BUSINESS_DAYS"):
        total = weekdays_between(y_start, year_end)
        elapsed = min(weekdays_between(y_start, today), total)
    else:
        total = (year_end - y_start).days + 1
        elapsed = min((today - y_start).days + 1, total)
    rows.append(("Year", elapsed, total, str(today.year)))


def fmt(label, elapsed, total):
    pct = elapsed / total * 100
    rem = 100 - pct
    return f"{label}: {pct:.2f}% | {rem:.2f}% | {elapsed}/{total}"


items = list(notices)

if not rows:
    items.append({
        "title": "No periods enabled",
        "subtitle": "Open Configure Workflow to turn at least one period on.",
        "arg": "",
        "valid": False,
    })
else:
    for label, elapsed, total, subtitle in rows:
        line = fmt(label, elapsed, total)
        items.append({
            "title": line,
            "subtitle": subtitle,
            "arg": line,
            "text": {"copy": line, "largetype": line},
            "valid": True,
        })

    if len(rows) > 1:
        all_lines = "\n".join(fmt(label, elapsed, total) for label, elapsed, total, _ in rows)
        items.append({
            "title": "Copy all",
            "subtitle": f"Copy all {len(rows)} lines to clipboard",
            "arg": all_lines,
            "text": {"copy": all_lines, "largetype": all_lines},
            "valid": True,
        })

print(json.dumps({"items": items}))
