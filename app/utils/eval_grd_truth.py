from functools import lru_cache
from app.services.resume_extractor import extract_resume_data
from pathlib import Path
import logging 
import sys
import platform
from app.utils.ground_truth import GROUND_TRUTH_DATA,ground_truth_skills

print(sys.executable)
print(platform.system())

pdf_path = Path(
    "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/test/Manalot_Anup_Dubey.pdf"
)
print("PDF path:", pdf_path)
print("Exists:", pdf_path.exists())
logger=logging.getLogger(__name__)
print('logger')
@lru_cache(maxsize=32)
def cached_extract_resume_skills(file_path: Path):
    print("Executing fresh extraction (Cache Miss)...")
    # Pass file_path directly without str() conversion
    resume_data = extract_resume_data(file_path)
    logger.info(resume_data)
    
    if isinstance(resume_data, dict):
        return resume_data.get("skills", [])
    return getattr(resume_data, "skills", [])

skills_first_call = cached_extract_resume_skills(pdf_path)
print("Skills:", skills_first_call)

predicted_skills = [
    'Annual Operating Plan (AOP)',
    'rolling forecast',
    'financial management',
    'forecasting',
    'variance analysis',
    'pipeline governance',
    'automation',
    'financial system integration',
    'financialoperations',
    'budget adherence',
    'resource allocation',
    'WIP reviews',
    'GAAP',
    'US GAAP',
    'PWC audit',
    'RTR',
    'BS Flux',
    'KPI',
    'Data Lake',
    'Python',
    'RPA',
    'AI',
    'BOT',
    'Tableau',
    'HANA',
    'HFM',
    'Revenue accounting',
    'invoicing',
    'receivable management',
    'working capital management',
    'audit documentation',
    'FX impact',
    'pyramid planning',
    'due diligence',
    'reconciliation',
    'financial projections'
]
# Skills: ['Annual Operating Plan (AOP)', 'rolling forecast', 'financial management', 'forecasting', 'variance analysis', 'pipeline governance', 'automation', 'financial system integration', 'financial operations', 'budget adherence', 'resource allocation', 'WIP reviews', 'GAAP', 'US GAAP', 'PWC audit', 'RTR', 'BS Flux', 'KPI', 'Data Lake', 'Python', 'RPA', 'AI', 'BOT', 'Tableau', 'HANA', 'HFM', 'Revenue accounting', 'invoicing', 'receivable management', 'working capital management', 'audit documentation', 'FX impact', 'pyramid planning', 'due diligence', 'reconciliation', 'financial projections']


def normalize_data(ground_truth,predictedtruth):
    ground_truth={skill.strip().lower() for skill in ground_truth}
    predictedtruth={skill.strip().lower() for skill in predictedtruth}  

    return ground_truth,predictedtruth


def evaluate_skills(ground_truth, predicted_skills):
        ground_truth, predicted_skills = normalize_data(ground_truth, predicted_skills)

        true_positives = len(set(ground_truth) & set(predicted_skills))
        false_positives = len(set(predicted_skills) - set(ground_truth))
        false_negatives = len(set(ground_truth) - set(predicted_skills))

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives
        }

normalized_ground_truth, normalized_predicted_skills = normalize_data(ground_truth_skills, predicted_skills)
evaluation_results = evaluate_skills(normalized_ground_truth, normalized_predicted_skills)
print("Evaluation Results:", evaluation_results)