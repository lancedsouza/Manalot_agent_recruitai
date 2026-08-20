import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.candidate_benchmark import CandidateBenchmarkProfile
from app.models.peer_group import PeerGroup


# ============================================================
# CONFIG
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        f"GEMINI_API_KEY not found in {ENV_PATH}"
    )

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# IDENTIFY PEER GROUP
# ============================================================

def identify_peer_group(
    profile: CandidateBenchmarkProfile,
) -> PeerGroup:

    prompt = f"""
You are defining the appropriate professional peer group
for benchmarking a candidate.

Candidate profile:

Name:
{profile.name}

Function:
{profile.function}

Current designation:
{profile.designation}

Total experience:
{profile.experience_years} years

Industry:
{profile.industry}

Geography:
{profile.geography}

Team size:
{profile.team_size}

Markets handled:
{profile.markets}

Portfolio handled:
{profile.portfolio_handled}

IMPORTANT RULES:

1. The peer group should primarily be based on:
   - professional function
   - approximate years of experience
   - geography
   - relevant/comparable industries

2. Do NOT restrict the peer group only to the candidate's
   current designation.

Example:
A Manager with 15 years of experience should still be
compared against other professionals with roughly
15 years of experience in the same function.

3. Designation will be evaluated later as a career
progression signal.

4. Choose a reasonable experience range around the
candidate's actual experience.

5. Include industries that are genuinely comparable,
not every industry.

6. Do not evaluate or rank the candidate yet.

Your only job is to define the appropriate peer group.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=PeerGroup,
        ),
    )

    return PeerGroup.model_validate_json(
        response.text
    )