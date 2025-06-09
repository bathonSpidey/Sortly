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
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.Sortly import Sortly

dotenv.load_dotenv(override=True)
print("Environment variables loaded.")
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY is not set in the environment variables.")
    
QFont("Segoe UI", 22, QFont.Bold)


class SortlyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sortly")
        self.setWindowIcon(QIcon("icons/sortly.png"))
        self.setGeometry(100, 100, 600, 400)

        self.is_dark = False 

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Title row layout with centered title and right-aligned theme button
        title_row = QHBoxLayout()

        # Title label (expand to fill space, centered alignment)
        self.title_label = QLabel("Sortly: Your Folder Organizer Assistant")
        self.title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        

        # Container layout to help keep alignment clean
        title_container = QHBoxLayout()
        title_container.addStretch()
        title_container.addWidget(self.title_label)
        title_container.addStretch()

        # Theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setFont(QFont("Segoe UI Emoji", 16))
        self.theme_button.setObjectName("theme_button")
        self.theme_button.setIcon(QIcon("icons/moon.png"))
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setToolTip("Toggle Dark/Light Theme")

        # Main title row with title in center and button on right
        title_row.addLayout(title_container, stretch=8)
        title_row.addWidget(self.theme_button, alignment=Qt.AlignRight)

        # Add title row to the main layout
        main_layout.addLayout(title_row)
        title_separator = QLabel()
        title_separator.setFixedHeight(1)
        title_separator.setStyleSheet("background-color: #cccccc;" if not self.is_dark else "background-color: #555;")
        main_layout.addWidget(title_separator)
        
        self.api_key_input = os.getenv("OPENAI_API_KEY")
        if not os.getenv("OPENAI_API_KEY"):
            self.api_key_input = QTextEdit()
            self.api_key_input.setPlaceholderText("Enter your API key here...")
            self.api_key_input.setFixedHeight(40)
            main_layout.addWidget(self.api_key_input)

            self.api_key_button = QPushButton("Save API Key")
            self.api_key_button.clicked.connect(self.save_api_key)
            main_layout.addWidget(self.api_key_button, alignment=Qt.AlignCenter)

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
        if self.is_dark:
            self.theme_button.setIcon(QIcon("icons/sun.png"))
        else:
            self.theme_button.setIcon(QIcon("icons/moon.png"))

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
        all_files = os.listdir(self.folder_path)
        chunks = [all_files[i:i + 40] for i in range(0, len(all_files), 40)]

        for idx, chunk in enumerate(chunks, start=1):
            user_message = f"Sort this folder: {self.folder_path} with the contents: {chunk}."
            if user_prompt:
                user_message += f" {user_prompt}"

            message = sortly.sort_folder(user_prompt=user_message)

            if message is None:
                QMessageBox.warning(self, "Error", "Failed to sort files. Please check the API key and try again.")
                return

            title = f"Chunk {idx}" if len(chunks) > 1 else "Done"
            self.show_long_message(title, message)
    def dark_theme(self):
        return """
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QTextEdit {
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444444;
            border-radius: 10px;
            padding: 8px;
        }
        QLabel {
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #3a6ea5;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #558ed5;
        }
        QPushButton#theme_button {
            background-color: transparent;
            font-size: 20px;
            border: none;
            color: #e0e0e0;
        }
        QPushButton#theme_button:hover {
            color: #ffffff;
        }
        QPushButton#theme_button {
            background-color: #444444;
            font-size: 20px;
            border-radius: 6px;
            color: white;
        }
        QPushButton#theme_button:hover {
            background-color: #666666;
        }
        """

    def light_theme(self):
        return """
        QWidget {
            background-color: #f9f9f9;
            color: #202020;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QTextEdit {
            background-color: #ffffff;
            color: #202020;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 8px;
        }
        QLabel {
            color: #202020;
        }
        QPushButton {
            background-color: #3a6ea5;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5b8fd1;
        }
        QPushButton#theme_button {
            background-color: transparent;
            font-size: 20px;
            border: none;
            color: #202020;
        }
        QPushButton#theme_button:hover {
            color: #000000;
        }
        QPushButton#theme_button {
            background-color: #e0e0e0;
            font-size: 20px;
            border-radius: 6px;
            color: #333;
        }
        QPushButton#theme_button:hover {
            background-color: #cfcfcf;
        }
        """



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortlyApp()
    window.show()
    sys.exit(app.exec())
