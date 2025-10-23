import spacy
from spacy.matcher import Matcher
from transformers import pipeline

# Load the small English spaCy model
nlp = spacy.load("en_core_web_sm")

# --- UPDATED LEGAL TEXT WITH INDIAN CONTEXT ---
legal_text = """
AGREEMENT FOR CONSULTING SERVICES

This Agreement is made and entered into as of October 1, 2025, (the "Effective Date"), by and between Rogue Company Pvt. Ltd., a company registered in India ("Company"), and Prerna, an individual residing in Lucknow, Uttar Pradesh ("Consultant").

WHEREAS, Company desires to engage Consultant to provide certain services in the field of artificial intelligence; and
WHEREAS, Consultant has expertise in this field and desires to provide such services to Company;

NOW, THEREFORE, the parties agree as follows:

1. Services. Consultant shall perform services related to AI strategy and model development (the "Services"). Consultant shall report to the Chief Technology Officer.

2. Term. This Agreement shall commence on the Effective Date and shall continue for a period of six (6) months, unless terminated earlier as provided herein.

3. Compensation. Company shall pay Consultant a fee of ₹12,000 per hour for Services. Consultant shall submit invoices monthly. Payment shall be made within 30 days of receipt of invoice.

4. Confidentiality. Consultant agrees to keep all Company information ("Confidential Information") strictly confidential. Confidential Information includes all proprietary data, trade secrets, and business plans. This obligation shall survive the termination of this Agreement for a period of five (5) years.

5. Termination. Either party may terminate this Agreement upon thirty (30) days written notice to the other party. Company may terminate this Agreement immediately for cause.

6. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Uttar Pradesh, India.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

Company: Rogue Company Pvt. Ltd.
Consultant: Prerna
"""

# Process the text with spaCy
doc = nlp(legal_text)

# --- 1. Named Entity Recognition (NER) ---
print("--- 1. Named Entities (NER) ---")
for ent in doc.ents:
    print(f"  > Entity: {ent.text},  Label: {ent.label_}")


# --- 2. Rule-Based Matches (THIS IS THE CORRECTED SECTION) ---
print("\n--- 2. Rule-Based Matches ---")
parties_found = {}
clauses_found = []

# 1. Find Parties (Simpler Method)
# We loop through all entities. The first ORG and PERSON are likely the parties.
for ent in doc.ents:
    if "Company" not in parties_found and ent.label_ == "ORG":
        # Check to avoid bad matches like "the Effective Date"
        if "date" not in ent.text.lower(): 
            parties_found["Company"] = ent.text
    
    if "Consultant" not in parties_found and ent.label_ == "PERSON":
        parties_found["Consultant"] = ent.text

if parties_found:
    print("\n[+] Found Parties:")
    print(f"  > Company: {parties_found.get('Company')}")
    print(f"  > Consultant: {parties_found.get('Consultant')}")

# 2. Find Clauses (using Matcher)
matcher = Matcher(nlp.vocab)
clause_pattern = [
    {"IS_DIGIT": True},
    {"IS_PUNCT": True, "OP": "?"},
    {"IS_TITLE": True}
]
matcher.add("CLAUSE_PATTERN", [clause_pattern])
matches = matcher(doc)

for match_id, start, end in matches:
    rule_name = nlp.vocab.strings[match_id]
    if rule_name == "CLAUSE_PATTERN":
        clauses_found.append(doc[start:end].text)

if clauses_found:
    print("\n[+] Found Key Clauses:")
    for clause in clauses_found:
        print(f"  > {clause}")
# --- END OF THE CORRECTED SECTION ---


# --- 3. Document Summarization ---
print("\nLoading summarization model (this may take a minute)...")
summarizer = pipeline("summarization", model="t5-small")
print("Summarization model loaded.")

summary = summarizer(legal_text, max_length=100, min_length=30, do_sample=False)

print("\n--- 3. Auto-Generated Summary ---")
print(summary[0]['summary_text'])