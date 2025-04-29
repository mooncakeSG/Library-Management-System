from database import SessionLocal, engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy import text
import re

def test_connection():
    try:
        # Print database URL (hiding password)
        safe_url = re.sub(r':.*?@', ':***@', SQLALCHEMY_DATABASE_URL)
        print(f"Attempting to connect to: {safe_url}")
        
        # Test connection using engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Successfully connected to the database!")
            print("Test query result:", result.scalar())
            
        # Test session
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT 1"))
            print("✅ Successfully created a database session!")
            print("Session test query result:", result.scalar())
        finally:
            db.close()
            
    except Exception as e:
        print("❌ Failed to connect to the database!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_connection() 