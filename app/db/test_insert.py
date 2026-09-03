from pathlib import Path

from app.services.resume_extractor import extract_resume_data


folder_path = Path(
    "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/test"
)


if __name__ == "__main__":

    for pdf_path in folder_path.glob("*.pdf"):

        print(f"\nProcessing: {pdf_path.name}")

        resume_data = extract_resume_data(pdf_path)

        print(resume_data)