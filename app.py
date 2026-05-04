import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── INPUT FIX (DARK + WHITE TEXT) ── */
.stTextInput > div > div > input {
    background: rgba(20, 20, 25, 0.9) !important;
    border: 1px solid rgba(255,140,50,0.35) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    backdrop-filter: blur(6px);
}

.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.2) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #888888 !important;
}

.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    width: 100%;
}

/* Footer */
.notice {
    font-size: 0.7rem;
    color: #605850;
    text-align: center;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ── UI ───────────────────────────────────────────────────────────────────────
st.title("🔬 ResearchMind")

topic = st.text_input("Research Topic", placeholder="e.g. Quantum computing")

run_btn = st.button("⚡ Run Research Pipeline")

# ── Pipeline ─────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a topic")
    else:
        with st.spinner("Running AI agents..."):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find info about {topic}")]
            })

            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user", sr["messages"][-1].content)]
            })

            report = writer_chain.invoke({
                "topic": topic,
                "research": rr["messages"][-1].content
            })

            feedback = critic_chain.invoke({
                "report": report
            })

        st.success("Done!")

        st.subheader("Report")
        st.write(report)

        st.subheader("Critic Feedback")
        st.write(feedback)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="notice">ResearchMind · Built with Streamlit</div>', unsafe_allow_html=True)
