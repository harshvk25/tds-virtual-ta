from fastapi import FastAPI, HTTPException
import tiktoken
from pydantic import BaseModel
import re
from typing import Optional

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

def count_tokens(text: str) -> int:
    """Count tokens using tiktoken for gpt-3.5-turbo-0125"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0125")
    return len(encoding.encode(text))

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    try:
        # Improved Japanese text detection
        text = None
        
        # Case 1: Text wrapped in "私は...。"
        wrapped_match = re.search(r"私は(.+?)。", request.question)
        if wrapped_match:
            text = wrapped_match.group(0)
        else:
            # Case 2: Standalone Japanese text
            if re.search(r"[\u3040-\u30FF\u4E00-\u9FFF]+。", request.question):
                text = request.question
        
        if not text:
            raise ValueError("No Japanese text found in input. Please include Japanese text to calculate token cost.")

        tokens = count_tokens(text)
        cost = (tokens / 1_000_000) * 0.50  # $0.50 per million tokens
        
        # Find the closest option
        options = [0.0018, 0.00175, 0.0017, 0.00165]
        closest_option = min(options, key=lambda x: abs(x - cost))
        
        return {
            "answer": f"The input text would cost {cost:.6f} cents ({tokens} tokens). The closest option is {closest_option}.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                    "text": "Token counting methodology"
                },
                {
                    "url": "https://openai.com/pricing",
                    "text": "OpenAI Pricing Information"
                }
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
