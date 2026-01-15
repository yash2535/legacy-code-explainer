# 🧠 Legacy Code Explainer

**Regex-Based COBOL & JCL Analysis Tool**


---

##  Project Overview

**Legacy Code Explainer** is a full-stack tool designed to **analyze, understand, and explain legacy mainframe code** such as **COBOL** and **JCL**.

* 🔍 Backend: **FastAPI**
* 🧠 Parsing: **Regex-only parsers**
* 🖥️ Frontend: **Streamlit**
* 🧪 Testing: **Pytest + Coverage**

---
## 🎥 Demo Video

📌 A complete walkthrough of the project is available in the demo video below:

▶️ **Watch Demo Video:**  
https://drive.google.com/file/d/1KYBZYQbbogtYSPeB9zP8wjWt1Ri2fUXC/view?usp=drive_link




## 🔄 System Flow

```
User Uploads COBOL / JCL Code
            ↓
        FastAPI Backend
            ↓
     Regex-Based Parsers
            ↓
 Intermediate Representation (IR)
            ↓
 Explanation Engine
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
