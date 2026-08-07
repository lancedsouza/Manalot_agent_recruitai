import instructor
import pdfplumber
from pathlib import Path
from app.models.resume import Resume
from openai import OpenAI
import time
import os

from app.utils.section_extractor import (
    extract_experience_section, 
    extract_education_section,
    extract_summary_section,
    EXPERIENCE_HEADERS, 
    EDUCATION_HEADERS,
    STOP_HEADERS,
    SUMMARY_HEADERS,
    ALL_HEADERS
)

folder_path = Path("/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent")
pdf_files = list(folder_path.glob("*.pdf"))

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ),
    mode=instructor.Mode.JSON,
)

# 1. Store your Golden Ground Truth dataset keyed by candidate name (lowercase for matching)
GROUND_TRUTH_DATA = {
    "anup dubey": [
        "Annual Operating Plan (AOP)", "rolling forecast accuracy", "monthly/quarterly performance reviews", 
        "data-driven decision-making", "financial management", "forecasting", "variance analysis", 
        "pipeline governance", "margin optimization", "revenue recognition (ASC 606 and IFRS 15)", 
        "P&L and BS management", "business process automation", "Data Lake", "Python", "RPA", 
        "AI", "Tableau", "HANA", "HFM", "US GAAP", "audit management"
    ],
    "dhaval kadakia": [
        "strategic budgeting", "forecasting", "financial modelling", "process automation", 
        "Financial Close & Reporting (IFRS)", "balance sheet reconciliations (BlackLine)", 
        "Financial Controls & Compliance (Archer System)", "Finance Transformation", 
        "SAP S/4 HANA enterprise implementation", "Agile coaching", "SG&A variance analysis", 
        "KPI dashboards", "Power BI", "Advanced Excel", "Think-cell", "Archer GRC", "OneStream"
    ],
    "manish thakur": [
        "Strategic FP&A", "Business Finance", "Wealth & Investment Management Finance", 
        "Revenue & Margin Analytics", "Cost Transformation & Optimization", "Investment Governance", 
        "Capital Allocation", "Executive & Board Decision Support", "Finance Transformation", 
        "AI-driven simplification (MS Co-Pilot, Agentic AI)", "Budgeting", "Forecasting", 
        "P&L Analysis", "Financial Modeling", "Project Management", "SAP", "Oracle", 
        "Hyperion", "Power BI", "Six Sigma (DMAIC)"
    ],
    "mahesh mordani": [
        "FP&A", "driver-based planning", "predictive forecasting", "cost allocations", 
        "management reporting", "P&L Preparation", "Reconciliation", "Variance Analysis", 
        "Process Improvement", "Project Management", "Process Standardization", "Financial Controls", 
        "Automation", "M&A transactions", "financial evaluation modeling", "SAP", "Oracle", 
        "PeopleSoft", "HFM", "Essbase", "Anaplan", "OneStream", "Cognos", "Tableau", 
        "Salesforce", "Alteryx", "PowerBI", "Lean/Green Belt (DMAIC)", "RPA"
    ],
    "khushbu palrecha": [
        "Financial Strategy & Planning", "Pricing & Profitability Optimization", "Corporate Compliance", 
        "Management Reporting", "Transformation & Transition Management", "GCC setup", 
        "Financial Planning", "Accounting", "Consolidation and Reporting", "GAAP compliance", 
        "Internal controls", "Working Capital Management", "Billings", "Cost Management", 
        "Budgetary Controls", "Segment Profitability Analysis", "Shareholder Reporting", 
        "IRDA Reporting", "Statutory Audit"
    ]
}


def evaluate_extraction(predicted_items: list, ground_truth_items: list) -> dict:
    """Calculates Precision, Recall, and F1 Score for skills lists."""
    pred_set = set(str(item).strip().lower() for item in predicted_items)
    true_set = set(str(item).strip().lower() for item in ground_truth_items)
    
    tp = len(pred_set.intersection(true_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn
    }


def parse_section_with_usage(section_text: str, section_name: str) -> tuple[Resume, dict]:
    """Sends a section to the LLM and tracks token usage."""
    start = time.time()
    
    response, completion = client.chat.completions.create_with_completion(
        model="qwen2.5:3b",
        response_model=Resume,
        messages=[
            {
                "role": "system",
                "content": f"You are an expert recruiter extracting data for the [{section_name.upper()}] section. Extract only what is present."
            },
            {
                "role": "user",
                "content": f"Extract structured data from this section:\n\n{section_text}"
            }
        ]
    )

    end = time.time()
    duration = end - start
    
    usage = getattr(completion, "usage", None)
    token_stats = {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
        "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
        "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        "duration_seconds": round(duration, 2)
    }

    return response, token_stats


def extract_header_block(full_text: str, line_count: int = 8) -> str:
    lines = full_text.splitlines()
    return "\n".join(lines[:line_count])


def extract_text(file_path: Path) -> str:
    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
    return "\n\n".join(extracted_text)


# --- Execution & Evaluation Loop ---
for file in pdf_files:
    print(f"\n{'='*50}")
    print(f"Processing File: {file.name}")
    print(f"{'='*50}")
    
    full_text = extract_text(file)
    header_block = extract_header_block(full_text)
    
    # Extract sections
    experience_section = extract_experience_section(full_text, EXPERIENCE_HEADERS, ALL_HEADERS)
    experience_context = f"{header_block}\n\n{experience_section}"
    
    # Run LLM extraction
    structured_resume, tokens = parse_section_with_usage(experience_context, "Experience")
    
    # Print Token usage metrics
    print("\n[Token & Latency Metrics]")
    print(f"  - Prompt Tokens:     {tokens['prompt_tokens']}")
    print(f"  - Completion Tokens: {tokens['completion_tokens']}")
    print(f"  - Total Tokens:      {tokens['total_tokens']}")
    print(f"  - Processing Time:   {tokens['duration_seconds']}s")
    
    # Match filename to Ground Truth dictionary dynamically
    matched_candidate = None
    file_lower = file.name.lower()
    for candidate_name in GROUND_TRUTH_DATA.keys():
        if candidate_name in file_lower:
            matched_candidate = candidate_name
            break
            
    if matched_candidate:
        ground_truth_skills = GROUND_TRUTH_DATA[matched_candidate]
        metrics = evaluate_extraction(structured_resume.skills, ground_truth_skills)
        
        print(f"\n[Accuracy Metrics for: {matched_candidate.title()}]")
        print(f"  - Precision: {metrics['precision']}")
        print(f"  - Recall:    {metrics['recall']}")
        print(f"  - F1 Score:  {metrics['f1_score']}")
        print(f"  - Breakdown: TP={metrics['true_positives']}, FP={metrics['false_positives']}, FN={metrics['false_negatives']}")
    else:
        print(f"\n[Warning] No ground truth entry found matching filename: {file.name}. Skipping evaluation metrics.")
        
    print(f"\nExtracted Candidate Name: {structured_resume.name}")
    print(f"Extracted Skills: {structured_resume.skills}")