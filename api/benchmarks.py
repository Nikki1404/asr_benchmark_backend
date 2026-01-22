from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
import io
from typing import List
from database import SessionLocal
from schemas import FileUploadResponse
import json
from crud import persist_dashboard_entries
from auth import get_current_active_user, get_current_user_optional
from models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
COLUMN_MAP = {
    "Audio File Name": ["file name", "audio_name", "audio file", "name", "audio name"],
    "Audio Length": ["duration", "audio length (sec)", "length"],
    "Model": ["model name"],
    "Ground_truth": ["ground truth", "actual text", "reference"],
    "Transcription": ["output", "prediction", "transcript"],
    "WER Score": ["wer", "word error rate"],
    "Inference time (in sec)": ["latency", "inference", "time"]
}

REQUIRED_COLUMNS = list(COLUMN_MAP.keys())

def normalize_columns(df: pd.DataFrame):
    df_cols_lower = {c.lower(): c for c in df.columns}

    for required in REQUIRED_COLUMNS:
        if required in df.columns:
            continue  # column exists

        # try to find a similar column
        found = False
        for alt in COLUMN_MAP[required]:
            if alt.lower() in df_cols_lower:
                df[required] = df[df_cols_lower[alt.lower()]]
                found = True
                break

        # if still not found → create empty column
        if not found:
            df[required] = ""

    return df

def parse_time_value(value):
    if value is None or str(value).strip() in ["", "nan", "NaN"]:
        return 0.0

    s = str(value).strip()

    # Case 1: "1 day, 0:03:22"
    if "day" in s:
        parts = s.split(",")
        days = int(parts[0].split()[0])
        time_part = parts[1].strip()
        t = list(reversed(time_part.split(":")))
        seconds = sum(float(x) * (60 ** idx) for idx, x in enumerate(t))
        return days * 86400 + seconds

    # Case 2: "06:44:00" or "03:22"
    if ":" in s:
        t = list(reversed(s.split(":")))
        return sum(float(x) * (60 ** idx) for idx, x in enumerate(t))

    # Case 3: Plain numeric
    try:
        return float(s)
    except:
        raise ValueError(f"Invalid time format: {s}")

@router.post(
    "/upload", 
    response_model=FileUploadResponse,
    summary="Upload benchmark Excel file",
    description="Upload and process an Excel file containing ASR benchmark data",
    response_description="Processed benchmark data ready for analysis",
    responses={
        200: {"description": "File processed successfully"},
        400: {"description": "Invalid file format or missing required columns"},
        500: {"description": "Server error during file processing"}
    },
    tags=["Benchmarks"]
)
async def upload_benchmark_file(
    file: UploadFile = File(
        ..., 
        description="Excel file (.xlsx or .xls) containing benchmark data",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    Upload and process an Excel file containing ASR benchmark data.
    
    **Required Excel columns:**
    - Audio File Name: Name of the audio file tested
    - Audio Length: Duration of audio in seconds
    - Model: Name of the ASR model used
    - Ground_truth: Correct transcription text
    - Transcription: Model's transcription output
    - WER Score: Word Error Rate as a decimal (0.0 to 1.0)
    - Inference time (in sec): Processing time in seconds
    
    **File Requirements:**
    - Format: Excel (.xlsx or .xls)
    - Size: Maximum 50MB
    - Structure: First row must contain column headers
    
    **Returns:**
    - Processed data array ready for dashboard analysis
    - Summary message with processing statistics
    
    **Errors:**
    - 400: Invalid file format or missing required columns
    - 400: Invalid data types in rows
    - 500: Server processing error
    """
    user_id = current_user.id if current_user else "anonymous"
    # Validate file type
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        df = df.dropna(how="all")

        if df.empty:
            raise HTTPException(400, "The uploaded file contains no usable data.")

        df = normalize_columns(df)
        processed_data = []
        for i, row in df.iterrows():
            try:
                audio_length = parse_time_value(row["Audio Length"])
                inference_time = parse_time_value(row["Inference time (in sec)"])
                # WER
                wer_raw = row["WER Score"]
                if pd.isna(wer_raw) or str(wer_raw).strip() == "":
                    wer_score = 0.0
                else:
                    wer_score = float(wer_raw)

                processed_row = {
                    "Audio File Name": str(row["Audio File Name"]),
                    "Audio Length": audio_length,
                    "Model": str(row["Model"]),
                    "Ground_truth": str(row["Ground_truth"]),
                    "Transcription": str(row["Transcription"]),
                    "WER Score": wer_score,
                    "Inference time (in sec)": inference_time
                }
                processed_data.append(processed_row)
            except (ValueError, TypeError) as e:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid data in row {i+2}: {str(e)}"
                )
        
        if not processed_data:
            raise HTTPException(status_code=400, detail="No valid data found in the file")
        
        persist_dashboard_entries(db, processed_data, user_id)
        
        return FileUploadResponse(
            data=processed_data,
            message=f"Successfully processed {len(processed_data)} rows from {file.filename}"
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse the Excel file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
    finally:
        await file.close()
