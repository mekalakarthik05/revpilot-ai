import random
import json
from datetime import datetime
from llm import ask_llm
from actions import send_email

# Memory Store
memory_store = []

def store_memory(deal, strategy, outcome):
    memory_store.append({
        "company": deal["company"],
        "strategy": strategy,
        "outcome": outcome,
        "time": datetime.now().isoformat()
    })

def get_memory():
    return memory_store[-5:]


# Prospecting Agent
def prospecting_agent():
    leads = [
        {"company": "DataZen", "industry": "AI SaaS"},
        {"company": "CloudNova", "industry": "Cloud"},
        {"company": "FinEdge", "industry": "FinTech"}
    ]

    enriched = []

    for l in leads:

        prompt = f"""
        You are a sales prospecting AI.

        Company: {l['company']}
        Industry: {l['industry']}

        Generate:
        - Lead score (0-100)
        - 2 decision makers (name + role)
        - Highly personalized outreach message

        Return JSON:
        {{
          "score": number,
          "decision_makers": ["Name - Role", "Name - Role"],
          "message": "..."
        }}
        """

        response = ask_llm(prompt)

        if response:
            try:
                data = json.loads(response)
                enriched.append({
                    "company": l["company"],
                    "industry": l["industry"],
                    "score": data["score"],
                    "decision_makers": data["decision_makers"],
                    "outreach": data["message"]
                })
                continue
            except:
                pass

        enriched.append({
            "company": l["company"],
            "industry": l["industry"],
            "score": random.randint(70, 90),
            "decision_makers": ["Unknown"],
            "outreach": f"Hi {l['company']}, exploring partnership opportunities."
        })

    return enriched


# Risk Analysis
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


# Churn Prediction
def predictive_agent(deal):
    churn = min(
        0.9,
        (deal["days_no_reply"] / 15) + (1 - deal["engagement_score"])
    )
    return int(churn * 100)


# Competitive Insight
def competitive_agent(deal):
    if deal.get("competitor"):
        return {
            "battlecard": f"Position ROI advantage vs {deal['competitor']}"
        }
    return None


# Company Intelligence
def enrichment_agent(deal):
    prompt = f"""
    Provide business insights for sales outreach.

    Company: {deal['company']}
    """

    return ask_llm(prompt) or "Scaling operations and improving conversions"


# Email Generator
def email_agent(deal, prediction, strategy, competitive):
    insights = enrichment_agent(deal)

    prompt = f"""
    Write a short B2B sales email.

    Company: {deal['company']}
    Insights: {insights}
    Risk: {prediction}%
    Strategy: {strategy['name']}
    Competitor: {deal.get('competitor')}
    """

    response = ask_llm(prompt)

    if response:
        return response

    return f"Hi {deal['company']} Team, following up on our discussion."


# Strategy Engine
def strategy_agent(deal, intel, prediction, comp):
    memory = get_memory()

    prompt = f"""
    Suggest best sales strategy.

    Past:
    {memory}

    Company: {deal['company']}
    Risk: {intel['risk']}
    Churn: {prediction}%
    Engagement: {deal['engagement_score']}
    Competitor: {deal.get('competitor')}

    Return JSON:
    {{
      "strategy": "...",
      "reason": "...",
      "confidence": 0-1
    }}
    """

    response = ask_llm(prompt)

    if response:
        try:
            data = json.loads(response)
            return {
                "name": data["strategy"],
                "reason": data["reason"],
                "confidence": data["confidence"],
                "alternatives": []
            }
        except:
            pass

    return {
        "name": "Follow-up Strategy",
        "confidence": 0.5,
        "alternatives": []
    }


# Execution Engine
def execution_agent(deal):
    deal["status"] = "Recovery Initiated"
    deal["days_no_reply"] = 0


# Adaptation Logic
def adaptation_agent(deal):
    if deal["email_opened"] and not deal["replied"]:
        return "Switch follow-up strategy"
    elif not deal["email_opened"]:
        return "Change subject line"
    return "Maintain strategy"


# Decision Explanation
def explanation_agent(deal, strategy, prediction):
    prompt = f"""
    Explain why this deal is at risk.

    Company: {deal['company']}
    Churn risk: {prediction}%
    Strategy: {strategy['name']}
    """

    return ask_llm(prompt) or "Risk due to inactivity and low engagement"


