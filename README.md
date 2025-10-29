# Legal Document Analyzer (AI Internship Golden Project)

This is a "Golden Project" submitted for the **CodeClause Artificial Intelligence Internship**.

This application is an AI-powered tool that analyzes legal documents to extract key information and provide a quick, easy-to-read summary. It's built to help users understand complex legal contracts at a glance.

---

## ✨ Key Features

* **Key Information Extraction:** Automatically identifies and extracts crucial details from the contract, such as:
    * The primary **Parties** involved (e.g., Company, Consultant)
    * A list of all major **Key Clauses** (e.g., "Confidentiality", "Termination")

* **Automatic Summarization:** Uses a pre-trained **Hugging Face Transformer model (T5-small)** to read the entire document and generate a concise, high-quality summary.

* **Simple User Interface:** A clean and user-friendly GUI built with **Tkinter** where you can paste any legal text and get an instant analysis.

---

## 🛠️ Technologies Used

* **Python:** The core programming language.
* **spaCy:** For high-performance NLP, Named Entity Recognition (NER), and rule-based matching to find clauses and parties.
* **Hugging Face `transformers`:** For state-of-the-art text summarization.
* **`tf-keras` / `PyTorch`:** As the backend framework for the Transformer model.
* **Tkinter:** For the cross-platform desktop GUI.

---

## 🚀 How to Run This Project

Follow these steps to set up and run the application on your local machine.

**1. Clone the Repository:**
```bash
git clone [https://github.com/YourUsername/CodeClause-Golden-Legal-Analyzer.git](https://github.com/YourUsername/CodeClause-Golden-Legal-Analyzer.git)
cd CodeClause-Golden-Legal-Analyzer
2. Create and Activate a Virtual Environment: This is a crucial step to avoid conflicts with other projects.

For Windows:

Bash

python -m venv .venv
.\.venv\Scripts\activate
For macOS/Linux:

Bash

python3 -m venv .venv
source .venv/bin/activate
3. Install Required Packages: The requirements.txt file (which you should have created) installs all dependencies automatically.

Bash

pip install -r requirements.txt
4. Download the spaCy Model: The application requires spaCy's small English model.

Bash

python -m spacy download en_core_web_sm
5. Run the Application: Once everything is installed, you can start the GUI.

Bash

python legal_gui.py
(Note: The first time you run it, it may take 30-60 seconds to download and cache the summarization model. This is a one-time process.)