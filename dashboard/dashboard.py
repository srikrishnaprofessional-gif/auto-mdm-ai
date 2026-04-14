# -------------------------
# 🔧 FIX IMPORT PATH
# -------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -------------------------
# 📦 IMPORTS
# -------------------------
import streamlit as st
import time

from app.agent import run_agent
from app.vector_memory import query_memory
from app.ai_agent import ask_llm

# -------------------------
# ⚙️ PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="AutoMDM AI Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# 🎨 HEADER
# -------------------------
st.markdown("""
<h1 style='margin-bottom:0;'>🤖 AutoMDM AI Platform</h1>
<p style='color:gray;'>Unified Customer Data | MDM | AI-Powered Insights</p>
<hr>
""", unsafe_allow_html=True)

# -------------------------
# 🎛️ SIDEBAR
# -------------------------
st.sidebar.title("⚙️ Control Panel")

live_mode = st.sidebar.toggle("Enable Live Mode", value=False)
refresh_rate = st.sidebar.slider("Refresh Interval (sec)", 2, 10, 3)

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 Active Agents")

def render_agent(agent, percent, logs):
    status = "🟢 Completed" if percent == 100 else "🟡 Running"

    st.sidebar.markdown(f"""
    <div style="padding:10px;margin-bottom:10px;border-radius:8px;
    background:#1e1e1e;border-left:4px solid #00c853;">
    <b>{agent}</b><br>
    Status: {status}
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.progress(percent)

    for log in logs[-1:]:
        st.sidebar.caption(log)

# -------------------------
# 🧠 EXECUTIVE REPORT UI
# -------------------------
def render_report(decisions):
    st.markdown("## 📊 Executive AI Report")

    cols = st.columns(3)

    for i, (agent, info) in enumerate(decisions.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border-left:5px solid #00c853;
                height:100%;
            ">
            <h4>{agent}</h4>
            <b>Summary:</b><br>{info['summary']}<br><br>
            <b>Insight:</b><br>{info['detail']}<br><br>
            <b>Impact:</b><br>{info['impact']}<br><br>
            <b>Confidence:</b> {info['confidence']}
            </div>
            """, unsafe_allow_html=True)

# -------------------------
# 📊 DATA TABLE UI
# -------------------------
def render_data(df):
    st.markdown("## 📁 Unified Customer 360 View")
    st.dataframe(df, use_container_width=True)

# -------------------------
# 💬 CHAT UI
# -------------------------
def render_chat():
    st.markdown("## 💬 Ask Your Data Agent")

    query = st.text_input("Ask something about your data")

    if query:
        memory = query_memory(query)

        prompt = f"""
        You are an AI data assistant.

        Question: {query}
        Memory: {memory}

        Provide a clear answer.
        """

        response = ask_llm(prompt)

        st.success("AI Response")
        st.write(response)

# -------------------------
# 🚀 MAIN EXECUTION
# -------------------------
def run_pipeline():
    df, decisions, progress, logs = run_agent()

    # Sidebar Agents
    for agent in progress:
        render_agent(agent, progress[agent], logs)

    # Main UI
    render_report(decisions)
    st.markdown("---")
    render_data(df)

    # Download button
    st.download_button(
        label="⬇️ Download Clean Data (CSV)",
        data=df.to_csv(index=False),
        file_name="customer_360.csv",
        mime="text/csv",
        key=f"download_{time.time()}"
    )

    st.markdown("---")
    render_chat()

# -------------------------
# 🎯 RUN MODES
# -------------------------
if live_mode:
    st.success("🔴 Live Processing Enabled")

    while True:
        run_pipeline()
        time.sleep(refresh_rate)

else:
    if st.button("🚀 Run Data Pipeline"):
        run_pipeline()

# -------------------------
# 📌 FOOTER
# -------------------------
st.markdown("""
<hr>
<p style='text-align:center;color:gray;'>
AutoMDM AI Platform • Real-time Data Integration • MDM • AI Insights
</p>
""", unsafe_allow_html=True)