from fastapi import FastAPI


app = FastAPI(
    title="Manalot RecruitAI",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Manalot RecruitAI API is running"
    }