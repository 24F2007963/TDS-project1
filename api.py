import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import requests

app = FastAPI()


# app.mount("/", StaticFiles(directory="public", html=True), name="static")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("OPENAI_API_KEY is:", os.getenv("OPENAI_API_KEY"))

# Load the cleaned content JSON (already preprocessed)
with open("cleaned_content.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Use your proxy here
API_URL = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise Exception("OPENAI_API_KEY environment variable is'nt't set")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "")

    # Prepare context from the documents (just concatenated text)
    context_chunks = [doc["content"] for doc in documents if "content" in doc]
    context = "\n\n".join(context_chunks[:5])  # limit to avoid token overflow

    prompt = (
        "You are a helpful teaching assistant for the IITM Tools in Data Science course. "
        "Based only on the context provided below, answer the student's question. "
        "If relevant, include any matching links with titles. "
        "Return the response as a JSON object with 'answer' and 'links' (url and text).\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Respond only in this JSON format:\n"
        "{\n"
        "  \"answer\": \"...\",\n"
        "  \"links\": [\n"
        "    {\"url\": \"...\", \"text\": \"...\"}\n"
        "  ]\n"
        "}"
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful IITM TA."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        answer_text = response.json()["choices"][0]["message"]["content"]
        # Parse to JSON in case it's returned as string
        try:
            parsed = json.loads(answer_text)
            return parsed
        except json.JSONDecodeError:
            return {
                "answer": answer_text.strip(),
                "links": []
            }
    except Exception as e:
        return {
            "answer": f"Error occurred: {e}",
            "links": []
        }
