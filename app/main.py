from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any
import io, csv, json, os
from .models import OfferIn, LeadOut
from .storage import DB
from .scoring import score_rule_layer, completeness_score
from .ai_client import get_ai_intent

app = FastAPI(title="Lead Intent Scoring API")

# ---------- OFFER ----------
@app.post("/offer")
async def create_offer(offer: OfferIn):
    DB.insert_offer(offer)
    return {"message": "Offer saved successfully"}

# ---------- UPLOAD LEADS ----------
@app.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files are allowed")

    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    count = 0
    for row in reader:
        DB.insert_lead(row)
        count += 1
    return {"message": f"{count} leads uploaded successfully"}

# ---------- SCORING ----------
@app.post("/score")
async def score_leads():
    offer = DB.get_latest_offer()
    if not offer:
        raise HTTPException(400, "No offer found. Use /offer first.")

    leads = DB.get_all_leads()
    results = []

    for lead in leads:
        rule_score = score_rule_layer(lead, offer)
        ai_data = await get_ai_intent(offer, lead, rule_score)
        ai_points_map = {"High": 50, "Medium": 30, "Low": 10}
        ai_points = ai_points_map.get(ai_data["intent"], 10)
        total_score = min(rule_score + ai_points, 100)

        DB.update_lead_result(lead["id"], rule_score, ai_points, total_score, ai_data)
        results.append({
            "name": lead["name"],
            "role": lead["role"],
            "company": lead["company"],
            "intent": ai_data["intent"],
            "score": total_score,
            "reasoning": ai_data["explanation"]
        })

    return JSONResponse(results)

# ---------- GET RESULTS ----------
@app.get("/results")
async def get_results():
    leads = DB.get_scored_leads()
    return JSONResponse(leads)

# ---------- EXPORT CSV ----------
@app.get("/export")
async def export_csv():
    leads = DB.get_scored_leads()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=leads[0].keys() if leads else [])
    writer.writeheader()
    writer.writerows(leads)
    output.seek(0)
    return StreamingResponse(
        iter([output.read()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"}
    )

@app.get("/")
def home():
    return {"message": "Lead Scoring API is running. Visit /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
