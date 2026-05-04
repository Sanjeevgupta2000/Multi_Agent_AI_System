import streamlit as st
from pipeline import run_research_pipeline
import time

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PDF FUNCTION ---------------- #
def generate_pdf(report_text):
    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []
    for line in report_text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
    return file_path

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("⚙️ System Overview")
st.sidebar.markdown("""
### 🤖 Multi-Agent Flow
1. 🔎 Search Agent  
2. 🌐 Reader Agent  
3. 📝 Writer Agent  
4. 🧠 Critic Agent  

### 🚀 Features
- Chat Interface  
- Real-time steps  
- PDF Export  
""")

# ---------------- TITLE ---------------- #
st.title("🤖 AI Research Assistant")
st.caption("Multi-Agent Research System with Real-Time Execution")

# ---------------- SESSION ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ---------------- CHAT DISPLAY ---------------- #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ---------------- #
prompt = st.chat_input("Enter your research topic...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        # 🔥 Progress UI
        progress = st.progress(0)
        status = st.empty()

        # Step 1
        status.info("🔎 Step 1: Search Agent is gathering information...")
        progress.progress(25)
        time.sleep(1)

        # Step 2
        status.info("🌐 Step 2: Reader Agent is scraping content...")
        progress.progress(50)
        time.sleep(1)

        # Step 3
        status.info("📝 Step 3: Writer Agent is generating report...")
        progress.progress(75)
        time.sleep(1)

        # Run actual pipeline
        result = run_research_pipeline(prompt)

        # Step 4
        status.info("🧠 Step 4: Critic Agent is reviewing report...")
        progress.progress(100)
        time.sleep(1)

        status.success("✅ Research Completed!")

        # Save result
        st.session_state.last_result = result

        # ---------------- OUTPUT TABS ---------------- #
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔎 Search",
            "📄 Scraped",
            "📝 Report",
            "🧠 Feedback"
        ])

        with tab1:
            st.write(result.get("search_results", ""))

        with tab2:
            st.write(result.get("scraped_content", ""))

        with tab3:
            st.write(result.get("report", ""))

        with tab4:
            st.write(result.get("feedback", ""))

    st.session_state.messages.append({
        "role": "assistant",
        "content": "✅ Research completed. See detailed results above."
    })

# ---------------- PDF DOWNLOAD ---------------- #
if st.session_state.last_result:
    report_text = st.session_state.last_result.get("report", "")

    if report_text:
        pdf_path = generate_pdf(report_text)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Report as PDF",
                data=f,
                file_name="AI_Research_Report.pdf",
                mime="application/pdf"
            )
