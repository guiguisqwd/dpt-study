# -*- coding: utf-8 -*-
"""Which day is it in the study plan? (learning day / weekly review / final review / nothing)."""
import datetime as dt
import json
from .paths import PLAN


def schedule():
    return json.loads(PLAN.read_text(encoding="utf-8"))


def day_info(date: str) -> dict:
    S = schedule()
    for d in S["learning_days"]:
        if d["date"] == date:
            return {"kind": "learning", **d}
    if date in S.get("weekly_review_days", []):
        # the learning days of the week that ends on this review day
        end = dt.date.fromisoformat(date)
        week = [d for d in S["learning_days"] if 0 < (end - dt.date.fromisoformat(d["date"])).days <= 7]
        idx = S["weekly_review_days"].index(date) + 1
        return {"kind": "weekly_review", "date": date, "week": idx, "days": week}
    if date in S.get("final_review", []):
        return {"kind": "final_review", "date": date, "days": S["learning_days"]}
    return {"kind": "none", "date": date}


def tomorrow(date: str = None, tz: str = "America/Los_Angeles") -> str:
    if date:
        return (dt.date.fromisoformat(date) + dt.timedelta(days=1)).isoformat()
    return (today(tz) + dt.timedelta(days=1)).isoformat()


def today(tz: str = "America/Los_Angeles") -> dt.date:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(tz)).date()
    except Exception:  # pragma: no cover
        return dt.date.today()


def previous_learning_days(date: str, n: int = 3):
    S = schedule()
    return [d for d in S["learning_days"] if d["date"] < date][-n:]


def days_left(date: str, goal: str = "2026-12-23") -> int:
    return (dt.date.fromisoformat(goal) - dt.date.fromisoformat(date)).days


WEEKDAY = "一二三四五六日"


def weekday_zh(date: str) -> str:
    return "周" + WEEKDAY[dt.date.fromisoformat(date).weekday()]
