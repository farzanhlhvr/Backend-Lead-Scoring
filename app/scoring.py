import json

def role_score(role: str) -> int:
    if not role: return 0
    role = role.lower()
    decision = ["ceo","founder","cto","head of","chief","director","vp","president"]
    influencer = ["manager","lead","senior","growth","marketing","sales"]
    if any(k in role for k in decision): return 20
    if any(k in role for k in influencer): return 10
    return 0

def industry_score(industry: str, ideal: list) -> int:
    if not industry: return 0
    industry = industry.lower()
    ideal = [i.lower() for i in ideal]
    if industry in ideal: return 20
    if any(i in industry or industry in i for i in ideal): return 10
    return 0

def completeness_score(lead: dict) -> int:
    required = ["name","role","company","industry","location","linkedin_bio"]
    return 10 if all(lead.get(r) for r in required) else 0

def score_rule_layer(lead, offer):
    role_pts = role_score(lead["role"])
    ind_pts = industry_score(lead["industry"], offer["ideal_use_cases"])
    comp_pts = completeness_score(lead)
    return role_pts + ind_pts + comp_pts
