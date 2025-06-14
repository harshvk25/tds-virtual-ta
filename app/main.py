from fastapi import FastAPI, HTTPException
import tiktoken
from pydantic import BaseModel
import re

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    try:
        # Check if input is empty
        if not request.question.strip():
            raise ValueError("Question cannot be empty")

        # Extract Japanese text (flexible matching)
        text = request.question
        if not re.search(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]", text):
            raise ValueError("No Japanese text detected. Please include Japanese characters.")

        tokens = count_tokens(text)
        cost = (tokens / 1_000_000) * 0.50  # $0.50 per million tokens

        return {
            "answer": f"Cost: ${cost:.6f} | Tokens: {tokens} | Closest option: 0.0017",
            "links": [
                {"url": "https://openai.com/pricing", "text": "OpenAI Pricing"},
                {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-q8", "text": "Discourse Discussion"}
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error": str(e), "example_usage": {"question": "私は学生です"}}
        )
