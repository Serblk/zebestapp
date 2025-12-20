# Расчет доходной части заработной платы (PyQt5)

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QIntValidator

MROT = 15279
TARIFF_COEFFICIENTS = {
    1: 1.00,
    2: 1.05,
    3: 1.10,
    4: 1.15
}
PAST_MONTH_SALARY = 32000


class SalaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Расчет доходной части заработной платы")
        self.setGeometry(200, 200, 600, 520)

        layout = QVBoxLayout(self)

        title = QLabel("Расчет доходной части заработной платы")
        layout.addWidget(title)

        # Поля ввода
        self.label_work_days = QLabel("Количество рабочих дней:")
        self.edit_work_days = QLineEdit()
        self.edit_work_days.setValidator(QIntValidator(0, 366, self))

        self.label_worked_days = QLabel("Количество отработанных дней:")
        self.edit_worked_days = QLineEdit()
        self.edit_worked_days.setValidator(QIntValidator(0, 366, self))

        self.label_grade = QLabel("Тарифный разряд:")
        self.combo_grade = QComboBox()
        self.combo_grade.addItems(["1", "2", "3", "4"])

        layout.addWidget(self.label_work_days)
        layout.addWidget(self.edit_work_days)
        layout.addWidget(self.label_worked_days)
        layout.addWidget(self.edit_worked_days)
        layout.addWidget(self.label_grade)
        layout.addWidget(self.combo_grade)

        # Кнопки
        buttons_row = QHBoxLayout()

        self.btn_oklad = QPushButton("Расчет оклада работника")
        self.btn_oklad.clicked.connect(self.calculate_oklad)

        self.btn_salary = QPushButton("З/п")
        self.btn_salary.clicked.connect(self.calculate_salary)

        self.btn_dynamics = QPushButton("Динамика заработной платы")
        self.btn_dynamics.clicked.connect(self.show_dynamics)

        buttons_row.addWidget(self.btn_oklad)
        buttons_row.addWidget(self.btn_salary)
        buttons_row.addWidget(self.btn_dynamics)
        layout.addLayout(buttons_row)

        # Поля вывода
        layout.addWidget(QLabel("Оклад (руб):"))
        self.edit_oklad_out = QLineEdit()
        self.edit_oklad_out.setReadOnly(True)
        layout.addWidget(self.edit_oklad_out)

        layout.addWidget(QLabel("Заработная плата (руб):"))
        self.edit_salary_out = QLineEdit()
        self.edit_salary_out.setReadOnly(True)
        layout.addWidget(self.edit_salary_out)

        layout.addWidget(QLabel("Вывод динамики:"))
        self.text_dynamics = QTextEdit()
        self.text_dynamics.setReadOnly(True)
        layout.addWidget(self.text_dynamics)

    def _get_inputs(self):
        work_days_text = self.edit_work_days.text().strip()
        worked_days_text = self.edit_worked_days.text().strip()

        if not work_days_text or not worked_days_text:
            raise ValueError("Заполните поля: количество рабочих дней и количество отработанных дней.")

        work_days = int(work_days_text)
        worked_days = int(worked_days_text)

        if work_days <= 0:
            raise ValueError("Количество рабочих дней должно быть больше 0.")

        if worked_days < 0:
            raise ValueError("Количество отработанных дней не может быть отрицательным.")

        if worked_days > work_days:
            raise ValueError("Отработанных дней не может быть больше, чем рабочих дней.")

        grade = int(self.combo_grade.currentText())
        coef = TARIFF_COEFFICIENTS[grade]

        return work_days, worked_days, grade, coef

    def _compute_oklad(self, coef):
        return MROT * coef

    def _compute_salary(self, oklad, worked_days, work_days):
        return oklad * worked_days / work_days

    def _show_error(self, message):
        QMessageBox.warning(self, "Ошибка ввода", message)

    def calculate_oklad(self):
        try:
            _, _, grade, coef = self._get_inputs()
            oklad = self._compute_oklad(coef)
            self.edit_oklad_out.setText(f"{oklad:.2f}")
            self.text_dynamics.clear()
        except Exception as e:
            self._show_error(str(e))

    def calculate_salary(self):
        try:
            work_days, worked_days, grade, coef = self._get_inputs()
            oklad = self._compute_oklad(coef)
            salary = self._compute_salary(oklad, worked_days, work_days)

            self.edit_oklad_out.setText(f"{oklad:.2f}")
            self.edit_salary_out.setText(f"{salary:.2f}")
            self.text_dynamics.clear()
        except Exception as e:
            self._show_error(str(e))

    def show_dynamics(self):
        try:
            work_days, worked_days, grade, coef = self._get_inputs()
            sick_days = work_days - worked_days

            oklad = self._compute_oklad(coef)
            salary = self._compute_salary(oklad, worked_days, work_days)

            delta = salary - PAST_MONTH_SALARY
            delta_percent = (delta / PAST_MONTH_SALARY * 100) if PAST_MONTH_SALARY != 0 else 0

            self.edit_oklad_out.setText(f"{oklad:.2f}")
            self.edit_salary_out.setText(f"{salary:.2f}")

            text = []
            text.append(f"Тарифный разряд: {grade}")
            text.append(f"Тарифный коэффициент: {coef:.2f}")
            text.append(f"МРОТ: {MROT} руб.")
            text.append("")
            text.append(f"Рабочие дни: {work_days}")
            text.append(f"Отработанные дни: {worked_days}")
            text.append(f"Дни болезни (не отработано): {sick_days}")
            text.append("")
            text.append(f"Оклад = МРОТ × коэффициент = {MROT} × {coef:.2f} = {oklad:.2f} руб.")
            text.append(f"З/п = оклад × отработанные / рабочие = {oklad:.2f} × {worked_days}/{work_days} = {salary:.2f} руб.")
            text.append("")
            text.append(f"З/п за прошлый месяц: {PAST_MONTH_SALARY:.2f} руб.")
            text.append(f"Изменение: {delta:+.2f} руб. ({delta_percent:+.2f}%)")

            self.text_dynamics.setPlainText("\n".join(text))
        except Exception as e:
            self._show_error(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalaryApp()
    window.show()
    sys.exit(app.exec_())
