from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON, Boolean, Enum as SQLEnum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum
from datetime import datetime

class UserRole(enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    author = Column(String, nullable=False)  # Keep for backward compatibility
    author_id = Column(String, ForeignKey("users.id"), nullable=True)  # Link to user
    excerpt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default="published")  # draft, published, archived
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    benchmark_data = Column(JSON, nullable=True)  # Store as JSON
    model_performance_data = Column(JSON, nullable=True)  # Store as JSON
    tags = Column(JSON, nullable=True)  # Post tags for categorization
    views_count = Column(Integer, default=0)  # Track post views
    likes_count = Column(Integer, default=0)  # Track post likes
    
    # Relationships
    author_user = relationship("User", back_populates="blog_posts")

class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model = Column(String, nullable=False)
    wer = Column(Float, nullable=False)
    dataset = Column(String, nullable=False)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    preferences = Column(JSON, nullable=True)  # User preferences/settings
    
    # Relationships
    blog_posts = relationship("BlogPost", back_populates="author_user")
    audit_logs = relationship("AuditLog", back_populates="user")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)  # login, create_post, delete_user, etc.
    resource_type = Column(String(50), nullable=True)  # user, post, file, etc.
    resource_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)  # Additional context
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class DashboardData(Base):
    __tablename__ = "dashboard_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    audio_file_name = Column(String, nullable=False)
    audio_length = Column(Float, nullable=False)
    model = Column(String, nullable=False)
    ground_truth = Column(Text, nullable=False)
    transcription = Column(Text, nullable=False)
    wer_score = Column(Float, nullable=False)
    inference_time = Column(Float, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())