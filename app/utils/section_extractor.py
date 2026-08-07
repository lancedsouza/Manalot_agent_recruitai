import re

SUMMARY_HEADERS = [
    "SUMMARY",
    "PROFILE",
    "PROFESSIONAL SUMMARY",
    "CAREER SUMMARY"
]

EXPERIENCE_HEADERS = [
    "WORK EXPERIENCE",
    "PROFESSIONAL EXPERIENCE",
    "EMPLOYMENT HISTORY",
    "CAREER HISTORY",
    "EXPERIENCE"
]

EDUCATION_HEADERS = [
    "EDUCATION",
    "ACADEMIC BACKGROUND",
    "ACADEMIC QUALIFICATIONS",
    "EDUCATIONAL BACKGROUND",
    "EDUCATIONAL QUALIFICATIONS"
]

STOP_HEADERS = [
    "SKILLS", 
    "PROFESSIONAL SKILLS", 
    "PROJECTS",
    "CERTIFICATIONS",
    "ACHIEVEMENTS", 
    "INTERESTS",
    "LANGUAGES"
]

ALL_HEADERS = (
    SUMMARY_HEADERS
    + EXPERIENCE_HEADERS
    + EDUCATION_HEADERS
    + STOP_HEADERS
)


def extract_experience_section(text: str, exp_headers: list, all_headers: list) -> str:
    """Extracts experience section text from raw resume string."""
    text_lines = text.splitlines()
    start = None
    end = len(text_lines)
    
    exp_set = set(h.upper() for h in exp_headers)
    all_set = set(h.upper() for h in all_headers) 

    for i, line in enumerate(text_lines):
        clean = re.sub(r"[^\w\s]", "", line.strip().upper())
        if not clean:
            continue
            
        if clean in exp_set and start is None:
            start = i + 1  
            continue      
        
        if clean in all_set and start is not None:
            end = i 
            break
            
        if start is not None and end != len(text_lines):
            break
            
    return "\n".join(text_lines[start:end]).strip() if start is not None else ""


def extract_education_section(text: str, edu_headers: list, all_headers: list) -> str:
    """Extracts education section text from raw resume string."""
    text_lines = text.splitlines()
    start = None
    end = len(text_lines)
    
    edu_set = set(h.upper() for h in edu_headers)
    all_set = set(h.upper() for h in all_headers)

    for i, line in enumerate(text_lines):
        clean = re.sub(r"[^\w\s]", "", line.strip().upper())
        if not clean:
            continue
            
        if clean in edu_set and start is None:
            start = i + 1  
            continue
             
        if clean in all_set and start is not None:
            end = i 
            break
            
        if start is not None and end != len(text_lines):
            break
            
    return "\n".join(text_lines[start:end]).strip() if start is not None else ""


def extract_summary_section(text: str, sum_headers: list, all_headers: list) -> str:
    """Extracts summary section text from raw resume string."""
    text_lines = text.splitlines()
    start = None
    end = len(text_lines)
    
    sum_set = set(h.upper() for h in sum_headers)
    all_set = set(h.upper() for h in all_headers)

    for i, line in enumerate(text_lines):
        clean = re.sub(r"[^\w\s]", "", line.strip().upper())
        if not clean:
            continue
            
        if clean in sum_set and start is None:
            start = i + 1  
            continue  # Crucial fix: prevents stopping on the header line itself
            
        if clean in all_set and start is not None:
            end = i 
            break
            
        if start is not None and end != len(text_lines):
            break
            
    return "\n".join(text_lines[start:end]).strip() if start is not None else ""


