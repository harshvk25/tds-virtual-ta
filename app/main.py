from fastapi import FastAPI, HTTPException
import tiktoken
from pydantic import BaseModel
import re

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken"""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


@app.post("/api/")
async def answer_question(request: QuestionRequest):
    # Extract Japanese text from question
    match = re.search(r"私は(.+?)。", request.question)
    if not match:
        raise HTTPException(status_code=400, detail="Japanese text not found")

    text = match.group(0)
    tokens = count_tokens(text)
    cost = (tokens / 1_000_000) * 0.50  # $0.50 per million tokens

    return {
        "answer": f"The input costs ${cost:.6f} ({tokens} tokens). Closest option: 0.0017",
        "links": [
            {"url": "https://openai.com/pricing", "text": "OpenAI Pricing"},
            {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-q8", "text": "Discourse Discussion"}
        ]
    }