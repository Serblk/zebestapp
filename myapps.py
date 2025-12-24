import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
    QPushButton, QComboBox, QMessageBox, QTextEdit
)

MROT = 15279

class SalaryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Расчет доходной части заработной платы")
        self.setGeometry(200, 200, 450, 420)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Количество рабочих дней:"))
        self.work_days = QLineEdit()
        layout.addWidget(self.work_days)

        layout.addWidget(QLabel("Количество отработанных дней:"))
        self.worked_days = QLineEdit()
        layout.addWidget(self.worked_days)

        layout.addWidget(QLabel("Тарифный разряд:"))
        self.grade = QComboBox()
        self.grade.addItems(["1", "2", "3", "4"])
        layout.addWidget(self.grade)

        # Кнопки
        self.btn_oklad = QPushButton("Расчет оклада работника")
        self.btn_oklad.clicked.connect(self.calc_oklad)
        layout.addWidget(self.btn_oklad)

        self.btn_salary = QPushButton("З/п")
        self.btn_salary.clicked.connect(self.calc_salary)
        layout.addWidget(self.btn_salary)

        self.btn_dyn = QPushButton("Динамика заработной платы")
        self.btn_dyn.clicked.connect(self.show_dyn)
        layout.addWidget(self.btn_dyn)

        # Вывод результатов
        layout.addWidget(QLabel("Оклад (руб):"))
        self.oklad_out = QLineEdit()
        self.oklad_out.setReadOnly(True)
        layout.addWidget(self.oklad_out)

        layout.addWidget(QLabel("Заработная плата (руб):"))
        self.salary_out = QLineEdit()
        self.salary_out.setReadOnly(True)
        layout.addWidget(self.salary_out)

        layout.addWidget(QLabel("Динамика (отработано / болезнь):"))
        self.dyn_out = QTextEdit()
        self.dyn_out.setReadOnly(True)
        layout.addWidget(self.dyn_out)

    def coef(self):
        # коэффициент по разряду
        r = int(self.grade.currentText())
        if r == 1:
            return 1.00
        if r == 2:
            return 1.05
        if r == 3:
            return 1.10
        return 1.15

    def get_numbers(self):
        if self.work_days.text() == "" or self.worked_days.text() == "":
            raise Exception("Заполните оба поля с днями.")

        wd = int(self.work_days.text())
        wkd = int(self.worked_days.text())

        if wd <= 0:
            raise Exception("Рабочие дни должны быть больше 0.")
        if wkd < 0:
            raise Exception("Отработанные дни не могут быть отрицательными.")
        if wkd > wd:
            raise Exception("Отработанные дни не могут быть больше рабочих.")

        return wd, wkd

    def calc_oklad(self):
        try:
            k = self.coef()
            oklad = MROT * k
            self.oklad_out.setText(str(round(oklad, 2)))
            self.dyn_out.clear()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def calc_salary(self):
        try:
            wd, wkd = self.get_numbers()
            k = self.coef()
            oklad = MROT * k
            salary = oklad * wkd / wd

            self.oklad_out.setText(str(round(oklad, 2)))
            self.salary_out.setText(str(round(salary, 2)))
            self.dyn_out.clear()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def show_dyn(self):
        try:
            wd, wkd = self.get_numbers()
            sick = wd - wkd

            # чтобы одновременно показать и оклад, и зарплату (по условию не запрещено)
            k = self.coef()
            oklad = MROT * k
            salary = oklad * wkd / wd
            self.oklad_out.setText(str(round(oklad, 2)))
            self.salary_out.setText(str(round(salary, 2)))

            self.dyn_out.setText(
                "Отработанные дни: " + str(wkd) + "\n" +
                "Дни болезни (не отработано): " + str(sick)
            )
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


app = QApplication(sys.argv)
window = SalaryApp()
window.show()
sys.exit(app.exec_())
