import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton, QCheckBox, QTextEdit, QPushButton
)


class UserProfileApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Profile")

        main_layout = QVBoxLayout()

        title_label = QLabel("Create your profile")
        main_layout.addWidget(title_label)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        age_layout = QHBoxLayout()
        age_layout.addWidget(QLabel("Age:"))
        self.age_input = QLineEdit()
        age_layout.addWidget(self.age_input)
        main_layout.addLayout(age_layout)

        work_name_layout = QHBoxLayout()
        work_name_layout.addWidget(QLabel("Work Name:"))
        self.work_name_input = QLineEdit()
        work_name_layout.addWidget(self.work_name_input)
        main_layout.addLayout(work_name_layout)

        self.setLayout(main_layout)

        main_layout.addWidget(QLabel("Work format:"))
        format_layout = QHBoxLayout()
        self.office_rb = QRadioButton("Office")
        self.remote_rb = QRadioButton("Remote")
        self.hybrid_rb = QRadioButton("Hybrid")

        format_layout.addWidget(self.office_rb)
        format_layout.addWidget(self.remote_rb)
        format_layout.addWidget(self.hybrid_rb)
        main_layout.addLayout(format_layout)

        self.notify_cb = QCheckBox("Receive notifications")
        main_layout.addWidget(self.notify_cb)

        main_layout.addWidget(QLabel("About:"))
        self.about_input = QTextEdit()
        main_layout.addWidget(self.about_input)

        self.submit_btn = QPushButton("Create profile")
        self.submit_btn.clicked.connect(self.generate_profile)
        main_layout.addWidget(self.submit_btn)

        main_layout.addWidget(QLabel("Result:"))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output)

        self.setLayout(main_layout)

    def generate_profile(self):
        name = self.name_input.text()
        age = self.age_input.text()
        work_name = self.work_name_input.text()
        if self.office_rb.isChecked():
            work_format = "Office"
        elif self.remote_rb.isChecked():
            work_format = "Remote"
        else:
            work_format = "Hybrid"

        notifications = "Yes" if self.notify_cb.isChecked() else "No"

        about = self.about_input.toPlainText()

        self.result_output.setText(f"Name: {name} \nAge: {age} \nWork name: {work_name} \nNotifications: {notifications} \nWork format: {work_format} \n\n About: \n{about}")

app = QApplication(sys.argv)
window = UserProfileApp()
window.show()
sys.exit(app.exec())