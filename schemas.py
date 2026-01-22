from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import UserRole, UserStatus

# Blog Post schemas
class BenchmarkResultSchema(BaseModel):
    """Individual benchmark result for a model on a specific dataset"""
    model: str = Field(..., description="Name of the ASR model tested", example="Whisper-large")
    wer: float = Field(..., description="Word Error Rate as a decimal (0.0 = perfect, 1.0 = completely wrong)", ge=0.0, le=1.0, example=0.123)
    dataset: str = Field(..., description="Name of the dataset used for testing", example="LibriSpeech-clean")

class ModelPerformanceDataSchema(BaseModel):
    """Aggregated performance metrics for a model across multiple tests"""
    model: str = Field(..., description="Name of the ASR model", example="Whisper-large")
    avgWer: float = Field(..., description="Average Word Error Rate across all tests", ge=0.0, le=1.0, example=0.145)

class BlogPostBase(BaseModel):
    """Base schema for blog post data"""
    title: str = Field(..., description="Blog post title", min_length=5, max_length=200, example="Whisper vs Traditional STT: Comprehensive Benchmark Analysis")
    author: str = Field(..., description="Author name", min_length=2, max_length=100, example="ASR Research Team")
    excerpt: str = Field(..., description="Brief summary/excerpt of the blog post", min_length=10, max_length=500, example="An in-depth comparison of OpenAI's Whisper model against traditional speech-to-text solutions...")
    content: str = Field(..., description="Full HTML content of the blog post", min_length=50, example="<h2>Executive Summary</h2><p>This analysis examines...</p>")
    benchmark_data: Optional[List[BenchmarkResultSchema]] = Field(None, description="Array of benchmark results associated with this post")
    model_performance_data: Optional[List[ModelPerformanceDataSchema]] = Field(None, description="Array of model performance summaries")

