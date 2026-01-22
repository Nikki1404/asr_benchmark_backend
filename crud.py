from sqlalchemy.orm import Session
from models import BlogPost, BenchmarkResult, DashboardData
from schemas import BlogPostCreate
import json
import uuid
from typing import List, Dict, Union

def create_blog_post(db: Session, post: BlogPostCreate):
    # Convert Pydantic models to dict for JSON storage
    benchmark_data = None
    if post.benchmark_data:
        benchmark_data = [item.model_dump() for item in post.benchmark_data]
    
    model_performance_data = None
    if post.model_performance_data:
        model_performance_data = [item.model_dump() for item in post.model_performance_data]
    
    db_post = BlogPost(
        title=post.title,
        author=post.author,
        excerpt=post.excerpt,
        content=post.content,
        benchmark_data=benchmark_data,
        model_performance_data=model_performance_data
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlogPost).offset(skip).limit(limit).all()

def get_blog_post(db: Session, post_id: str):
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def create_benchmark_result(db: Session, model: str, wer: float, dataset: str):
    db_result = BenchmarkResult(model=model, wer=wer, dataset=dataset)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_benchmark_results(db: Session):
    return db.query(BenchmarkResult).all()

def create_dashboard_data(db: Session, data: dict):
    db_data = DashboardData(**data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_dashboard_data(db: Session):
    return db.query(DashboardData).all()

def persist_dashboard_entries(
    db: Session,
    rows: Union[Dict, List[Dict]],
    user_id: str
):
    """
    Universal persistence function:
    - Accepts one dict OR list of dicts.
    - Auto-detects single vs multiple entries.
    - Uses bulk insert for performance.
    - Safe for concurrent writes.
    - Automatically rolls back on error.
    """

    if isinstance(rows, dict):
        rows = [rows]

    entries = []

    try:
        for r in rows:
            entry = DashboardData(
                id=str(uuid.uuid4()),
                audio_file_name=r.get("Audio File Name"),
                audio_length=r.get("Audio Length"),
                model=r.get("Model"),
                ground_truth=r.get("Ground_truth"),
                transcription=r.get("Transcription"),
                wer_score=r.get("WER Score"),
                inference_time=r.get("Inference time (in sec)"),
                created_by=user_id
            )
            entries.append(entry)

        if len(entries) == 1:
            db.add(entries[0])
            db.commit()
            db.refresh(entries[0])
        else:
            db.bulk_save_objects(entries)
            db.commit()

        return entries

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to persist dashboard entries: {e}")