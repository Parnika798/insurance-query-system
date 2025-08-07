# parse_policy.py

import os
import re
import uuid
import fitz  # PyMuPDF
import spacy
import pandas as pd
from docx import Document


nlp = spacy.load("en_core_web_sm")



def parse_document(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported format: Use PDF or DOCX")

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

# ------------------- 1.2 Clean and Normalize -------------------

def clean_text(text):
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[’‘]", "'", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ------------------- 1.3 Clause Chunking -------------------

def split_into_clauses(text):
    doc = nlp(text)
    clauses = []
    buffer = ""
    for sent in doc.sents:
        buffer += sent.text.strip() + " "
        if len(buffer.split()) >= 30 or re.search(r"\.\s*$", buffer):
            clauses.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        clauses.append(buffer.strip())
    return clauses

# ------------------- 1.4 Assign Metadata -------------------

def assign_metadata(clauses, policy_name):
    records = []
    for clause in clauses:
        section = extract_section_header(clause)
        records.append({
            "clause_id": f"CL-{uuid.uuid4().hex[:8]}",
            "clause_text": clause,
            "section": section,
            "policy_name": policy_name
        })
    return pd.DataFrame(records)

def extract_section_header(text):
    match = re.match(r"(Section\s+\d+[\.:]?)", text, re.I)
    return match.group(1) if match else "General"

# ------------------- MAIN WRAPPER -------------------

def process_policy_file(file_path, output_json=None):
    policy_name = os.path.basename(file_path)
    raw_text = parse_document(file_path)
    clean = clean_text(raw_text)
    clauses = split_into_clauses(clean)
    df = assign_metadata(clauses, policy_name)
    
    if output_json:
        df.to_json(output_json, orient='records', indent=2)
        print(f"✅ Metadata saved to {output_json}")
    
    return df


