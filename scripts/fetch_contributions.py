#!/usr/bin/env python3
"""
fetch_contributions.py
Avi Vashishta's exact scraper for daily contribution data from GitHub public endpoint.
Writes data/contributions.json with raw days + derived stats.
"""
import datetime
import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "Bleezbub")
URL = f"https://github.com/users/{USERNAME}/contributions"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT_PATH = os.path.join(ROOT, "data", "contributions.json")


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("[data-date]")
    if not cells:
        print("no calendar cells found", file=sys.stderr)
        sys.exit(1)

    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        td_id = td.get("id")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.search(r"(\d+)\s+contribution", text, re.I)
            if m:
                count = int(m.group(1))
            else:
                m_start = re.match(r"(\d+)", text)
                count = int(m_start.group(1)) if m_start else 0
        days.append({"date": date, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    if not days:
        return {"length": 0, "start": "", "end": ""}
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    if streak == 0:
        return {"length": 0, "start": "", "end": ""}
    return {
        "length": streak,
        "start": days[idx + 1]["date"],
        "end": days[end_idx]["date"],
    }


def compute_longest_streak(days):
    best = 0
    best_start = ""
    best_end = ""
    curr = 0
    curr_start = ""
    for d in days:
        if d["count"] > 0:
            if curr == 0:
                curr_start = d["date"]
            curr += 1
            if curr > best:
                best = curr
                best_start = curr_start
                best_end = d["date"]
        else:
            curr = 0
    return {"length": best, "start": best_start, "end": best_end}


def compute_best_day(days):
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    return {"date": best["date"], "count": best["count"]}


def main():
    print(f"Fetching contributions for {USERNAME}...")
    days = fetch_days()
    total = sum(d["count"] for d in days)
    cur_streak = compute_current_streak(days)
    long_streak = compute_longest_streak(days)
    best_day = compute_best_day(days)

    first_date = days[0]["date"]
    last_date = days[-1]["date"]

    payload = {
        "user": USERNAME,
        "updated": datetime.datetime.utcnow().isoformat() + "Z",
        "total_contributions": total,
        "range": {"start": first_date, "end": last_date},
        "current_streak": cur_streak,
        "longest_streak": long_streak,
        "best_day": best_day,
        "days": days,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[OK] Saved {OUT_PATH} ({total} contributions)")


if __name__ == "__main__":
    main()