class BlogPostCreate(BlogPostBase):
    """Schema for creating a new blog post"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Whisper vs Traditional STT: Comprehensive Benchmark Analysis",
                "author": "ASR Research Team",
                "excerpt": "An in-depth comparison of OpenAI's Whisper model against traditional speech-to-text solutions, analyzing accuracy, speed, and resource consumption.",
                "content": "<h2>Executive Summary</h2><p>This comprehensive analysis examines the performance characteristics of OpenAI's Whisper model compared to traditional speech-to-text solutions.</p>",
                "benchmark_data": [
                    {"model": "Whisper-large", "wer": 0.123, "dataset": "LibriSpeech-clean"},
                    {"model": "Traditional-STT", "wer": 0.187, "dataset": "LibriSpeech-clean"}
                ],
                "model_performance_data": [
                    {"model": "Whisper-large", "avgWer": 0.145},
                    {"model": "Traditional-STT", "avgWer": 0.204}
                ]
            }
        }

class BlogPostResponse(BlogPostBase):
    """Schema for blog post responses including system-generated fields"""
    id: str = Field(..., description="Unique identifier for the blog post", example="550e8400-e29b-41d4-a716-446655440000")
    date: datetime = Field(..., description="Publication date and time", example="2025-12-04T10:30:00Z")

    class Config:
        from_attributes = True

# Dashboard Data schemas
class DashboardDataRow(BaseModel):
    audio_file_name: str = None
    audio_length: float = None
    model: str = None
    ground_truth: str = None
    transcription: str = None
    wer_score: float = None
    inference_time: float = None
    
    class Config:
        # Allow field names with different cases
        populate_by_name = True
        # Define field aliases for the exact frontend field names
        fields = {
            'audio_file_name': 'Audio File Name',
            'audio_length': 'Audio Length', 
            'model': 'Model',
            'ground_truth': 'Ground_truth',
            'transcription': 'Transcription',
            'wer_score': 'WER Score',
            'inference_time': 'Inference time (in sec)'
        }

class FileUploadResponse(BaseModel):
    """Response schema for file upload processing"""
    data: List[dict] = Field(..., description="Processed benchmark data from uploaded file")
    message: str = Field(default="File processed successfully", description="Processing status message", example="Successfully processed 150 rows from benchmark_results.xlsx")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "Audio File Name": "sample_001.wav",
                        "Audio Length": 12.5,
                        "Model": "Whisper-large",
                        "Ground_truth": "hello world this is a test",
                        "Transcription": "hello world this is a test",
                        "WER Score": 0.0,
                        "Inference time (in sec)": 2.3
                    }
                ],
                "message": "Successfully processed 150 rows from benchmark_results.xlsx"
            }
        }

# AI Service schemas
class SummarizeRequest(BaseModel):
    """Request schema for text summarization"""
    content: str = Field(..., description="Text content to summarize", min_length=10, example="This is a detailed analysis of ASR model performance showing that Whisper achieves superior accuracy with 12.3% WER compared to traditional models at 18.7% WER, though with increased computational requirements.")

class SummarizeResponse(BaseModel):
    """Response schema for text summarization"""
    summary: str = Field(..., description="AI-generated concise summary", example="Whisper outperforms traditional ASR models with 12.3% vs 18.7% WER, but requires more computational resources.")

class BlogGenerationData(BaseModel):
    """Input data for AI blog post generation"""
    summaryStats: dict = Field(..., description="Overall benchmark statistics", example={"totalFiles": 150, "avgWer": 0.156, "avgInferenceTime": 2.34})
    modelPerformance: List[dict] = Field(..., description="Per-model performance data", example=[{"model": "Whisper", "avgWer": 0.123, "avgInferenceTime": 3.2}])
    fileName: str = Field(..., description="Source file name for context", example="benchmark_results_2025.xlsx")

class BlogPostOutput(BaseModel):
    """AI-generated blog post output"""
    title: str = Field(..., description="Generated blog post title", example="Comprehensive ASR Benchmark Analysis: Whisper vs Traditional Models")
    excerpt: str = Field(..., description="Generated excerpt/summary", example="Latest benchmarking reveals significant accuracy improvements with modern transformer-based ASR models.")
    content: str = Field(..., description="Full HTML blog post content", example="<h2>Executive Summary</h2><p>Our comprehensive analysis...</p>")

class AnalyzeErrorsRequest(BaseModel):
    """Request schema for transcription error analysis"""
    ground_truth: str = Field(..., description="Correct transcription text", example="The quick brown fox jumps over the lazy dog")
    transcription: str = Field(..., description="ASR model output to analyze", example="The quick brown fox jumps over the lady dog")

class TranscriptionError(BaseModel):
    """Individual transcription error details"""
    type: str = Field(..., description="Error type", enum=["Substitution", "Deletion", "Insertion"], example="Substitution")
    ground_truth_segment: str = Field(..., description="Correct text segment", example="lazy")
    transcription_segment: str = Field(..., description="Transcribed text segment", example="lady")

class AnalysisResult(BaseModel):
    """Transcription error analysis results"""
    summary: str = Field(..., description="Overall quality assessment", example="High accuracy transcription with 1 substitution error affecting word recognition.")
    errors: List[TranscriptionError] = Field(..., description="Detailed error breakdown")

class CompareModelsRequest(BaseModel):
    """Request schema for model comparison"""
    model_a: dict = Field(..., description="First model data with name and benchmark results", example={"name": "Whisper", "data": [{"WER Score": 0.12, "Inference time (in sec)": 3.2}]})
    model_b: dict = Field(..., description="Second model data with name and benchmark results", example={"name": "Traditional STT", "data": [{"WER Score": 0.18, "Inference time (in sec)": 1.8}]})

class HeadToHeadAnalysis(BaseModel):
    """Head-to-head model comparison results"""
    winner: str = Field(..., description="Overall winning model", example="Whisper")
    summary: str = Field(..., description="Executive summary of comparison", example="Whisper demonstrates superior accuracy but with increased computational requirements.")
    accuracyAnalysis: str = Field(..., description="Detailed accuracy comparison", example="Whisper achieves 12% WER vs Traditional STT's 18% WER, representing a 33% improvement in accuracy.")
    speedAnalysis: str = Field(..., description="Performance and speed analysis", example="Traditional STT processes audio 1.8x faster but at the cost of accuracy.")

# ===== USER & AUTHENTICATION SCHEMAS =====

class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full display name")
    bio: Optional[str] = Field(None, max_length=500, description="User biography")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    confirm_password: str = Field(..., description="Password confirmation")

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")

class UserAdminUpdate(UserUpdate):
    """Schema for admin user updates"""
    role: Optional[UserRole] = Field(None, description="User role")
    status: Optional[UserStatus] = Field(None, description="User status")

class UserResponse(UserBase):
    """Schema for user responses"""
    id: str
    role: UserRole
    status: UserStatus
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    is_email_verified: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login"""
    username_or_email: str = Field(..., description="Username or email address")
    password: str = Field(..., description="User password")

class TokenResponse(BaseModel):
    """Schema for token responses"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    """Schema for token refresh"""
    refresh_token: str

class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

# ===== AUDIT LOG SCHEMAS =====

class AuditLogResponse(BaseModel):
    """Schema for audit log responses"""
    id: str
    user_id: Optional[str]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ===== ADMIN SCHEMAS =====

class SystemStatsResponse(BaseModel):
    """Schema for system statistics"""
    total_users: int
    active_users: int
    total_posts: int
    total_uploads: int
    recent_activities: List[AuditLogResponse]
    user_growth: List[Dict[str, Any]]
    popular_models: List[Dict[str, Any]]
    tradeOffs: str = Field(..., description="Trade-off analysis and recommendations", example="Choose Whisper for batch processing where accuracy is critical; use Traditional STT for real-time applications.")