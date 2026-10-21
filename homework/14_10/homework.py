import sys, os
import json
from about_dialog import AboutDialog
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QComboBox,
    QMessageBox,
    QListWidget
)

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_from_json()

        main_layout = QVBoxLayout()

        self.setWindowTitle("Task Manager")

        task_layout = QHBoxLayout()
        task_layout.addWidget(QLabel("Task:"))

        self.task_label = QLabel("Название: 0 символов")
        task_layout.addWidget(self.task_label)
        self.task_name = QLineEdit()
        self.task_name.textChanged.connect(self.update_char_count)

        task_layout.addWidget(self.task_name)
        main_layout.addLayout(task_layout)

        self.about_task = QTextEdit()
        main_layout.addWidget(QLabel("Description:"))
        main_layout.addWidget(self.about_task)

        name_priority_layout = QHBoxLayout()
        name_priority_layout.addWidget(QLabel("Priority:"))
        self.combo_priority_filter = QComboBox()
        self.combo_priority_filter.addItems(["Low", "Medium", "High"])
        name_priority_layout.addWidget(self.combo_priority_filter)
        main_layout.addLayout(name_priority_layout)

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

        self.clear_all_btn = QPushButton("clear all")
        self.clear_all_btn.clicked.connect(self.clear_tasks)
        down_btn_layout.addWidget(self.clear_all_btn)

        self.clear_btn = QPushButton("Clear task")
        self.clear_btn.clicked.connect(self.clear_form)
        down_btn_layout.addWidget(self.clear_btn)

        self.edit_btn = QPushButton("Save Edit")
        self.edit_btn.clicked.connect(self.edit_task)
        down_btn_layout.addWidget(self.edit_btn)

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
        main_layout.addLayout(filter_layout)


        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.fill_form_for_edit)
        main_layout.addWidget(self.task_list)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        more_info_layout = QVBoxLayout()
        self.about_btn = QPushButton("About")
        self.about_btn.setObjectName("aboutButton")
        self.about_btn.clicked.connect(self.depict_window)
        more_info_layout.addWidget(self.about_btn)
        main_layout.addLayout(more_info_layout)

        #css
        self.setStyleSheet("""
        QLineEdit {
            background-color: rgb(113, 144, 145);        
            color: white;
        }
        QPushButton {
            background-color: rgb(59, 145, 42);
            color: white;
        }
        
        QPushButton#aboutButton {
            background-color: #555555;
            color: white;
            border-radius: 4px;
            padding: 4px;
        }
        """)

        self.load_from_json()
        self.render_tasks()
        self.task_count_layout.setText(f"Задач: {len(self.tasks)}")

        self.current_editing_id = None


    def generate_task(self):
        name_task = self.task_name.text().strip()

        if not name_task:
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")
            return

        describe_task = self.about_task.toPlainText().strip()

        priority = self.combo_priority_filter.currentText()

        additional_list = [self.cb_important, self.cb_notification, self.cb_favorite]
        active_flags = [cb.text() for cb in additional_list if cb.isChecked()]

        new_id = max([t["id"] for t in self.tasks], default=0) + 1

        self.tasks.append({
            "id": new_id,
            "name": name_task,
            "description": describe_task,
            "priority": priority,
            "additional": active_flags
        })

        self.task_name.clear()
        self.about_task.clear()
        for cb in additional_list:
            cb.setChecked(False)

        self.render_tasks()

        self.task_status_layout.setText("Status: Задача добавлена")
        self.task_count_layout.setText(f"Задач: {len(self.tasks)}")
        self.save_to_json()

    def render_tasks(self):
        current_filter = self.combo_filter.currentText()

        if current_filter == "All":
            self.current_display_tasks = self.tasks
        else:
            self.current_display_tasks = [t for t in self.tasks if t["priority"] == current_filter]

        self.task_list.clear()

        for t in self.current_display_tasks:
            additionals = t["additional"]
            desc = f": {t['description']}, additions: " if t['description'] else ""
            item_text = f"[{t['priority']}] {t['name']}{desc}{additionals if additionals else []}"
            self.task_list.addItem(item_text)

    def clear_form(self):
        self.task_name.clear()
        self.about_task.clear()
        self.cb_important.setChecked(False)
        self.cb_notification.setChecked(False)
        self.cb_favorite.setChecked(False)
        self.task_status_layout.setText("Task Status: Ready")

    def clear_tasks(self):
        reply = QMessageBox.question(
            self,
            "are you sure?",
            "delete all tasks?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.task_list.clear()
            self.tasks.clear()
            self.render_tasks()
            self.task_status_layout.setText("Status: Список очищен")
            self.task_count_layout.setText(f"Задач: 0")

            self.save_to_json()

    def update_char_count(self, text):
        self.task_label.setText(f"Название: {len(text)} символов")

    def delete_task(self):
        row = self.task_list.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "You not select a task!")
            return

        reply = QMessageBox.question(
            self,
            "Delete Task?",
            "delete selected task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.tasks:
                task_to_delete = self.current_display_tasks[row]
                self.tasks.remove(task_to_delete)
                self.task_status_layout.setText("Status: Task deleted")
            else:
                self.task_status_layout.setText("Status: Nothing to delete")

        self.save_to_json()
        self.render_tasks()
        self.task_count_layout.setText(f"Task Count: {len(self.tasks)}")
        self.clear_form()

    def fill_form_for_edit(self, item=None):
        row = self.task_list.currentRow()

        if row == -1:
            return

        task = self.current_display_tasks[row]

        self.task_name.setText(task["name"])
        self.about_task.setPlainText(task["description"])
        self.combo_priority_filter.setCurrentText(task["priority"])
        self.cb_important.setChecked("Important" in task["additional"])
        self.cb_notification.setChecked("Notification" in task["additional"])
        self.cb_favorite.setChecked("Favorite" in task["additional"])

        self.current_editing_id = task["id"]

    def edit_task(self):
        if self.current_editing_id is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите задачу для редактирования!")
            return

        for task in self.tasks:
            if task["id"] == self.current_editing_id:
                task["name"] = self.task_name.text().strip()
                task["description"] = self.about_task.toPlainText().strip()
                task["priority"] = self.combo_priority_filter.currentText()

                additional_list = [self.cb_important, self.cb_notification, self.cb_favorite]
                task["additional"] = [cb.text() for cb in additional_list if cb.isChecked()]

                self.task_status_layout.setText("Status: Task edited")
                break

        self.current_editing_id = None

        self.save_to_json()
        self.render_tasks()
        self.clear_form()

    def depict_window(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def save_to_json(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []


def main():
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

