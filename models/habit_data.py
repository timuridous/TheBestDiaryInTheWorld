from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Tuple, Literal


GoalKind = Literal["check", "number"]


@dataclass
class Goal:
    name: str
    kind: GoalKind  # "check" for checkbox, "number" for numeric input


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
    """In-memory goal completion/values keyed by (date, goal_name)."""

    checked: Dict[Tuple[date, str], bool] = field(default_factory=dict)
    numeric: Dict[Tuple[date, str], float] = field(default_factory=dict)

    def is_checked(self, day: date, goal_name: str) -> bool:
        return self.checked.get((day, goal_name), False)

    def set_checked(self, day: date, goal_name: str, value: bool) -> None:
        self.checked[(day, goal_name)] = value

    def get_number(self, day: date, goal_name: str) -> float | None:
        return self.numeric.get((day, goal_name))

    def set_number(self, day: date, goal_name: str, value: float | None) -> None:
        key = (day, goal_name)
        if value is None:
            self.numeric.pop(key, None)
        else:
            self.numeric[key] = value

    def count_completed_for_week(self, week: WeekInfo, goals: List[Goal]) -> int:
        """Count completed checkbox goals for the given week."""
        count = 0
        checkbox_goals = [g for g in goals if g.kind == "check"]
        for day in week.days:
            for goal in checkbox_goals:
                if self.is_checked(day, goal.name):
                    count += 1
        return count

    @staticmethod
    def total_slots_for_week(week: WeekInfo, goals: List[Goal]) -> int:
        """Total number of checkbox cells in the week."""
        checkbox_count = len([g for g in goals if g.kind == "check"])
        return checkbox_count * len(week.days)

