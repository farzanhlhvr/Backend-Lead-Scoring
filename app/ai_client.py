import os, httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def build_prompt(offer, lead):
    return f"""
Offer:
Name: {offer['name']}
Value props: {', '.join(offer['value_props'])}
Ideal use cases: {', '.join(offer['ideal_use_cases'])}

Lead:
Name: {lead['name']}
Role: {lead['role']}
Company: {lead['company']}
Industry: {lead['industry']}
Location: {lead['location']}
LinkedIn Bio: {lead.get('linkedin_bio', '')}

Task:
Classify buying intent as High / Medium / Low and explain in 1–2 sentences.
Format strictly as:
Intent: <High|Medium|Low>
Explanation: <your short explanation>
"""

async def get_ai_intent(offer, lead, rule_score: int):
    if not OPENAI_API_KEY:
        # Fallback deterministic if key not provided
        if rule_score >= 40:
            return {"intent":"High","explanation":"Strong role & industry fit (fallback)"}
        elif rule_score >= 25:
            return {"intent":"Medium","explanation":"Moderate fit (fallback)"}
        else:
            return {"intent":"Low","explanation":"Weak match (fallback)"}

    prompt = build_prompt(offer, lead)
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an assistant classifying buying intent."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0
            },
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"].strip()

    intent = "Low"
    if "high" in text.lower(): intent = "High"
    elif "medium" in text.lower(): intent = "Medium"
    explanation = text.split("Explanation:",1)[-1].strip() if "Explanation:" in text else text
    return {"intent": intent, "explanation": explanation}
