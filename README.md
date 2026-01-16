# 🧠 Legacy Code Explainer  
**Regex-Based COBOL & JCL Analysis Tool with Multi-Turn Chat Support**

---

## 📌 Project Overview

**Legacy Code Explainer** is a full-stack application designed to **analyze, understand, and explain legacy mainframe code**, specifically **COBOL** and **JCL**.

The system performs **static code analysis**, converts legacy code into a structured **Intermediate Representation (IR)**, and generates **clear, professional explanations**.  
It also supports **multi-turn conversational queries**, allowing users to ask follow-up questions on the same code without re-parsing.

---

## ✨ Key Features

- ✅ COBOL & JCL static code analysis  
- ✅ Regex-based parsing with structured IR  
- ✅ One-time parsing per session (efficient)  
- ✅ AI-generated explanations grounded strictly in IR  
- ✅ **Multi-turn conversational chat on the same code**  
- ✅ SQLite-backed session & IR persistence  
- ✅ Clean backend–frontend separation  
- ✅ REST API with FastAPI  
- ✅ Streamlit-based UI  
- ✅ Pytest with coverage reporting  

---


---
## 🎥 Demo Video

📌 A complete walkthrough of the project is available in the demo video below:

▶️ **Watch Demo Video:**  
https://drive.google.com/file/d/1dmQeqIf5iixDveUBkeeQjdg2nio60X2y/view?usp=sharing




## 🔄 System Flow

```
User uploads COBOL / JCL code
            ↓
        FastAPI Backend
            ↓
     Regex-Based Parsers
            ↓
 Intermediate Representation (IR)
            ↓
 Initial Explanation (Static Analysis)
            ↓
  Multi-Turn Chat (IR Reused)
            ↓
     Streamlit Frontend UI

```

---

## 🧩 Parsing Strategy


### ✅ Used

* Python Regex (`re`)
* Modular parser factory
* Language-agnostic IR schema

---

## ▶️ How to Run the Project (IMPORTANT)

### 1️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
```

**Windows**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run Backend (FastAPI)

From **project root**:

```bash
uvicorn backend.app.main:app --reload
```

📌 Backend will start at:

```
http://127.0.0.1:8000
```

📌 API Docs:

```
http://127.0.0.1:8000/docs
```

---

## 🖥️ Run Frontend (Streamlit)

Open **new terminal**, then:

```bash
cd frontend
streamlit run app.py
```

📌 Frontend will start at:

```
http://localhost:8501
```

---

## 🧪 Testing & Coverage

### Run Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=term-missing
```

### HTML Coverage Report

```bash
pytest --cov=backend --cov-report=html
```

📂 Coverage output:

```
backend/htmlcov/index.html
```

---

## 🛠️ Tech Stack

| Layer    | Technology   |
| -------- | ------------ |
| Backend  | FastAPI      |
| Frontend | Streamlit    |
| Parsing  | Regex (`re`) |
| Testing  | Pytest       |
| Coverage | pytest-cov   |

---

## 🎯 Design Decisions

* ✔ Regex parsing chosen for simplicity & speed

* ✔ Clean separation of backend & frontend
* ✔ Scalable IR-based architecture

---

## 🚀 Future Enhancements


* AI-generated explanations
* Legacy code modernization suggestions
* Export to PDF / DOC reports

---

## 👨‍💻 Author

**Yash Jagdale**
Legacy Code Understanding & Modernization
(COBOL | JCL | Mainframe | Python | AI)

---
