import tkinter as tk
from tkinter import scrolledtext
import spacy
from spacy.matcher import Matcher
from transformers import pipeline
import threading

# --- 1. Load Models (Do this once at the start) ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

print("Loading summarization model (this may take a minute)...")
# Using a specific model version for stability
summarizer = pipeline("summarization", model="t5-small")
print("All models loaded. GUI is ready.")


# --- 2. Define the Core Analysis Function ---
def analyze_text():
    # Clear the output box first
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    
    # Get text from the input box
    legal_text = input_text.get('1.0', tk.END)
    
    if len(legal_text.strip()) < 50:
        output_text.insert(tk.END, "Error: Please paste a legal document.")
        output_text.config(state=tk.DISABLED)
        return

    # Process the text with spaCy
    doc = nlp(legal_text)

    # --- 2a. Information Extraction ---
    parties_found = {}
    clauses_found = []

    # Find Parties (Simpler Method)
    for ent in doc.ents:
        if "Company" not in parties_found and ent.label_ == "ORG":
            if "date" not in ent.text.lower(): 
                parties_found["Company"] = ent.text
        
        if "Consultant" not in parties_found and ent.label_ == "PERSON":
            parties_found["Consultant"] = ent.text

    # Find Clauses (using Matcher)
    matcher = Matcher(nlp.vocab)
    clause_pattern = [
        {"IS_DIGIT": True},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_TITLE": True}
    ]
    matcher.add("CLAUSE_PATTERN", [clause_pattern])
    matches = matcher(doc)

    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "CLAUSE_PATTERN":
            clauses_found.append(doc[start:end].text)

    # --- 2b. Summarization ---
    # Run summarizer in a separate thread to prevent GUI from freezing
    
    output_text.insert(tk.END, "Analyzing... (Summarization may take a moment)\n\n")
    
    def run_summarization():
        try:
            summary = summarizer(legal_text, max_length=150, min_length=40, do_sample=False)
            
            # --- 2c. Display All Results ---
            output_text.config(state=tk.NORMAL)
            
            output_text.insert(tk.END, "--- 1. Extracted Parties ---\n")
            output_text.insert(tk.END, f"  > Company: {parties_found.get('Company', 'Not Found')}\n")
            output_text.insert(tk.END, f"  > Consultant: {parties_found.get('Consultant', 'Not Found')}\n\n")
            
            output_text.insert(tk.END, "--- 2. Key Clauses Found ---\n")
            if clauses_found:
                for clause in clauses_found:
                    output_text.insert(tk.END, f"  > {clause}\n")
            else:
                output_text.insert(tk.END, "No clauses found with the current pattern.\n")
            
            output_text.insert(tk.END, "\n--- 3. Auto-Generated Summary ---\n")
            output_text.insert(tk.END, summary[0]['summary_text'])
            
            output_text.config(state=tk.DISABLED)
            
        except Exception as e:
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"\nAn error occurred during summarization: {e}")
            output_text.config(state=tk.DISABLED)

    # Start the summarization in a new thread
    threading.Thread(target=run_summarization).start()


# --- 3. Set up the GUI Window ---
window = tk.Tk()
window.title("Golden Project: Legal Document Analyzer")
window.geometry("1000x700")

# --- 4. Create GUI Components ---
main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Input Text Area
input_frame = tk.LabelFrame(main_frame, text="Paste Legal Document Here")
input_frame.pack(fill=tk.X, expand=False, side=tk.TOP, pady=5)

input_text = scrolledtext.ScrolledText(input_frame, height=15, wrap=tk.WORD, font=("Arial", 10))
input_text.pack(fill=tk.X, expand=True, padx=5, pady=5)

# Analyze Button
analyze_button = tk.Button(main_frame, text="Analyze Document", command=analyze_text, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
analyze_button.pack(fill=tk.X, expand=False, side=tk.TOP, pady=10)

# Output Text Area
output_frame = tk.LabelFrame(main_frame, text="Analysis Results")
output_frame.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, height=20, wrap=tk.WORD, font=("Arial", 10), state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# --- 5. Start the Application ---
window.mainloop()