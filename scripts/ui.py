import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, 
    QPushButton, QCheckBox, QSlider, QDialog, QScrollArea, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np


class DatabaseViewer(QDialog):
    """A specialized window to display the user database with scrolling."""
    def __init__(self, database_content):
        super().__init__()
        self.setWindowTitle("User Database Viewer")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)

        # Scrollable area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Display the database content
        text_edit = QTextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.setText(database_content)
        text_edit.setStyleSheet("""
            background-color: #2b2b2b;
            color: #c9d1d9;
            border: none;
            font: 14px 'Courier New';
        """)
        content_layout.addWidget(text_edit)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)


class CombinedUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified Repository Interface")
        self.setGeometry(100, 100, 800, 600)

        self.data = self.load_data()

        self.selected_users = []  # List of selected users
        self.checkboxes = []  # Store checkboxes here

        self.init_ui()

    def load_data(self):
        """Load the data from the JSON file."""
        try:
            with open('./data/analyzed_db.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def init_ui(self):
        """Initialize the UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # First section: Post count input and scraping button
        post_section_layout = QVBoxLayout()
        self.post_count_label = QLabel("Number of latest posts to scrape:", self)
        post_section_layout.addWidget(self.post_count_label)

        self.post_count_slider = QSlider(Qt.Horizontal, self)
        self.post_count_slider.setRange(1, 100)
        self.post_count_slider.setValue(10)
        self.post_count_slider.valueChanged.connect(self.update_post_count_input)
        post_section_layout.addWidget(self.post_count_slider)

        self.post_count_input = QLineEdit(self)
        self.post_count_input.setPlaceholderText("Enter number of posts (1-100)")
        self.post_count_input.setText(str(self.post_count_slider.value()))
        self.post_count_input.textChanged.connect(self.update_post_count_slider)
        post_section_layout.addWidget(self.post_count_input)

        self.scraping_button = QPushButton("Run Scraping and Processing", self)
        self.scraping_button.clicked.connect(self.run_scraping_and_processing)
        post_section_layout.addWidget(self.scraping_button)

        main_layout.addLayout(post_section_layout)

        # Second section: User filtering and checkboxes for selection
        score_layout = QHBoxLayout()
        self.score_input = QLineEdit(self)
        self.score_input.setPlaceholderText("Enter score threshold (0-100)")
        score_layout.addWidget(self.score_input)

        filter_button = QPushButton("Filter Users", self)
        filter_button.clicked.connect(self.filter_users)
        score_layout.addWidget(filter_button)

        main_layout.addLayout(score_layout)

        # User list display
        self.users_layout = QVBoxLayout()
        self.users_group = QWidget(self)
        self.users_group.setLayout(self.users_layout)
        main_layout.addWidget(self.users_group)

        # Analyze and process button
        analyze_button = QPushButton("Analyze and Process", self)
        analyze_button.clicked.connect(self.analyze_and_process)
        main_layout.addWidget(analyze_button)

        # Visualize data button
        visualize_button = QPushButton("Visualize Data", self)
        visualize_button.clicked.connect(self.visualize_data)
        main_layout.addWidget(visualize_button)

        # View Database Button
        self.view_db_button = QPushButton("View User Database", self)
        self.view_db_button.clicked.connect(self.view_database)
        main_layout.addWidget(self.view_db_button)

    def update_post_count_input(self, value):
        """Update the text input when the slider value changes."""
        self.post_count_input.setText(str(value))

    def update_post_count_slider(self):
        """Update the slider value when the text input changes."""
        try:
            value = int(self.post_count_input.text())
            if 1 <= value <= 100:
                self.post_count_slider.setValue(value)
        except ValueError:
            pass  # Ignore invalid input

    def run_scraping_and_processing(self):
        """Run the scraping and processing scripts sequentially."""
        post_count = self.post_count_slider.value()
        scripts = [
            ('./scripts/reddit_scraper.py', str(post_count)),
        ]

        for script in scripts:
            try:
                result = subprocess.run(['python', script[0], script[1]], capture_output=True, text=True)

                if result.returncode == 0:
                    QMessageBox.information(self, "Success", f"Successfully ran {script[0]}:\n{result.stdout}")
                else:
                    QMessageBox.warning(self, "Error", f"Error running {script[0]}:\n{result.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to run {script[0]}: {str(e)}")

    def filter_users(self):
        """Filter the users based on the score and display checkboxes."""
        for checkbox in self.checkboxes:
            checkbox.setParent(None)  # Remove checkboxes from layout

        threshold = self.score_input.text()

        if not threshold.isdigit() or not (0 <= int(threshold) <= 100):
            print("Please enter a valid score between 0 and 100.")
            return

        threshold = int(threshold)
        filtered_users = {user: score for user, score in self.data.items() if score >= threshold}

        # Add users as checkboxes
        self.checkboxes.clear()  # Reset checkboxes
        self.selected_users.clear()  # Reset selected users

        for user, score in filtered_users.items():
            checkbox = QCheckBox(f"{user} (Score: {score})", self)
            checkbox.setChecked(True)  # Initially check all checkboxes
            checkbox.stateChanged.connect(self.toggle_selection)
            self.checkboxes.append(checkbox)
            self.users_layout.addWidget(checkbox)

    def toggle_selection(self):
        """Handle the selection toggle for sending messages."""
        self.selected_users = []

        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                user = checkbox.text().split(' ')[0]  # Get the username part from the checkbox text
                self.selected_users.append(user)

    def analyze_and_process(self):
        """Run the analysis and processing scripts sequentially."""
        print("Running analysis...")
        subprocess.run(["python", "./scripts/analyze_users.py"], check=True)

        print("Running processing...")
        subprocess.run(["python", "./scripts/processing.py"], check=True)

    def visualize_data(self):
        """Visualize data with a pie chart."""
        values = list(self.data.values())

        # Pie chart
        plt.figure(figsize=(12, 10))
        unique, counts = np.unique(values, return_counts=True)
        plt.pie(counts, labels=[f"Score {score}" for score in unique], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title("Score Distribution (Big Pie Chart)")
        plt.show()

    def view_database(self):
        """Display the user database in a scrollable window."""
        db_path = './data/user_db.json'
        if os.path.exists(db_path):
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    formatted_data = json.dumps(user_data, ensure_ascii=False, indent=4)
                    db_viewer = DatabaseViewer(formatted_data)
                    db_viewer.exec_()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load database: {str(e)}")
        else:
            QMessageBox.warning(self, "File Not Found", f"The database file {db_path} does not exist.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CombinedUI()
    ui.show()
    sys.exit(app.exec_())
