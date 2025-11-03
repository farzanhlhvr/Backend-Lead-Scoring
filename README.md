# 🧠 Lead Intent Scoring Backend

A backend service that scores B2B leads (High / Medium / Low) by combining **rule-based logic** and **AI reasoning**.

---

## 🚀 Features
- `POST /offer` — submit offer details  
- `POST /leads/upload` — upload leads via CSV  
- `POST /score` — compute intent scores  
- `GET /results` — view JSON results  
- `GET /export` — download results as CSV  

---

## 🧩 Example Offer JSON
```json
{
  "name": "AI Outreach Automation",
  "value_props": ["24/7 outreach", "6x more meetings"],
  "ideal_use_cases": ["B2B SaaS mid-market"]
}
