
# 🧪 Blood Test Report Analyzer — Debugged and Enhanced

A multi-agent AI system that analyzes blood test reports using **CrewAI**, served through a **FastAPI API**, with **Celery for async processing** and **MySQL for result storage**.

---

## 🚀 Project Objective

This system was initially buggy and incomplete. The goal was to **debug** and **make it fully functional** using:

- ✅ FastAPI for HTTP interface  
- ✅ CrewAI agents for medical reasoning  
- ✅ Celery for background tasks  
- ✅ Redis as task broker  
- ✅ MySQL with SQLAlchemy ORM for storing results  

---

## 🐛 Bugs Fixed & Modifications Made

### ✅ Environment & Library Issues

- 🔹 Used Python 3.11.0
- 🔹 Created a virtual environment:  
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- 🔹 Installed all necessary libraries:  
  ```bash
  pip install crewai crewai-tools fastapi uvicorn celery redis python-multipart sqlalchemy pymysql
  ```

---

### ✅ Code Fixes

#### 🔄 Import Errors

- ❌ `from crewai_tools.tools.serper_dev_tool import SerperDevTool`  
  ✅ Changed to `from crewai_tools import SerperDevTool`

- ❌ `PDFLoader` not defined  
  ✅ Used:  
  ```python
  from langchain_community.document_loaders import PyPDFLoader
  ```

#### 🧠 Tool Fix

- Defined `BloodTestReportTool` as a valid CrewAI tool:
  ```python
  @tool("Read Blood Test Report")
  def read_data_tool(query: str):
      ...
  ```

#### 🔐 LLM Configuration

- ❌ `llm` was undefined  
  ✅ Fixed with:

  ```python
  from crewai.llm import LLM

  llm = LLM(
      model="gpt-4.1-mini",
      api_key="your-openai-api-key",
      temperature=0.8
  )
  ```

#### 🧑‍⚕️ Agent Import

- ❌ `from crewai.agents import Agent`  
  ✅ Changed to `from crewai import Agent` to match the current version of CrewAI

---

## 🧰 Setup Instructions

### 1. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install crewai crewai-tools fastapi uvicorn celery redis python-multipart sqlalchemy pymysql
```

---

### 3. Run Redis (using Docker)

```bash
docker run -d -p 6379:6379 --name redis redis
```

---

### 4. Run MySQL and Create DB

- Create a database named `blood_analysis`
- Update this line in `main.py` (encode `@` as `%40`):

```python
DATABASE_URL = "mysql+pymysql://root:Vineet%40@127.0.0.1:3306/blood_analysis"
```

---

## ⚙️ Run the Application

### ✅ 1. Start FastAPI server

```bash
uvicorn main:app --reload --port 8000
```

---

### ✅ 2. Start Celery Worker (Windows requires `--pool=solo`)

```bash
celery -A main.celery_app worker --loglevel=info --pool=solo
```

---

## 🧪 API Usage

### 🔄 Upload & Analyze a Blood Report

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@C:\Users\KIIT\Desktop\Folder\blood-test-analyser-debug\data\sample.pdf" \
  -F "query=analyse my blood test report"
```

Response:

```json
{
  "status": "queued",
  "task_id": "4dd1b3d6-3223-48ee-bd36-1df7d8491e70"
}
```

---

### 📥 Fetch Result

```bash
curl http://localhost:8000/result/4dd1b3d6-3223-48ee-bd36-1df7d8491e70
```

---

## 📁 Folder Structure

```
.
├── main.py               # FastAPI + Celery + DB logic
├── agents.py             # CrewAI medical agent
├── task.py               # CrewAI task for analyzing report
├── tools.py              # PDF analysis tool
├── models.py             # SQLAlchemy DB model
├── data/                 # Folder for temp uploaded PDFs
├── venv/                 # Python virtual environment
```

---

## 📌 Tech Stack

- **Python 3.11**
- **FastAPI**
- **Celery + Redis**
- **CrewAI (multi-agent reasoning)**
- **MySQL + SQLAlchemy**

---

## 🧠 Future Enhancements

- Add JWT user authentication
- Support multi-user task queues
- Build a frontend for uploading reports

---

## 🙌 Author

> Debugged and documented by [Your Name]
