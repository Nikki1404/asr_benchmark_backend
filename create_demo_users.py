"""
Seed script for creating demo users in the database
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, UserRole, UserStatus, Base
from auth import AuthService
from datetime import datetime

# Create database tables
Base.metadata.create_all(bind=engine)

def create_demo_users():
    """Create demo users for testing"""
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@demo.com").first()
        if existing_admin:
            print("Demo users already exist!")
            return

        # Create demo users
        demo_users = [
            {
                "username": "admin_user",
                "email": "admin@demo.com",
                "password": "password123",
                "full_name": "System Administrator",
                "role": UserRole.ADMIN,
                "bio": "System administrator with full access to all features."
            },
            {
                "username": "editor_user", 
                "email": "editor@demo.com",
                "password": "password123",
                "full_name": "Content Editor",
                "role": UserRole.EDITOR,
                "bio": "Content editor with publish and analysis permissions."
            },
            {
                "username": "viewer_user",
                "email": "viewer@demo.com", 
                "password": "password123",
                "full_name": "Data Viewer",
                "role": UserRole.VIEWER,
                "bio": "Viewer with read-only access to published content."
            }
        ]

        for user_data in demo_users:
            # Truncate password to 72 bytes for bcrypt
            password = user_data["password"][:72]
            hashed_password = AuthService.get_password_hash(password)
            
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                bio=user_data["bio"],
                hashed_password=hashed_password,
                role=user_data["role"],
                status=UserStatus.ACTIVE,
                is_email_verified=True,
                created_at=datetime.utcnow(),
                preferences={"theme": "light", "email_notifications": True}
            )
            
            db.add(db_user)

        db.commit()
        print("Demo users created successfully!")
        print("- Admin: admin@demo.com / password123")
        print("- Editor: editor@demo.com / password123") 
        print("- Viewer: viewer@demo.com / password123")

    except Exception as e:
        print(f"Error creating demo users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_users()