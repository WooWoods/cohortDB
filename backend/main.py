from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List
import crud
import models
import schemas
from database import db
from services import file_handler

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def startup_event():
    db.connect()
    db.create_tables([
        models.ReportedAges,
        models.BsRate,
        models.Coverage,
        models.Fastp,
        models.Markdup,
        models.PicardAlignmentSummary,
        models.PicardGcBias,
        models.PicardGcBiasSummary,
        models.PicardHs,
        models.PicardInsertSize,
        models.PicardQualityYield,
        models.Screen,
    ])

@app.on_event("shutdown")
def shutdown_event():
    if not db.is_closed():
        db.close()

@app.post("/api/v1/data/upload")
async def upload_data(file: UploadFile = File(...)):
    try:
        file_handler.process_uploaded_file(file)
        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/initial")
async def get_initial_data_route():
    try:
        data = crud.get_initial_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/download")
async def download_data(samples: str):
    sample_list = [s.strip() for s in samples.split(',')]
    try:
        excel_file = file_handler.generate_excel_file(sample_list)
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=cohort_data.xlsx"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/filter")
async def filter_data(filters: schemas.FilterSchema):
    try:
        data = crud.get_filtered_data(filters)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
