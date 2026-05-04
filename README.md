# 🔬 ResearchMind AI — Multi-Agent Research System

A production-style **Generative AI application** that uses multiple AI agents to perform end-to-end research — from searching the web to generating structured reports and critical analysis.

---

## 🚀 Overview

**ResearchMind AI** is a multi-agent system built using LLMs and tool integrations.
It automates the complete research workflow:

1. 🔍 Search for relevant information
2. 📄 Extract detailed content from sources
3. ✍️ Generate a structured research report
4. 🧐 Critically evaluate the report

All inside a **modern chat-based UI with streaming output**.

---

## 🧠 Architecture

```
User Input
   ↓
🔍 Search Agent
   ↓
📄 Reader Agent
   ↓
✍️ Writer Chain
   ↓
🧐 Critic Chain
   ↓
Final Output
```

---

## ✨ Features

* 💬 Chat-style interface (like ChatGPT)
* ⚡ Real-time streaming output
* 🧠 Multi-agent orchestration
* 📚 Research memory (history tracking)
* 📄 PDF export for reports
* 🔗 Agent workflow visualization
* 🌙 Modern dark UI (Streamlit)

---

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **LLMs (Mistral API)**
* **Streamlit**
* **Tavily API (Web Search)**
* **ReportLab (PDF generation)**

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/researchmind-ai.git
cd researchmind-ai
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project can be deployed on:

* Streamlit Cloud
* Render
* Hugging Face Spaces

---

## 📊 Example Use Cases

* Academic research automation
* Market analysis
* Technology trend reports
* AI-assisted documentation

---

## ⚠️ Limitations

* Depends on external APIs (Mistral, Tavily)
* Response quality depends on source data
* Not optimized for very large-scale research yet

---

## 🔮 Future Improvements

* RAG (Retrieval-Augmented Generation)
* Vector database (FAISS / Pinecone)
* Async multi-agent execution
* Better citation tracking
* User authentication

---

## 👨‍💻 Author

**Sanjeev Gupta**
Aspiring Generative AI Engineer

---

## ⭐ Show Your Support

If you found this project useful:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---

## 📜 License

This project is open-source and available under the MIT License.
