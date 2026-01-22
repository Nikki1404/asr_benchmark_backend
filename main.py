from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

from database import engine, SessionLocal, Base
from api import posts, benchmarks, ai_services
import seed_data

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ASR Benchmark Hub API",
    description="""
    ## ASR Benchmark Hub Backend API
    
    A comprehensive REST API for managing ASR (Automatic Speech Recognition) benchmark data, 
    blog posts, and AI-powered analysis services.
    
    ### Features
    - **Blog Management**: Create, read, and manage ASR benchmark blog posts
    - **File Processing**: Upload and process Excel benchmark data files
    - **AI Services**: Powered by Google Gemini AI for content generation and analysis
    - **Data Analysis**: Comprehensive benchmark statistics and model comparisons
    
    ### API Categories
    - **Blog Posts**: Manage benchmark reports and analysis articles
    - **Benchmarks**: Upload and process ASR benchmark data files
    - **AI Services**: Generate summaries, reports, and perform error analysis
    
    ### Authentication
    AI services require a valid Google Gemini API key configured in the environment.
    
    ### Data Formats
    - Blog posts support rich HTML content with embedded benchmark data
    - Excel uploads must follow the specified column format
    - All responses follow consistent JSON schemas
    """,
    version="1.0.0",
    root_path="/apps",
    openapi_url="/docs/openai.json",
    contact={
        "name": "ASR Benchmark Hub",
        "url": "https://github.com/yourusername/asr-benchmark-hub"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Blog Posts",
            "description": "Operations for managing ASR benchmark blog posts and reports"
        },
        {
            "name": "Benchmarks", 
            "description": "File upload and processing operations for benchmark data"
        },
        {
            "name": "AI Services",
            "description": "AI-powered content generation and analysis services using Google Gemini"
        }
    ]
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API routers
from api import users
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(benchmarks.router, prefix="/api/benchmarks", tags=["benchmarks"])
app.include_router(ai_services.router, prefix="/api/ai", tags=["ai"])
app.include_router(users.router, prefix="/api/auth", tags=["authentication", "users"])

@app.on_event("startup")
async def startup_event():
    """Seed the database with initial data if it's empty"""
    db = SessionLocal()
    try:
        seed_data.seed_database(db)
    finally:
        db.close()

@app.get(
    "/",
    summary="API Root",
    description="Get basic API information and status",
    response_description="API welcome message and version info",
    tags=["System"]
)
async def root():
    """
    API root endpoint providing basic information about the ASR Benchmark Hub API.
    
    Returns:
    - API name and version
    - Basic status information
    """
    return {
        "message": "ASR Benchmark Hub API", 
        "version": "1.0.0",
        "description": "Backend API for ASR benchmark data management and AI analysis",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get(
    "/health",
    summary="Health Check",
    description="Check API health and database connectivity", 
    response_description="System health status",
    tags=["System"]
)
async def health_check():
    """
    Health check endpoint for monitoring and uptime verification.
    
    Returns:
    - System health status
    - API availability confirmation
    
    Use this endpoint for:
    - Load balancer health checks
    - Monitoring system integration
    - Service availability verification
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3019, reload=True)
