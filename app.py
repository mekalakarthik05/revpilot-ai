import streamlit as st
import time
from datetime import datetime

from crm import deals
from agents import coordinator_agent, get_memory, prospecting_agent, metrics_agent
from actions import send_email, get_email_events

st.set_page_config(page_title="RevPilot AI", layout="wide")

# ================= UI STYLE =================
st.markdown("""
<style>
body { background-color: #0b0f1a; }

.card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.log {
    background:#111827;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    border-left: 4px solid #6366f1;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<h1 style='text-align:center;'>🚀 RevPilot AI</h1>
<p style='text-align:center;color:gray;'>
Autonomous Multi-Agent Revenue Intelligence System
</p>
""", unsafe_allow_html=True)

# ================= METRICS =================
total = len(deals)
recovered = len([d for d in deals if d["status"] == "Recovery Initiated"])
revenue = sum(d["value"] for d in deals if d["status"] == "Recovery Initiated")

metrics = metrics_agent(deals)

st.markdown("## 📊 Business Dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Deals", total)
c2.metric("Recovered Deals", recovered)
c3.metric("Revenue Impact", f"₹{revenue}")
c4.metric("Conversion", f"{metrics['conversion']}%")

st.caption(f"Cycle Time Reduced: {metrics['cycle_reduction']}%")

# ================= AI CONTROL =================
st.markdown("## 🎛️ AI Control Panel")

auto_mode = st.toggle("Enable Autonomous Mode")

if auto_mode:
    st.success("🟢 Autonomous AI Running")
else:
    st.warning("🟡 Manual Mode")

# ================= PIPELINE =================
st.markdown("## 📊 Pipeline Overview")

left, right = st.columns([1, 3])

with left:
    st.markdown("<div class='card'><h4>Risk Distribution</h4>", unsafe_allow_html=True)

    high = len([d for d in deals if d["days_no_reply"] > 10])
    medium = len([d for d in deals if 5 < d["days_no_reply"] <= 10])
    low = total - high - medium

    def bar(label, value, color):
        percent = int((value / max(total,1)) * 100)
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <b>{label}</b> ({value})
            <div style="background:#1f2937;border-radius:6px;">
                <div style="
                    width:{percent}%;
                    background:{color};
                    padding:6px;
                    border-radius:6px;
                    text-align:right;
                    color:white;
                ">
                {percent}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    bar("High Risk", high, "#ef4444")
    bar("Medium Risk", medium, "#f59e0b")
    bar("Low Risk", low, "#22c55e")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='card'><h4>⚡ AI System Status</h4>", unsafe_allow_html=True)
        st.success("Autonomous Agents Active")
        st.write("• Intelligence Agent: Running")
        st.write("• Strategy Agent: Optimizing")
        st.write("• Execution Agent: Active")
        st.write("• Learning Engine: Updating")
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='card'><h4>📈 Live Impact</h4>", unsafe_allow_html=True)
        st.metric("Decisions Made", total)
        st.metric("Actions Triggered", recovered)
        st.metric("Success Rate", f"{int((recovered/total)*100)}%")
        st.metric("Avg Response Time", "0.3s")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= AI INTELLIGENCE =================
st.markdown("## 🧠 AI Intelligence Layer")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'><h4>🧠 Decision Brain</h4>", unsafe_allow_html=True)

    sample = deals[0]
    result = coordinator_agent(sample)

    st.write(f"Inactivity: {sample['days_no_reply']} days")
    st.write(f"Engagement: {sample['engagement_score']}")
    st.write(f"Churn Prediction: {result['prediction']}%")

    st.progress(result['prediction'] / 100)
    st.caption("AI evaluating deal risk signals")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'><h4>📊 Strategy Effectiveness</h4>", unsafe_allow_html=True)

    def stat(label, value, color):
        percent = int((value / max(total,1)) * 100)
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <b>{label}</b>
            <div style="background:#1f2937;border-radius:6px;">
                <div style="
                    width:{percent}%;
                    background:{color};
                    padding:6px;
                    border-radius:6px;
                    text-align:right;
                    color:white;
                ">
                {value}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    stat("Recovered", recovered, "#6366f1")
    stat("Pending", total - recovered, "#64748b")

    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'><h4>💡 AI Insights</h4>", unsafe_allow_html=True)

    st.write("• AI predicts deal churn in next 7 days")
    st.write("• Competitive signals detected (Zoho, Salesforce)")
    st.write("• ROI messaging drives highest conversion")
    st.write("• Follow-up delay = biggest revenue leak")

    st.success("AI continuously learning")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= AUTONOMOUS ENGINE =================
st.markdown("## 🤖 Autonomous Engine")

log_box = st.empty()
logs = []

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    logs.insert(0, f"<div class='log'><b>[{t}]</b><br>{msg}</div>")
    log_box.markdown("".join(logs[:10]), unsafe_allow_html=True)

if st.button("Start AI Execution") or auto_mode:

    progress = st.progress(0)

    for i, deal in enumerate(deals):

        result = coordinator_agent(deal)

        if result["risk"] != "LOW":

            log(f"🚨 Risk detected → {deal['company']}")
            log(f"🧠 Prediction → {result['prediction']}%")
            log(f"🎯 Strategy → {result['strategy']['name']}")

            log("📧 Generating Email...")
            log(result["email"])

            event = send_email(
                deal["email"],
                "Regarding our discussion",
                result["email"]
            )

            deal["email_opened"] = event["opened"]
            deal["replied"] = event["replied"]

            log(f"📨 Sent → {deal['email']}")
            log(f"👀 Opened → {event['opened']}")
            log(f"💬 Replied → {event['replied']}")

            if result.get("competitive"):
                log(f"⚔️ {result['competitive']['battlecard']}")

            log(f"🔁 Adaptation → {result['adaptation']}")
            log("────────────")

        progress.progress((i+1)/len(deals))
        time.sleep(0.25)

    st.success("Autonomous cycle completed")

# ================= LEARNING =================
st.markdown("## 🧠 Learning Engine")

memory = get_memory()

if memory:
    st.metric("Learned Strategies", len(memory))
    for m in memory:
        st.write(f"• {m['company']} → {m['strategy']}")
    st.success("AI improving continuously")
else:
    st.info("Learning in progress...")

# ================= PROSPECTING =================
st.markdown("## 🔍 Prospecting Agent")

for l in prospecting_agent():
    st.markdown(f"""
    <div class='card'>
    <b>{l['company']}</b> ({l['industry']})<br>
    Score: {l['score']}<br>
    📧 {l['outreach']}
    </div>
    """, unsafe_allow_html=True)

# ================= EMAIL TRACKING =================
st.markdown("## 📬 Email Tracking")

events = get_email_events()

if events:
    for e in events:
        status = "🟢 Replied" if e["replied"] else ("🟡 Opened" if e["opened"] else "🔴 Not Opened")

        st.markdown(f"""
        <div class='card'>
        📧 {e['email']}<br>
        Status: {status}<br>
        Time: {e['time']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No email activity yet")