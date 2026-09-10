import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

EMOTION_KEYWORDS = {
    "angry": ["angry", "furious", "unacceptable", "terrible", "worst", "complain", "manager"],
    "frustrated": ["frustrated", "annoyed", "again", "still waiting", "how long", "ridiculous"],
    "worried": ["worried", "scared", "nervous", "pain", "hurt", "emergency", "help me"],
    "happy": ["thank", "great", "excellent", "perfect", "amazing", "love", "best"],
}


async def analyze_sentiment(text: str) -> dict:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = await model.generate_content_async(
            f"Analyze the sentiment of this patient message. Return JSON with: "
            f"'score' (float -1 to 1), 'emotion' (string: angry/frustrated/worried/happy/neutral), "
            f"'urgency' (low/medium/high). Message: \"{text}\""
        )
        import json
        result = json.loads(response.text)
        return result
    except Exception:
        text_lower = text.lower()
        for emotion, keywords in EMOTION_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return {"score": -0.5, "emotion": emotion, "urgency": "medium"}
        return {"score": 0, "emotion": "neutral", "urgency": "low"}


async def should_escalate(sentiment: dict) -> bool:
    return sentiment.get("urgency") == "high" or sentiment.get("emotion") in ["angry", "worried"]
