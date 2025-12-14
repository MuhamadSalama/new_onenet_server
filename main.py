import os
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the core package
from onenet_core.main import create_app
from onenet_core.database import Base, get_db
from onenet_core.models import User, Role, Permission
from dotenv import load_dotenv
load_dotenv()

# Consumer owns the database configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "onenet_db")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@asynccontextmanager
async def lifespan(app):
    """Startup and shutdown events"""
    # Startup: Create tables and seed data
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Seed initial data
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        if not existing_admin:
            print("Seeding initial data...")
            
            # Step 1: Create Permissions (in order)
            permissions = [
                Permission(name="user:create", description="Create new users", category="user_management"),
                Permission(name="user:read", description="View user information", category="user_management"),
                Permission(name="user:update", description="Update users", category="user_management"),
                Permission(name="user:delete", description="Delete users", category="user_management"),
                Permission(name="wallet:read", description="View wallet information", category="wallet"),
                Permission(name="wallet:transfer", description="Perform wallet transfers", category="wallet"),
                Permission(name="role:read", description="View roles", category="role_management"),
                Permission(name="role:create", description="Create roles", category="role_management"),
                Permission(name="role:assign", description="Assign roles to users", category="role_management"),
                Permission(name="admin:panel", description="Access admin panel", category="admin"),
                Permission(name="risk:console", description="Access risk console", category="admin"),
            ]
            
            for perm in permissions:
                db.add(perm)
            db.commit()
            print(f"Created {len(permissions)} permissions")
            
            # Step 2: Create Roles and assign permissions
            # Admin role - all permissions
            admin_role = Role(name="admin", description="Administrator with full access")
            admin_perms = db.query(Permission).all()
            admin_role.permissions = admin_perms
            db.add(admin_role)
            
            # Manager role - elevated permissions
            manager_role = Role(name="manager", description="Manager with elevated permissions")
            manager_perm_names = ["user:read", "user:create", "user:update", "wallet:read", "wallet:transfer", "role:read"]
            manager_perms = db.query(Permission).filter(Permission.name.in_(manager_perm_names)).all()
            manager_role.permissions = manager_perms
            db.add(manager_role)
            
            # User role - basic permissions
            user_role = Role(name="user", description="Standard user role")
            user_perm_names = ["user:read", "wallet:read", "wallet:transfer"]
            user_perms = db.query(Permission).filter(Permission.name.in_(user_perm_names)).all()
            user_role.permissions = user_perms
            db.add(user_role)
            
            db.commit()
            print("Created 3 roles with assigned permissions")
            
            # Step 3: Create Users and assign roles
            # Admin  user
            admin_user = User(
                email="admin@example.com",
                name="Admin User",
                password_hash="admin123",  # Note: In production, hash this!
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=60),
            )
            admin_user.roles = [admin_role, manager_role]
            db.add(admin_user)
            
            # Demo user
            demo_user = User(
                email="demo@example.com",
                name="Demo User",
                password_hash="demo123",
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=30),
            )
            demo_user.roles = [user_role]
            db.add(demo_user)
            
            db.commit()
            print("Created 2 users (admin@example.com and demo@example.com)")
            print("Seeding complete!")
        else:
            print("Database already seeded, skipping...")
    finally:
        db.close()
    
    yield  # App runs here
    
    # Shutdown
    print("Shutting down...")

# Real database dependency for the consumer
def get_real_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the FastAPI app
app = create_app()
app.router.lifespan_context = lifespan

# Override the stub dependency with the real database connection
app.dependency_overrides[get_db] = get_real_db

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://localhost:8001")
    print("Login credentials:")
    print("  Admin: admin@example.com / admin123")
    print("  Demo:  demo@example.com / demo123")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
