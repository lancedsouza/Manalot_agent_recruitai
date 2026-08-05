import instructor
import pdfplumber
from pathlib import Path
from app.models.resume import Resume
from openai import OpenAI
import time


import os
time.time()


folder_path=Path("/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/Sent")

pdf_files=folder_path.glob("*.pdf")
pdf_file = next(folder_path.glob("*.pdf"))

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ),
    mode=instructor.Mode.JSON,
)
def parse_text_to_pydantic(resume_text: str) -> Resume:
    

    start = time.time()
    # """Takes raw resume text and forces the local LLM to return a validated Resume Pydantic object."""
    # response = client.chat.completions.create(
    #     model="qwen2.5:3b",        # Using your local free model
    #     response_model=Resume,    # Enforces your exact Pydantic schema
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are an expert technical recruiter. Accurately extract candidate information from the resume text into the requested schema fields.",
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Extract the structured data from this resume text:\n\n{resume_text}",
    #         },
    #     ],
    # )
    response = client.chat.completions.create(
    model="qwen2.5:3b",
    response_model=Resume,
   messages=[
    {
        "role": "system",
        "content":
        """
        You are an expert recruiter.

Rules:

1. Skills must be technologies, tools, frameworks,
   business domains or methodologies.

2. Do NOT include:
   - company names
   - job titles
   - certifications

3. Education must contain:
   - degree
   - institution
   - start_date
   - end_date

4. Experience must contain:
   - company
   - title
   - start_date
   - end_date

Return only information present in the resume."""
    },
    {
        "role": "user",
        "content": resume_text
    }
]
)

    print(response)
    end = time.time()
    total_time=end-start
    print(f"time taken by llm {total_time}")

    print(f"LLM took {end-start:.2f} seconds")
    return response

  


def extract_text(file_path:Path):
    start=time.time()
    extracted_text=[]

    path=Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"pdf file not found at {file_path}")
    
    else:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text=page.extract_text()
                if page_text:
                    extracted_text.append(page_text)
        end=time.time()
        total_time=end-start
        print(f"Time taken for extraction {total_time}")
        return "/n/n".join(extracted_text)
            
for file in pdf_files:
    print(f"Raeading pdf...")
    full_text=extract_text(file)
    print(f"Extracted full_text {len(full_text)}")
    # send files parse texr into the required pydantic schema
    print("Sending text to LLm...")
    structured_resume=parse_text_to_pydantic(full_text)
    # Step C: Access fields cleanly like a normal Python object
    print(f"Candidate Name: {structured_resume.name}")
    print(f"Skills Found: {structured_resume.skills}")
    print(f"Experience Years: {structured_resume.experience_years}")
    
    # Or dump the whole thing to a standard Python dictionary
    print(structured_resume.model_dump())





    