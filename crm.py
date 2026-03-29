import random

base_deals = [
    {
        "id": "deal_1",
        "company": "Pinnacle Enterprises",
        "email": "pinnacle@gmail.com",
        "stage": "Negotiation",
        "value": 50000,
        "days_no_reply": 10,
        "engagement_score": 0.2,
        "status": "active",
        "email_opened": True,
        "replied": False,
        "competitor": "Zoho",
        "company_size": random.choice(["Startup", "Mid", "Enterprise"]),
        "recent_funding": random.choice(["Seed", "Series A", "Series B", "None"])
    },
    {
        "id": "deal_2",
        "company": "CloudEdge",
        "email": "cloudedge@gmail.com",
        "stage": "Proposal",
        "value": 80000,
        "days_no_reply": 12,
        "engagement_score": 0.1,
        "status": "active",
        "email_opened": False,
        "replied": False,
        "competitor": "Salesforce"
    }
]

active_accounts = [
    {
        "company": "AlphaCorp",
        "support_tickets_open": 12,
        "daily_active_users": 120
    },
    {
        "company": "BetaTech",
        "support_tickets_open": 3,
        "daily_active_users": 900
    },
    {
        "company": "GammaSoft",
        "support_tickets_open": 18,
        "daily_active_users": 80
    }
]
def generate_dynamic_deals(n=5):
    companies = ["AlphaCorp", "BetaTech", "GammaSoft", "DeltaAI"]

    new_deals = []
    for i in range(n):
        new_deals.append({
            "id": f"deal_dyn_{i}",
            "company": random.choice(companies),
            "email": f"contact{i}@company.com",
            "stage": "Negotiation",
            "value": random.randint(20000, 100000),
            "days_no_reply": random.randint(1, 15),
            "engagement_score": round(random.uniform(0.1, 0.9), 2),
            "status": "active",
            "email_opened": random.choice([True, False]),
            "replied": False,
            "competitor": random.choice(["Zoho", "Salesforce", None])
        })
    return new_deals


deals = base_deals + generate_dynamic_deals(random.randint(3, 7))