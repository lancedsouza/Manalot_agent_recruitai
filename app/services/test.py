from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
    timeout=30.0,
    max_retries=0,
)

start = time.perf_counter()

print("Calling NVIDIA...")

response = client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    messages=[
        {
            "role": "user",
            "content": "Reply with only: hello"
        }
    ],
    temperature=0,
)

print(
    f"Returned in "
    f"{time.perf_counter() - start:.2f}s"
)

print(
    response.choices[0].message.content
)