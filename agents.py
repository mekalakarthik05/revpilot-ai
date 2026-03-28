import random

# ================= MEMORY =================
memory_store = []

def store_memory(deal, strategy, outcome):
    memory_store.append({
        "company": deal["company"],
        "strategy": strategy,
        "outcome": outcome
    })

def get_memory():
    return memory_store[-5:]


# ================= PROSPECTING =================
def prospecting_agent():
    leads = [
        {"company": "DataZen", "industry": "AI SaaS"},
        {"company": "CloudNova", "industry": "Cloud"},
        {"company": "FinEdge", "industry": "FinTech"}
    ]

    enriched = []

    for l in leads:

        # 🔥 AI-STYLE SCORING (Industry relevance)
        base_score = 70

        if "AI" in l["industry"]:
            score = base_score + 20   # High priority
        elif "Cloud" in l["industry"]:
            score = base_score + 15
        elif "FinTech" in l["industry"]:
            score = base_score + 10
        else:
            score = base_score
        
        score += random.randint(-5, 5)  # Add some variability

        # 🔥 AI-STYLE PERSONALIZED OUTREACH
        if "AI" in l["industry"]:
            message = f"Hi {l['company']}, we help AI companies scale revenue with intelligent automation."
        elif "Cloud" in l["industry"]:
            message = f"Hi {l['company']}, we optimize cloud sales pipelines to increase conversion."
        elif "FinTech" in l["industry"]:
            message = f"Hi {l['company']}, we help fintech teams reduce churn and improve deal velocity."
        else:
            message = f"Hi {l['company']}, we improve revenue efficiency across your sales pipeline."

        enriched.append({
            "company": l["company"],
            "industry": l["industry"],
            "score": score,
            "outreach": message
        })

    return enriched


# ================= INTELLIGENCE =================
def intelligence_agent(deal):
    score = (
        deal["days_no_reply"] * 5 +
        (1 - deal["engagement_score"]) * 50 +
        (10 if deal.get("competitor") else 0)
    )

    if score >= 70:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {"risk": risk, "score": int(score)}


# ================= PREDICTIVE =================
def predictive_agent(deal):
    churn = min(
        0.9,
        (deal["days_no_reply"] / 15) + (1 - deal["engagement_score"])
    )
    return int(churn * 100)


# ================= COMPETITIVE =================
def competitive_agent(deal):
    if deal.get("competitor"):
        return {
            "battlecard": f"Position ROI advantage vs {deal['competitor']}"
        }
    return None


# ================= EMAIL =================
def email_agent(deal, prediction, strategy, competitive):

    inactivity = deal["days_no_reply"]
    engagement = deal["engagement_score"]
    company = deal["company"]

    opening = (
        f"I noticed we haven’t connected in the last {inactivity} days"
        if inactivity > 7 else
        "Just following up on our recent conversation"
    )

    if prediction > 70:
        risk_line = "our system is detecting a high risk of deal drop-off"
    elif prediction > 40:
        risk_line = "there may be a slowdown in deal progress"
    else:
        risk_line = "things seem to be progressing well"

    engagement_line = ""
    if engagement < 0.3:
        engagement_line = "We also observed lower engagement, which may impact timelines."

    comp_line = ""
    if competitive:
        comp_line = "We understand you're evaluating alternatives and want to ensure best ROI."

    value_line = "Our customers typically improve ROI by 25–30%."

    return f"""
Hi {company} Team,

{opening}, and {risk_line}.

{engagement_line}

{comp_line}

{value_line}

Would you be open to a quick discussion this week?

Best regards,  
Sales Team
""".strip()


# ================= STRATEGY =================
def strategy_agent(deal, intel, prediction, comp):

    options = []

    if prediction > 60:
        options.append(("Urgent Recovery", 0.92))

    if deal["engagement_score"] < 0.3:
        options.append(("ROI Re-engagement", 0.88))

    if comp:
        options.append(("Competitive Positioning", 0.9))

    if not options:
        options.append(("Relationship Nurturing", 0.6))

    best = max(options, key=lambda x: x[1])

    return {
        "name": best[0],
        "confidence": best[1],
        "alternatives": [o[0] for o in options]
    }


# ================= EXECUTION =================
def execution_agent(deal):
    deal["status"] = "Recovery Initiated"
    deal["days_no_reply"] = 0


# ================= ADAPTATION =================
def adaptation_agent(deal):
    if deal["email_opened"] and not deal["replied"]:
        return "Switch to urgency follow-up"
    elif not deal["email_opened"]:
        return "Change subject line"
    return "Maintain strategy"


# ================= METRICS =================
def metrics_agent(deals):
    total = len(deals)
    recovered = len([d for d in deals if d["status"] == "Recovery Initiated"])

    return {
        "conversion": int((recovered / total) * 100) if total else 0,
        "cycle_reduction": random.randint(15, 35)
    }


# ================= COORDINATOR =================
def coordinator_agent(deal):

    intel = intelligence_agent(deal)
    prediction = predictive_agent(deal)
    comp = competitive_agent(deal)

    if intel["risk"] != "LOW":

        strategy = strategy_agent(deal, intel, prediction, comp)
        email = email_agent(deal, prediction, strategy, comp)

        execution_agent(deal)
        adaptation = adaptation_agent(deal)

        store_memory(deal, strategy["name"], "success")

        return {
            "risk": intel["risk"],
            "score": intel["score"],
            "prediction": prediction,
            "strategy": strategy,
            "adaptation": adaptation,
            "competitive": comp,
            "email": email
        }

    return {
        "risk": intel["risk"],
        "score": intel["score"],
        "prediction": prediction
    }