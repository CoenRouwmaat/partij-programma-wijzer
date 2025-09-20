from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[
            "What is the meaning of life?",
            "What is the purpose of existence?",
            "How do I bake a cake?"
        ])

if not result.embeddings:
    raise ValueError("Google API result did not return any embeddings.")

for embedding in result.embeddings:
    print(embedding)
