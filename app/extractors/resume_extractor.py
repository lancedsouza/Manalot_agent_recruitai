from app.context.context_engineer import extract_context    
from app.utils.pdf_reader import parse_text_to_pydantic
from pathlib import Path


folder_path=Path("/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent")

pdf_files=folder_path.glob("*.pdf")
pdf_file = next(folder_path.glob("*.pdf"))


for file in pdf_files:
    print(f"Reading pdf...")
    context=extract_context(file)
    print(f"Extracted full_text {len(context)}")
    # send files parse texr into the required pydantic schema
    print("Sending text to LLm...")
    structured_resume=parse_text_to_pydantic(context)
    # Step C: Access fields cleanly like a normal Python object
    print(f"Candidate Name: {structured_resume.name}")
    print(f"Skills Found: {structured_resume.skills}")
    print(f"Experience Years: {structured_resume.experience_years}")
    
    # Or dump the whole thing to a standard Python dictionary
    print(structured_resume.model_dump())
