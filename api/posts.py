from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from schemas import BlogPostCreate, BlogPostResponse
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/", 
    response_model=List[BlogPostResponse],
    summary="Get all blog posts",
    description="Retrieve a paginated list of all blog posts with their benchmark data",
    response_description="List of blog posts with pagination support",
    tags=["Blog Posts"]
)
async def get_posts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all blog posts from the database.
    
    - **skip**: Number of posts to skip (for pagination)
    - **limit**: Maximum number of posts to return (default: 100, max: 100)
    
    Returns a list of blog posts sorted by creation date (newest first).
    Each post includes benchmark data and model performance metrics if available.
    """
    posts = crud.get_blog_posts(db, skip=skip, limit=limit)
    
    # Convert JSON fields back to proper format for frontend
    response_posts = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "date": post.date.isoformat() if post.date else None,
            "author": post.author,
            "excerpt": post.excerpt,
            "content": post.content,
            "benchmarkData": post.benchmark_data,
            "modelPerformanceData": post.model_performance_data
        }
        response_posts.append(post_dict)
    
    return response_posts

@router.post(
    "/", 
    response_model=BlogPostResponse,
    status_code=201,
    summary="Create a new blog post",
    description="Create a new blog post with optional benchmark data and model performance metrics",
    response_description="The created blog post with assigned ID and timestamp",
    tags=["Blog Posts"]
)
async def create_post(
    post: BlogPostCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new blog post in the database.
    
    - **title**: The title of the blog post
    - **author**: Author of the blog post
    - **excerpt**: Brief summary/excerpt of the post
    - **content**: Full HTML content of the blog post
    - **benchmark_data**: Optional array of benchmark results
    - **model_performance_data**: Optional array of model performance metrics
    
    The system automatically assigns a unique ID and timestamp to the post.
    """
    db_post = crud.create_blog_post(db=db, post=post)
    
    # Format response to match frontend expectations
    response = {
        "id": db_post.id,
        "title": db_post.title,
        "date": db_post.date.isoformat() if db_post.date else None,
        "author": db_post.author,
        "excerpt": db_post.excerpt,
        "content": db_post.content,
        "benchmarkData": db_post.benchmark_data,
        "modelPerformanceData": db_post.model_performance_data
    }
    
    return response

@router.get(
    "/{post_id}", 
    response_model=BlogPostResponse,
    summary="Get a specific blog post",
    description="Retrieve a single blog post by its unique identifier",
    response_description="The requested blog post with all associated data",
    responses={
        404: {"description": "Blog post not found"},
        200: {"description": "Blog post retrieved successfully"}
    },
    tags=["Blog Posts"]
)
async def get_post(
    post_id: str, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific blog post by its unique ID.
    
    - **post_id**: Unique identifier of the blog post
    
    Returns the complete blog post including:
    - Basic post information (title, author, date, excerpt, content)
    - Associated benchmark data if available
    - Model performance metrics if available
    
    Raises 404 error if the post is not found.
    """
    db_post = crud.get_blog_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Format response to match frontend expectations
    response = {
        "id": db_post.id,
        "title": db_post.title,
        "date": db_post.date.isoformat() if db_post.date else None,
        "author": db_post.author,
        "excerpt": db_post.excerpt,
        "content": db_post.content,
        "benchmarkData": db_post.benchmark_data,
        "modelPerformanceData": db_post.model_performance_data
    }
    
    return response
