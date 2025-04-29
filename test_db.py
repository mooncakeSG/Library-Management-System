from database import engine
from sqlalchemy import text

try:
    # Test the connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        
        # Test querying the tables
        result = connection.execute(text("SHOW TABLES"))
        print("\nAvailable tables:")
        for row in result:
            print(row[0])
            
except Exception as e:
    print(f"Error connecting to database: {e}") 