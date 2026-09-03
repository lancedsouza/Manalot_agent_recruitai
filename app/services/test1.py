from pathlib import Path

folder = Path(
    "/mnt/c/Users/User/Manlot/Annil Raikundlia - Lance/Medline/Sr.Mgr FP&A/test"
)

for file_path in folder.glob("*.pdf"):
    print(file_path)