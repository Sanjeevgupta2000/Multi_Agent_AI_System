import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Graph
from graphviz import Digraph

# ── PAGE CONFIG ─────────────────────────────────────
st.set_page_config(page_title="ResearchMind AI", page_icon="🔬", layout="wide")

# ── DARK UI CSS ─────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #0a0a0f; color: #e8e4dc; }

[data-testid="stTextInput"] input {
    background: rgba(20,20,25,0.9);
    color: white;
    border: 1px solid rgba(255,140,50,0.4);
}

.stButton>button {
    background: linear-gradient(135deg, #ff8c32, #ff5a1a);
    color: black;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ── STREAMING FUNCTION ─────────────────────────────────────
def stream_text(text, speed=0.01):
    placeholder = st.empty()
    full = ""
    for ch in text:
        full += ch
        placeholder.markdown(full)
        time.sleep(speed)
    return full

# ── PDF FUNCTION ─────────────────────────────────────
def create_pdf(text):
    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []
    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
    return file_path

# ── GRAPH ─────────────────────────────────────
def show_graph():
    dot = Digraph()
    dot.node("Search")
    dot.node("Reader")
    dot.node("Writer")
    dot.node("Critic")

    dot.edge("Search", "Reader")
    dot.edge("Reader", "Writer")
    dot.edge("Writer", "Critic")

    st.graphviz_chart(dot)

# ── SESSION STATE ─────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# ── SIDEBAR (HISTORY + GRAPH) ─────────────────────────
with st.sidebar:
    st.title("📚 History")

    for item in st.session_state.history:
        if st.button(item["topic"]):
            st.write(item["report"])

    st.markdown("---")
    st.markdown("### 🔗 Agent Flow")
    show_graph()

# ── HEADER ─────────────────────────────────────
st.title("🔬 ResearchMind AI")
st.caption("Multi-Agent Research System")

# ── CHAT HISTORY ─────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── INPUT ─────────────────────────────────────
prompt = st.chat_input("Enter research topic...")

# ── MAIN PIPELINE ─────────────────────────────────────
if prompt:
    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant
    with st.chat_message("assistant"):
        with st.spinner("Running AI Agents..."):

            # STEP 1: SEARCH
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find detailed info about {prompt}")]
            })
            search_data = sr["messages"][-1].content

            # STEP 2: READER
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user", search_data[:800])]
            })
            reader_data = rr["messages"][-1].content

            # STEP 3: WRITER
            report = writer_chain.invoke({
                "topic": prompt,
                "research": reader_data
            })

            # STREAM OUTPUT
            st.markdown("### 📝 Report")
            stream_text(report)

            # STEP 4: CRITIC
            feedback = critic_chain.invoke({
                "report": report
            })

            st.markdown("### 🧐 Feedback")
            stream_text(feedback, speed=0.005)

            # PDF DOWNLOAD
            pdf_file = create_pdf(report)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇ Download PDF",
                    f,
                    file_name="report.pdf"
                )

    # save messages
    st.session_state.messages.append({
        "role": "assistant",
        "content": report
    })

    # save history
    st.session_state.history.append({
        "topic": prompt,
        "report": report
    })
