# 🧬 Blood Test Report Analyzer — with FastAPI, Celery, Redis, and MySQL

A multi-agent AI system that analyzes blood test reports using **CrewAI**, served through a **FastAPI API**, with **Celery for asynchronous background processing**, **Redis as the message broker**, and **MySQL for persistent result storage**.

This architecture allows the system to **handle multiple concurrent requests efficiently**, queueing tasks using **Redis** and processing them with **Celery** workers. and then storring the result in mysql database
---

## 🐛 Bugs Fixed & Modifications Made

### ✅ Code Fixes

#### 🔄 Import Errors

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
#### • In task.py nutrition_analysis and exercise_planning has agent=docrtor which is wrong because there is nutritionist and exercise_specialist agent in agent.py so nutrition_analysis will use nutritionist and exercise_planning will use exercise_specialist. corrected that

#### Updated file path was never passed to the agent. prev it is using default in the tool. so i have updated it so that file path is passed.

  ✅ Fixed with:
  ```python
result = medical_crew.kickoff({'query': query,'file_path': file_path})
  ```

#### • in main.py it is only calling doctor agent and not calling nutritionist and exercise_specialist so i have updated the code so that it will call other two agent with there task sequentialy. and save the output of each agent in a list then inserting it to the database after completing.

  ✅ Fixed with:
  ```python
results = []

# 2. Create a callback function to capture each task’s output
def task_callback(task_output):
    # name = getattr(task_output, 'task_name', '<unknown>')
    results.append(task_output.raw)
medical_crew = Crew(
    agents=[doctor, nutritionist, exercise_specialist],
    tasks=[help_patients, nutrition_analysis, exercise_planning],
    process=Process.sequential,
    task_callback=task_callback,
)
final  = medical_crew.kickoff({'query': query,'file_path': file_path})
  ```
#### created .env file to fetch the open ai api key.

#### 🧑‍⚕️ Agent Import

- ❌ `from crewai.agents import Agent`  
  ✅ Changed to `from crewai import Agent` to match the current version of CrewAI

- ❌ `from crewai_tools.tools.serper_dev_tool import SerperDevTool`  
  ✅ Changed to `from crewai_tools import SerperDevTool`

---

✅ Added a new file `models.py` for SQLAlchemy DB integration
✅ Made some changes in main.py for integrating Celery and MySQL

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
- Update the line in `main.py`:

```python
DATABASE_URL = "mysql+pymysql://root:Yourpassword@127.0.0.1:3306/blood_analysis"
```

---

### 5. update your open ai api key on .env file

## ⚙️ Run the Application

### ✅ 1. Start FastAPI Server

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
  -F "file=@C:\Your\Folder\Path\sample.pdf" \
  -F "query=analyse my blood test report"
```

Response:
```json
{
  ...,
 ...,
  "task_id": "4dd1b3d6-3223-48ee-bd36-1df7d8491e70"
}
```

---

### 📥 Fetch Result

```bash
curl http://localhost:8000/result/task id which you recieved
```

---

## 📌 Tech Stack

- **Python 3.11**
- **FastAPI**
- **Celery + Redis**
- **CrewAI (multi-agent reasoning)**
- **MySQL + SQLAlchemy**
