from pymongo import MongoClient
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    logger.info("✅ MongoDB connection successful")
    
    db = client["janta_voice"]
    complaints_collection = db["complaints"]
    users_collection = db["users"]    
    
    # Test if we can access the collection
    complaints_collection.find_one()
    logger.info("✅ Database and collection access successful")
    
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    logger.error("Please make sure MongoDB is running on localhost:27017")
    
    # Create fallback collections for testing
    complaints_collection = None
    logger.warning("⚠️  Using fallback mode - complaints will not be saved to database")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")