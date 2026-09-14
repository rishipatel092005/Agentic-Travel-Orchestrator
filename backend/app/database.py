"""
MongoDB database connection and management.
Provides access to collections without connecting on every request.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    """
    Singleton database connection handler.
    Manages MongoDB collections for the application.
    """
    
    _instance: Optional["Database"] = None
    _client: Optional[MongoClient] = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection."""
        if self._client is None:
            try:
                self._client = MongoClient(
                    settings.mongodb_uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000
                )
                # Test the connection
                self._client.admin.command("ping")
                self._db = self._client[settings.database_name]
                logger.info(f"Connected to MongoDB: {settings.database_name}")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.warning(f"MongoDB connection failed: {e}. Running in offline mode.")
                self._db = None
    
    @property
    def users_collection(self):
        """Get the users collection."""
        if self._db is None:
            raise RuntimeError("Database connection not available")
        return self._db["users"]
    
    @property
    def trips_collection(self):
        """Get the trips collection."""
        if self._db is None:
            raise RuntimeError("Database connection not available")
        return self._db["trips"]
    
    @property
    def itineraries_collection(self):
        """Get the itineraries collection."""
        if self._db is None:
            raise RuntimeError("Database connection not available")
        return self._db["itineraries"]
    
    def close(self):
        """Close the database connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Database connection closed")
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._db is not None


# Global database instance
db = Database()