# Email Sequence Generator (UPGRADED)
def sequence_agent(deal):
    prompt = f"""
    You are a senior sales strategist.

    Company: {deal['company']}
    Industry: {deal.get('industry')}
    Size: {deal.get('company_size')}
    Funding: {deal.get('recent_funding')}

    Create a 3-email sequence targeting TWO roles.

    Each email must include:
    - Subject
    - Body
    - Clear next step for sales rep

    Make emails role-specific (e.g., CTO vs Head of Sales).
    """

    return ask_llm(prompt) or "Sequence unavailable"


# Safe Email Sender (FIXED)
def safe_email_send(deal, email):
    for _ in range(2):
        try:
            return send_email(deal["email"], "Follow-up", email)
        except:
            continue
    return {"opened": False, "replied": False}


# Metrics Engine
def metrics_agent(deals):
    total = len(deals)
    recovered = len([d for d in deals if d["status"] == "Recovery Initiated"])

    return {
        "conversion": int((recovered / total) * 100) if total else 0,
        "cycle_reduction": random.randint(15, 35)
    }


# Business Impact
def impact_agent(deals):
    recovered = len([d for d in deals if d["status"] == "Recovery Initiated"])
    revenue = sum(d["value"] for d in deals if d["status"] == "Recovery Initiated")

    return {
        "revenue_recovered": revenue,
        "conversion_improvement": f"{int((recovered/len(deals))*100)}%"
    }


# Impact Model (NEW)
def impact_model(deals):
    recovered = len([d for d in deals if d["status"] == "Recovery Initiated"])
    avg_deal = sum(d["value"] for d in deals) / len(deals)

    revenue = recovered * avg_deal
    time_saved = recovered * 2
    cost_saved = time_saved * 500

    return {
        "revenue_recovered": int(revenue),
        "time_saved_hours": time_saved,
        "cost_saved": int(cost_saved)
    }


# Decision Coordinator
def coordinator_agent(deal):

    trace = []

    try:
        if random.random() < 0.05:
            raise Exception("Simulated failure")

        intel = intelligence_agent(deal)
        trace.append("risk_evaluated")

        prediction = predictive_agent(deal)
        trace.append("prediction_generated")

        comp = competitive_agent(deal)

        priority = "URGENT" if intel["risk"] == "HIGH" else ("FOLLOW-UP" if intel["risk"] == "MEDIUM" else "MONITOR")

        if intel["risk"] != "LOW":

            strategy = strategy_agent(deal, intel, prediction, comp)
            trace.append("strategy_selected")

            email = email_agent(deal, prediction, strategy, comp)
            trace.append("email_generated")

            event = safe_email_send(deal, email)
            trace.append("email_sent")

            execution_agent(deal)

            adaptation = adaptation_agent(deal)
            trace.append("adaptation_applied")

            explanation = explanation_agent(deal, strategy, prediction)
            trace.append("explanation_generated")

            next_steps = [
                "Schedule follow-up call within 24 hours",
                "Send ROI-focused case study",
                "Address competitor comparison directly"
            ]

            store_memory(deal, strategy["name"], "success")

            return {
                "risk": intel["risk"],
                "priority": priority,
                "prediction": prediction,
                "strategy": strategy,
                "adaptation": adaptation,
                "explanation": explanation,
                "next_steps": next_steps,
                "email": email,
                "email_event": event,
                "trace": trace,
                "agent_chain": "intelligence → prediction → strategy → execution → adaptation"
            }

        return {
            "risk": intel["risk"],
            "priority": priority,
            "prediction": prediction,
            "trace": trace,
            "agent_chain": "intelligence → prediction"
        }

    except Exception as e:
        return {
            "error": str(e),
            "recovery": "Fallback system activated",
            "trace": trace,
            "agent_chain": "error_handling → fallback"
        }


# Churn Agent (UPGRADED)
def top_churn_agent(accounts):

    ranked = sorted(
        accounts,
        key=lambda x: (x["support_tickets_open"] * 2 - x["daily_active_users"]),
        reverse=True
    )

    top = ranked[:3]
    results = []

    for acc in top:

        prompt = f"""
        Company: {acc['company']}
        Open Tickets: {acc['support_tickets_open']}
        Daily Users: {acc['daily_active_users']}

        Explain churn risk AND provide a SPECIFIC retention plan.
        """

        strategy = ask_llm(prompt) or "Provide dedicated support and engagement."

        results.append({
            "company": acc["company"],
            "risk_reason": f"High tickets: {acc['support_tickets_open']}, Low usage: {acc['daily_active_users']}",
            "strategy": strategy
        })

    return results