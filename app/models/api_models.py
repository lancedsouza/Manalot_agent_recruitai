from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=""
)

# Try to list models
try:
    models = client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"  - {model.id}")
except Exception as e:
    print(f"Could not list models: {e}")
    print("\nTry these known working models instead:")
    print("  - meta/llama-3.1-70b-instruct")
    print("  - meta/llama-3.1-8b-instruct")
    print("  - mistralai/mistral-large-2-instruct")
    print("  - google/gemma-2-27b-it")