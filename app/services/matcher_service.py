from app.services.embedding_service import create_embedding
from app.utils.similarity import similarity


def match_resumes_with_jd(
    jd_embedding,
    resumes,
):
    """
    Compare one JD embedding against multiple resumes.

    resumes format:

    [
        {
            "name": "candidate1.pdf",
            "text": "resume text..."
        },
        ...
    ]
    """

    results = []

    for resume in resumes:

        resume_text = resume["text"]

        if not resume_text.strip():
            continue

        # Embed complete resume
        resume_embedding = create_embedding(
            resume_text
        )

        # Compare JD against resume
        score = similarity(
            jd_embedding,
            resume_embedding,
        )

        results.append({
            "Candidate": resume["name"],
            "Match Score": round(
                score,
                4
            ),
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["Match Score"],
        reverse=True,
    )

    return results