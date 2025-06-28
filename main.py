from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from celery import Celery
from crewai import Crew, Process
from agents import doctor
from task import help_patients

import os
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AnalysisResult

# === Database Configuration ===
DATABASE_URL = "mysql+pymysql://root:Vineet%40@localhost:3306/blood_analysis"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# === Celery Configuration ===
celery_app = Celery("blood_analyzer")
celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/0'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.timezone = 'Asia/Kolkata'
celery_app.conf.enable_utc = True

# === Celery Task ===
@celery_app.task
def analyze_blood_test(query: str, file_path: str, task_id: str):
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from models import Base, AnalysisResult

    DATABASE_URL = "mysql+pymysql://root:Vineet%40@127.0.0.1:3306/blood_analysis"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Run CrewAI analysis
        medical_crew = Crew(
            agents=[doctor],
            tasks=[help_patients],
            process=Process.sequential,
        )
        result = medical_crew.kickoff({'query': query})

        # Fetch the row
        db_result = db.query(AnalysisResult).filter_by(task_id=task_id).first()
        if db_result is None:
            raise Exception(f"No task found with task_id={task_id}")

        db_result.status = "COMPLETED"
        db_result.result = str(result)
        db.commit()
        return str(result)

    except Exception as e:
        db_result = db.query(AnalysisResult).filter_by(task_id=task_id).first()
        if db_result:
            db_result.status = "FAILED"
            db_result.result = str(e)
            db.commit()
        return f"Error during analysis: {str(e)}"

    finally:
        db.close()


# === FastAPI App ===
app = FastAPI(title="Blood Test Report Analyser")

@app.get("/")
def root():
    return {"message": "Blood Test Report Analyser API with Celery and MySQL is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        task_id = str(uuid.uuid4())

        db = SessionLocal()
        db_result = AnalysisResult(
            task_id=task_id,
            filename=file.filename,
            query=query.strip(),
            status="PENDING"
        )
        db.add(db_result)
        db.commit()
        db.close()

        task = analyze_blood_test.apply_async(args=[query.strip(), file_path, task_id], task_id=task_id)
        return {"status": "queued", "task_id": task_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/result/{task_id}")
def get_result(task_id: str):
    db = SessionLocal()
    record = db.query(AnalysisResult).filter_by(task_id=task_id).first()
    db.close()

    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "status": record.status,
        "query": record.query,
        "file": record.filename,
        "result": record.result,
        "created_at": record.created_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
