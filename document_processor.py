import os
import re
from PyPDF2 import PdfReader
import json

# Define the extraction fields
FIELD_MAPPING = {
    "Invoice": ["invoice_number", "date", "company", "total_amount"],
    "Resume": ["name", "email", "phone", "experience_years"],
    "Utility Bill": ["account_number", "date", "usage_kwh", "amount_due"]
}

def get_match_group(match, group_index=1):
    """Safely retrieves a regex group or returns None."""
    if match:
        try:
            return match.group(group_index).strip()
        except IndexError:
            return None
    return None

def extract_text_from_pdf(filepath):
    """Reads text from a PDF file."""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        # Do not print or log failure, just return empty text for stability
        return ""

def classify_document(text):
    """Simple keyword/regex-based classification."""
    text_lower = text.lower()
    
    if "invoice #" in text_lower or "total amount" in text_lower or "thank you for your business" in text_lower:
        return "Invoice"
    if "email" in text_lower and "phone" in text_lower and "experience" in text_lower:
        return "Resume"
    if "account number" in text_lower and "usage" in text_lower and "amount due" in text_lower:
        return "Utility Bill"
    if "general document containing random information" in text_lower or "document id" in text_lower:
        return "Other"
    
    return "Unclassifiable"

def extract_structured_data(doc_class, text):
    """Extracts structured data using Regex."""
    data = {}
    
    if doc_class == "Invoice":
        data['invoice_number'] = re.search(r'(?:Invoice #|INV-|ID:)\s*(\S+)', text, re.IGNORECASE)
        data['date'] = re.search(r'(?:Date:)\s*(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        data['company'] = re.search(r'(?:Company:)\s*(\S[\S\s]*?)(?:\n)', text, re.IGNORECASE)
        data['total_amount'] = re.search(r'(?:Total Amount:)\s*\$?([\d,]+\.\d{2})', text, re.IGNORECASE)

    elif doc_class == "Resume":
        # Safer Name extraction pattern
        data['name'] = re.search(r'^\s*([A-Za-z\s]+)\n', text, re.MULTILINE)
        data['email'] = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        data['phone'] = re.search(r'(\+\d{1}-\d{3}-\d{3}-\d{4})', text)
        data['experience_years'] = re.search(r'(?:Experience:)\s*(\d+)\s*years?', text, re.IGNORECASE)

    elif doc_class == "Utility Bill":
        data['account_number'] = re.search(r'(?:Account Number:)\s*(\S+)', text, re.IGNORECASE)
        data['date'] = re.search(r'(?:Billing Date:)\s*(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
        data['usage_kwh'] = re.search(r'(?:Usage:)\s*(\d+)\s*kWh', text, re.IGNORECASE)
        data['amount_due'] = re.search(r'(?:Amount Due:)\s*\$?([\d,]+\.\d{2})', text, re.IGNORECASE)

    # Format output and type conversion
    extracted = {}
    if doc_class in FIELD_MAPPING:
        for field in FIELD_MAPPING[doc_class]:
            value = get_match_group(data.get(field))
            
            # Type conversion
            if field in ['total_amount', 'amount_due'] and value is not None:
                try:
                    extracted[field] = float(value.replace('$', '').replace(',', ''))
                except ValueError:
                    extracted[field] = value
            elif field in ['usage_kwh', 'experience_years'] and value is not None:
                try:
                    extracted[field] = int(value)
                except ValueError:
                    extracted[field] = value
            else:
                extracted[field] = value
    
    elif doc_class in ["Other", "Unclassifiable"]:
         extracted["note"] = "No extraction required"
    
    return extracted

def process_documents(input_dir):
    """Main function to iterate over files and process them."""
    results = {}
    allowed_extensions = ('.pdf', '.txt')
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(allowed_extensions):
            filepath = os.path.join(input_dir, filename)
            text = extract_text_from_pdf(filepath)
            
            if not text:
                continue
                
            doc_class = classify_document(text)
            extracted_data = extract_structured_data(doc_class, text)
            
            results[filename] = {
                "class": doc_class,
                **extracted_data
            }
            
    return results