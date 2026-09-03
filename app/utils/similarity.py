def similarity(jd_embedding, candidate_embedding):

    dot_product = sum(
        x * y
        for x, y in zip(jd_embedding, candidate_embedding)
    )

    magnitude_jd = sum(
        x ** 2 for x in jd_embedding
    ) ** 0.5

    magnitude_candidate = sum(
        y ** 2 for y in candidate_embedding
    ) ** 0.5

    if magnitude_jd == 0 or magnitude_candidate == 0:
        return 0

    return dot_product / (
        magnitude_jd * magnitude_candidate
    )