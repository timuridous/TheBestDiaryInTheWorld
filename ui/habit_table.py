from __future__ import annotations

from datetime import date
from typing import Callable, List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

from models.habit_data import HABITS, HabitState, WeekInfo


class HabitTable(QTableWidget):
    """Table showing habits (rows) vs days (columns) with checkboxes."""

    def __init__(
        self,
        week: WeekInfo,
        state: HabitState,
        on_toggle: Callable[[date, str, bool], None],
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._week = week
        self._state = state
        self._on_toggle = on_toggle

        self._current_day = date.today()

        self.setRowCount(len(HABITS))
        # 1 column for "Habits" + 7 for days
        self.setColumnCount(1 + len(self._week.days))
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

        self._populate_headers()
        self.refresh()

        self.cellChanged.connect(self._handle_cell_changed)

    # --- Public API -----------------------------------------------------

    def set_week(self, week: WeekInfo) -> None:
        self._week = week
        self.setColumnCount(1 + len(self._week.days))
        self._populate_headers()
        self.refresh()

    def refresh(self) -> None:
        self.blockSignals(True)
        try:
            self._populate_body()
            self._highlight_current_day()
        finally:
            self.blockSignals(False)

    # --- Internal helpers -----------------------------------------------

    def _populate_headers(self) -> None:
        habits_header = QTableWidgetItem("Habits")
        habits_header.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.setHorizontalHeaderItem(0, habits_header)

        for idx, day in enumerate(self._week.days, start=1):
            text = f"{day.strftime('%a')}\n{day.strftime('%b %-d') if hasattr(day, 'strftime') else ''}"
            # On Windows, %-d may not be supported; fall back gracefully.
            try:
                date_str = day.strftime("%b %-d")
            except ValueError:
                date_str = day.strftime("%b %d").lstrip("0")
            text = f"{day.strftime('%a')}\n{date_str}"
            header = QTableWidgetItem(text)
            header.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setHorizontalHeaderItem(idx, header)

    def _populate_body(self) -> None:
        for row, habit in enumerate(HABITS):
            habit_item = QTableWidgetItem(habit)
            habit_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setItem(row, 0, habit_item)

            for col, day in enumerate(self._week.days, start=1):
                item = QTableWidgetItem()
                item.setFlags(
                    Qt.ItemFlag.ItemIsUserCheckable
                    | Qt.ItemFlag.ItemIsEnabled
                )
                checked = self._state.is_checked(day, habit)
                item.setCheckState(
                    Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
                )
                self.setItem(row, col, item)

    def _highlight_current_day(self) -> None:
        highlight_color = QBrush(QColor("#f3f4f6"))  # light gray
        today = self._current_day
        for col, day in enumerate(self._week.days, start=1):
            for row in range(self.rowCount()):
                item = self.item(row, col)
                if not item:
                    continue
                if day == today:
                    item.setBackground(highlight_color)
                else:
                    item.setBackground(QBrush())

    def _handle_cell_changed(self, row: int, column: int) -> None:
        if column == 0:
            return
        habit = HABITS[row]
        day_index = column - 1
        if not (0 <= day_index < len(self._week.days)):
            return
        day = self._week.days[day_index]
        item = self.item(row, column)
        if item is None:
            return

        checked = item.checkState() == Qt.CheckState.Checked
        self._on_toggle(day, habit, checked)

