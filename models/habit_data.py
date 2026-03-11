from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Tuple


HABITS: List[str] = [
    "Exercise",
    "Read",
    "Meditate",
    "Healthy Eating",
    "Sleep 8hrs",
]


@dataclass
class WeekInfo:
    start_date: date
    end_date: date
    days: List[date]


def get_week_for(reference_day: date | None = None) -> WeekInfo:
    """Return a Sunday–Saturday week containing reference_day."""
    ref = reference_day or date.today()
    # weekday(): Monday=0 ... Sunday=6, so compute days since Sunday
    days_since_sunday = (ref.weekday() + 1) % 7
    start = ref - timedelta(days=days_since_sunday)
    days = [start + timedelta(days=i) for i in range(7)]
    end = days[-1]
    return WeekInfo(start_date=start, end_date=end, days=days)


@dataclass
class HabitState:
    """In-memory habit completion state keyed by (date, habit)."""

    checked: Dict[Tuple[date, str], bool] = field(default_factory=dict)

    def is_checked(self, day: date, habit: str) -> bool:
        return self.checked.get((day, habit), False)

    def set_checked(self, day: date, habit: str, value: bool) -> None:
        self.checked[(day, habit)] = value

    def count_completed_for_week(self, week: WeekInfo) -> int:
        count = 0
        for day in week.days:
            for habit in HABITS:
                if self.is_checked(day, habit):
                    count += 1
        return count

    @staticmethod
    def total_slots_for_week(week: WeekInfo) -> int:
        return len(HABITS) * len(week.days)

