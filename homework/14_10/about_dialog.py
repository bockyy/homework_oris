from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")

        main_layout = QVBoxLayout()
        title_label = QLabel("Task Manager 2.0")
        about = QLabel("Version 2.0\n"
                        "Author: Akbirov Eldar 11-521\n"
                        "Purpose: application for creating, filtration and saving tasks")
        main_layout.addWidget(title_label)
        main_layout.addWidget(about)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        main_layout.addWidget(self.close_btn)

        self.setLayout(main_layout)