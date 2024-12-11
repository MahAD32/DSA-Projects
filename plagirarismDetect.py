import sys
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
import string

# Ensure nltk resources are available
for resource in ['punkt', 'stopwords']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

# Preprocessing function

def clean_text(input_text):
    stop_words = set(stopwords.words('english'))
    translator = str.maketrans('', '', string.punctuation)
    input_text = input_text.lower().translate(translator)
    tokenizer = RegexpTokenizer(r'\b\w+\b')
    tokens = tokenizer.tokenize(input_text)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)

# Jaccard Index computation
def calculate_jaccard(text_a, text_b):
    set_a, set_b = set(text_a.split()), set(text_b.split())
    return len(set_a & set_b) / len(set_a | set_b) if set_a | set_b else 0

# Main Application Class
class TextComparator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Similarity Analyzer")
        self.resize(640, 480)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("Load two text files to evaluate their similarity.")
        layout.addWidget(self.info_label)

        self.load_file1_button = QPushButton("Load First File")
        self.load_file1_button.clicked.connect(self.load_first_file)
        layout.addWidget(self.load_file1_button)

        self.load_file2_button = QPushButton("Load Second File")
        self.load_file2_button.clicked.connect(self.load_second_file)
        layout.addWidget(self.load_file2_button)

        self.compare_button = QPushButton("Analyze Similarity")
        self.compare_button.setEnabled(False)
        self.compare_button.clicked.connect(self.analyze_similarity)
        layout.addWidget(self.compare_button)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.first_file_path = None
        self.second_file_path = None

    def load_first_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select First Text File", "", "Text Files (*.txt)")
        if file_path:
            self.first_file_path = file_path
            self.info_label.setText(f"File 1: {os.path.basename(file_path)} loaded.")
            self.toggle_compare_button()

    def load_second_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Second Text File", "", "Text Files (*.txt)")
        if file_path:
            self.second_file_path = file_path
            self.info_label.setText(f"File 2: {os.path.basename(file_path)} loaded.")
            self.toggle_compare_button()

    def toggle_compare_button(self):
        self.compare_button.setEnabled(bool(self.first_file_path and self.second_file_path))

    def analyze_similarity(self):
        if not (self.first_file_path and self.second_file_path):
            self.output_box.setText("Please load both text files before analyzing.")
            return

        with open(self.first_file_path, 'r') as file:
            text_a = clean_text(file.read())
        with open(self.second_file_path, 'r') as file:
            text_b = clean_text(file.read())

        # Cosine Similarity
        vectorizer = CountVectorizer().fit_transform([text_a, text_b])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)[0, 1]

        # Jaccard Similarity
        jaccard_index = calculate_jaccard(text_a, text_b)

        self.output_box.setText(f"Cosine Similarity: {cosine_sim:.4f}\nJaccard Index: {jaccard_index:.4f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TextComparator()
    main_window.show()
    sys.exit(app.exec_())
