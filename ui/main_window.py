from __future__ import annotations

from datetime import date, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.habit_data import HABITS, HabitState, WeekInfo, get_week_for
from ui.habit_table import HabitTable


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Progress Tracker")
        self._state = HabitState()
        self._current_reference_day = date.today()
        self._week = get_week_for(self._current_reference_day)

        self._build_ui()
        self._update_progress_label()

    # --- UI construction ------------------------------------------------

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        title_label = QLabel("Progress Tracker")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: 600;")

        # Week navigation + progress summary
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(12)

        self.prev_button = QPushButton("◀")
        self.next_button = QPushButton("▶")
        for btn in (self.prev_button, self.next_button):
            btn.setFixedWidth(32)

        self.week_label = QLabel()
        self.week_label.setStyleSheet("font-size: 14px;")

        nav_left = QHBoxLayout()
        nav_left.addWidget(self.prev_button)
        nav_left.addWidget(self.week_label)
        nav_left.addWidget(self.next_button)
        nav_left.addStretch(1)

        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.progress_label.setStyleSheet("color: #6b7280; font-size: 12px;")

        nav_layout.addLayout(nav_left)
        nav_layout.addWidget(self.progress_label)

        # Table
        self.table = HabitTable(
            week=self._week,
            state=self._state,
            on_toggle=self._handle_toggle,
        )

        # Footer
        footer_label = QLabel("Track your daily habits across the week")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("color: #6b7280; font-size: 11px;")

        root_layout.addWidget(title_label)
        root_layout.addLayout(nav_layout)
        root_layout.addWidget(self.table)
        root_layout.addWidget(footer_label)

        self.setCentralWidget(root)
        self.resize(800, 500)

        self._update_week_label()

        # Connections
        self.prev_button.clicked.connect(self._go_to_previous_week)
        self.next_button.clicked.connect(self._go_to_next_week)

    # --- Event handlers -------------------------------------------------

    def _handle_toggle(self, day: date, habit: str, checked: bool) -> None:
        self._state.set_checked(day, habit, checked)
        self._update_progress_label()

    def _go_to_previous_week(self) -> None:
        self._current_reference_day -= timedelta(days=7)
        self._week = get_week_for(self._current_reference_day)
        self.table.set_week(self._week)
        self._update_week_label()
        self._update_progress_label()

    def _go_to_next_week(self) -> None:
        self._current_reference_day += timedelta(days=7)
        self._week = get_week_for(self._current_reference_day)
        self.table.set_week(self._week)
        self._update_week_label()
        self._update_progress_label()

    # --- Helpers --------------------------------------------------------

    def _update_week_label(self) -> None:
        start = self._week.start_date
        end = self._week.end_date
        label = f"{start.strftime('%b %d')} - {end.strftime('%b %d')}"
        self.week_label.setText(label)

    def _update_progress_label(self) -> None:
        completed = self._state.count_completed_for_week(self._week)
        total = self._state.total_slots_for_week(self._week)
        percent = (completed / total * 100) if total else 0.0
        self.progress_label.setText(f"{completed}/{total} completed ({percent:.0f}%)")


def run() -> None:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

