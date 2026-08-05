from app.utils.pdf_reader import extract_text
import re
from pathlib import Path
folder_path=Path("/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent")

pdf_files=folder_path.glob("*.pdf")
pdf_file = next(folder_path.glob("*.pdf"))

def remove_email(text):
    text=re.sub(r"(\S+@\S+)","",text)
    return text

def remove_phone(text):
    text=re.sub(r"(\+?\d+)","",text)
    return text

def remove_urls(text):
    text=re.sub(r"(\https?://\S+|www\.\S+),"",text")
    return text

def remove_page_nos(text:str)->str:
    text=re.sub(r"Page \d+ of \d+"),"",text,flags=re.IGNORECASE")
    return text

def normalize_whitesapce(text):
    text=re.sub(r"\n\s*\n+")
    return text


def extract_context()->str:
    full_text=extract_text(pdf_file)
     
    text=remove_email(full_text)
    text=remove_urls(text)
    text=remove_phone(text)
    text=remove_page_nos(text)
    text=normalize_whitesapce(text)
    return text
        
