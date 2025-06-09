import sys
import os
import dotenv
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
    QTextEdit,
    QSizePolicy,
    QDialog,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.Sortly import Sortly

dotenv.load_dotenv(override=True)
print("Environment variables loaded.")
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY is not set in the environment variables.")


class SortlyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sortly")
        self.setGeometry(100, 100, 600, 400)

        self.is_dark = False  # Light theme by default

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title row with toggle on right
        title_row = QHBoxLayout()
        self.title_label = QLabel("Sortly: Your Folder Organizer Assistant")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.theme_button = QPushButton("🌙")
        self.theme_button.setObjectName("theme_button")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setToolTip("Toggle Dark/Light Theme")

        title_row.addWidget(self.title_label)
        title_row.addStretch()
        title_row.addWidget(self.theme_button)

        main_layout.addLayout(title_row)
        
        # API Key prompt if not in environment
        self.api_key_input = os.getenv("OPENAI_API_KEY")
        if not os.getenv("OPENAI_API_KEY"):
            self.api_key_input = QTextEdit()
            self.api_key_input.setPlaceholderText("Enter your API key here...")
            self.api_key_input.setFixedHeight(40)
            main_layout.addWidget(self.api_key_input)

            # Button to save API key
            self.api_key_button = QPushButton("Save API Key")
            self.api_key_button.clicked.connect(self.save_api_key)
            main_layout.addWidget(self.api_key_button, alignment=Qt.AlignCenter)

        # Folder label
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setWordWrap(True)
        self.folder_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.folder_label)

        # Select folder button
        self.select_button = QPushButton("Select Folder")
        self.select_button.clicked.connect(self.select_folder)
        main_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)

        # Text box
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Write your prompt here or just use the default one by clicking 'Sort..."
        )
        main_layout.addWidget(self.text_input)

        # Sort button
        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.sort_files)
        main_layout.addWidget(self.sort_button, alignment=Qt.AlignCenter)

        self.folder_path = None
        self.files_content = []

        self.apply_theme()
        
        
        
    def save_api_key(self):
        api_key = self.api_key_input.toPlainText().strip()
        if api_key:
            os.environ["api"] = api_key
            QMessageBox.information(self, "API Key Saved", "API key has been saved temporarily for this session.")
            self.api_key_input.hide()
            self.api_key_button.hide()
        else:
            QMessageBox.warning(self, "Invalid", "Please enter a valid API key.")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        self.theme_button.setText("☀️" if self.is_dark else "🌙")
        self.theme_button.setStyleSheet(
            "background-color: white; color: black;"
            if self.is_dark
            else "background-color: black; color: white;"
        )

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet(self.dark_theme())
        else:
            self.setStyleSheet(self.light_theme())

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.folder_label.setText(f"Selected Folder:\n{folder}")
            
    def show_long_message(self, title, message):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(500, 400)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(message)
        layout.addWidget(text_edit)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec()

    def sort_files(self):
        sortly = Sortly(os.getenv("OPENAI_API_KEY"))
        if not self.folder_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return

        user_prompt = self.text_input.toPlainText()
        user_message = f"Sort this folder: {self.folder_path} with the contents: {os.listdir(self.folder_path)}."
        if user_prompt:
            user_message = f"Sort this folder: {self.folder_path} with the contents: {os.listdir(self.folder_path)}. {user_prompt}"
        message = sortly.sort_folder(user_prompt=user_message)
        if message is None:
            QMessageBox.warning(self, "Error", "Failed to sort files. Please check the API key and try again.")
            return
        self.show_long_message("Done", message)

    def dark_theme(self):
        return """
        QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
            font-family: Arial;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #666;
            border-radius: 5px;
        }
        QLabel {
            color: #f0f0f0;
        }
        QPushButton:not(#theme_button) {
            background-color: #4e9a06;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
        }
        QPushButton:hover:not(#theme_button) {
            background-color: #5cbf0c;
        }
        """

    def light_theme(self):
        return """
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: Arial;
        }
        QTextEdit {
            background-color: #f5f5f5;
            color: black;
            border: 1px solid #999;
            border-radius: 5px;
        }
        QLabel {
            color: #202020;
        }
        QPushButton:not(#theme_button) {
            background-color: #4e9a06;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
        }
        QPushButton:hover:not(#theme_button) {
            background-color: #5cbf0c;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortlyApp()
    window.show()
    sys.exit(app.exec())
