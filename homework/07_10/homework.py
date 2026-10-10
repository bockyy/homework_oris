import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QComboBox,
)

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []

        main_layout = QVBoxLayout()

        self.setWindowTitle("Task Manager")

        task_layout = QHBoxLayout()
        task_layout.addWidget(QLabel("Task:"))
        self.task_name = QLineEdit()
        task_layout.addWidget(self.task_name)
        main_layout.addLayout(task_layout)

        self.about_task = QTextEdit()
        main_layout.addWidget(QLabel("Description:"))
        main_layout.addWidget(self.about_task)

        name_priority_layout = QLabel("Priority:")
        main_layout.addWidget(name_priority_layout)

        priority_layout = QHBoxLayout()
        self.rb_low = QRadioButton("Low")
        self.rb_medium = QRadioButton("Medium")
        self.rb_medium.setChecked(True)
        self.rb_high = QRadioButton("High")

        priority_layout.addWidget(self.rb_low)
        priority_layout.addWidget(self.rb_medium)
        priority_layout.addWidget(self.rb_high)
        main_layout.addLayout(priority_layout)

        additional_layout = QLabel("Additional:")
        main_layout.addWidget(additional_layout)

        add_layout = QHBoxLayout()
        self.cb_important = QCheckBox("Important")
        self.cb_notification = QCheckBox("Notification")
        self.cb_favorite = QCheckBox("Favorite")

        add_layout.addWidget(self.cb_important)
        add_layout.addWidget(self.cb_notification)
        add_layout.addWidget(self.cb_favorite)
        main_layout.addLayout(add_layout)

        task_info_layout = QHBoxLayout()
        self.task_status_layout = QLabel("Status: Ready")
        task_info_layout.addWidget(self.task_status_layout)
        self.task_count_layout = QLabel("Task Count: 0")
        task_info_layout.addWidget(self.task_count_layout)
        main_layout.addLayout(task_info_layout)

        #buttons
        button_layout = QVBoxLayout()
        up_btn_layout = QHBoxLayout()
        down_btn_layout = QHBoxLayout()

        self.submit_btn = QPushButton("Create Task")
        self.submit_btn.clicked.connect(self.generate_task)
        up_btn_layout.addWidget(self.submit_btn)

        self.clear_btn = QPushButton("Clear task")
        self.clear_btn.clicked.connect(self.clear_form)
        down_btn_layout.addWidget(self.clear_btn)

        self.delete_btn = QPushButton("Delete task")
        self.delete_btn.clicked.connect(self.delete_task)
        down_btn_layout.addWidget(self.delete_btn)

        button_layout.addLayout(up_btn_layout)
        button_layout.addLayout(down_btn_layout)
        main_layout.addLayout(button_layout)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["All", "Low", "Medium", "High"])

        self.combo_filter.currentTextChanged.connect(self.render_tasks)
        filter_layout.addWidget(self.combo_filter)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.result_output)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def generate_task(self):
        name_task = self.task_name.text()
        describe_task = self.about_task.toPlainText()
        if self.rb_low.isChecked():
            priority = "Low"
        elif self.rb_medium.isChecked():
            priority = "Medium"
        else:
            priority = "High"

        additional_list = [self.cb_important, self.cb_notification, self.cb_favorite]

        additional_tasks = [add.text() for add in additional_list if add.isChecked()]
        additional_str = ", ".join(additional_tasks) if additional_tasks else "None"

        self.tasks.append({"name": name_task, "description": describe_task, "priority": priority, "additional": additional_str})

        self.task_status_layout.setText("Status: Task created")
        self.task_count_layout.setText(f"Task Count: {len(self.tasks)}")

        self.render_tasks()

    def render_tasks(self):
        current_filter = self.combo_filter.currentText()
        if current_filter == "All":
            filtered = self.tasks
        else:
            filtered = [t for t in self.tasks if t["priority"] == current_filter]

        if not filtered:
            self.result_output.setText("No tasks to display.")
            return

        cards = []
        for t in filtered:
            task = (
                f"Task: {t['name']}\n"
                f"Description: {t['description']}\n"
                f"Priority: {t['priority']}\n"
                f"Additional: {t['additional']}"
            )
            cards.append(task)

        separator = "\n" + "-" * 35 + "\n"
        self.result_output.setText(separator.join(cards))

    def clear_form(self):
        self.task_name.clear()
        self.about_task.clear()
        self.rb_medium.setChecked(True)
        self.cb_important.setChecked(False)
        self.cb_notification.setChecked(False)
        self.cb_favorite.setChecked(False)
        self.task_status_layout.setText("Task Status: Ready")

    def delete_task(self):
        if len(self.tasks) > 0:
            self.tasks.pop()
            self.task_status_layout.setText(f"Status: Task deleted")
        else:
            self.task_status_layout.setText("Status: Nothing to delete")

        self.task_count_layout.setText(f"Task Count: {len(self.tasks)}")
        self.render_tasks()

def main():
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
	main()

