from app.scoring import role_score, industry_score, completeness_score, score_rule_layer

def test_role_scores():
    assert role_score("CEO") == 20
    assert role_score("Growth Manager") == 10
    assert role_score("Intern") == 0

def test_industry_scores():
    ideal = ["B2B SaaS mid-market"]
    assert industry_score("B2B SaaS mid-market", ideal) == 20
    assert industry_score("SaaS", ideal) == 10
    assert industry_score("Finance", ideal) == 0

def test_completeness():
    lead = {"name":"a","role":"b","company":"c","industry":"d","location":"e","linkedin_bio":"f"}
    assert completeness_score(lead) == 10
    lead["location"] = ""
    assert completeness_score(lead) == 0

def test_rule_layer_total():
    offer = {"ideal_use_cases":["B2B SaaS mid-market"]}
    lead = {"name":"x","role":"CEO","company":"y","industry":"B2B SaaS mid-market","location":"z","linkedin_bio":"bio"}
    assert score_rule_layer(lead, offer) == 50
