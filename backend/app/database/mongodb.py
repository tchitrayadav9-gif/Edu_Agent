"""
Database connection manager supporting MongoDB and JSON fallback storage.
Provides collection interfaces for users, student_profiles, memory, chat_history,
study_plans, interview_sessions, documents, evaluation_results, and agent_logs.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger("edumind.database")

# Local fallback file path
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
LOCAL_DB_FILE = os.path.join(DATA_DIR, "local_db.json")


class LocalCollection:
    """In-memory collection with JSON file persistence fallback."""
    def __init__(self, name: str, parent_db):
        self.name = name
        self.parent_db = parent_db

    def find(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        docs = self.parent_db.data.get(self.name, [])
        if not query:
            return [dict(d) for d in docs]
        
        result = []
        for doc in docs:
            match = True
            for k, v in query.items():
                if isinstance(v, dict) and "$in" in v:
                    if doc.get(k) not in v["$in"]:
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                result.append(dict(doc))
        return result

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        docs = self.find(query)
        return docs[0] if docs else None

    def insert_one(self, document: Dict[str, Any]):
        doc_copy = dict(document)
        if "_id" not in doc_copy and "id" in doc_copy:
            doc_copy["_id"] = doc_copy["id"]
        elif "_id" not in doc_copy:
            import uuid
            doc_copy["_id"] = str(uuid.uuid4())
            
        if self.name not in self.parent_db.data:
            self.parent_db.data[self.name] = []
        self.parent_db.data[self.name].append(doc_copy)
        self.parent_db.save()
        return doc_copy

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        docs = self.parent_db.data.get(self.name, [])
        updated = False
        for i, doc in enumerate(docs):
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                if "$set" in update:
                    doc.update(update["$set"])
                else:
                    doc.update(update)
                docs[i] = doc
                updated = True
                break
        
        if not updated and upsert:
            new_doc = dict(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            else:
                new_doc.update(update)
            self.insert_one(new_doc)
            
        self.parent_db.save()
        return {"matched_count": 1 if updated else 0, "upserted": not updated and upsert}

    def delete_one(self, query: Dict[str, Any]):
        docs = self.parent_db.data.get(self.name, [])
        initial_len = len(docs)
        self.parent_db.data[self.name] = [
            d for d in docs if not all(d.get(k) == v for k, v in query.items())
        ]
        deleted = initial_len - len(self.parent_db.data[self.name])
        self.parent_db.save()
        return {"deleted_count": deleted}

    def delete_many(self, query: Dict[str, Any]):
        return self.delete_one(query)

    def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        return len(self.find(query))


class FallbackDatabase:
    """Mock/Fallback MongoDB database that serializes to JSON."""
    def __init__(self, filepath: str = LOCAL_DB_FILE):
        self.filepath = filepath
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.load()

    def load(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load local db file: {e}. Starting fresh.")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        try:
            # Custom JSON serializer for dates/objects
            def default_serializer(o):
                if isinstance(o, datetime):
                    return o.isoformat()
                return str(o)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, default=default_serializer, indent=2)
        except Exception as e:
            logger.error(f"Failed to save local db: {e}")

    def __getitem__(self, collection_name: str) -> LocalCollection:
        return LocalCollection(collection_name, self)


class DatabaseManager:
    """Central database coordinator managing connection and collections."""
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGODB_DB_NAME", "edumind_db")
        self.client = None
        self.db = None
        self.is_connected = False
        self._init_connection()

    def _init_connection(self):
        try:
            # Try connecting to MongoDB with a 1.5-second timeout
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=1500)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_connected = True
            logger.info("Connected successfully to live MongoDB instance.")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB not reachable at {self.mongo_uri} ({e}). Using persistent Local JSON Database engine.")
            self.db = FallbackDatabase()
            self.is_connected = False

    def get_collection(self, name: str):
        if self.db is None:
            self._init_connection()
        return self.db[name]

    @property
    def users(self):
        return self.get_collection("users")

    @property
    def student_profiles(self):
        return self.get_collection("student_profiles")

    @property
    def skills(self):
        return self.get_collection("skills")

    @property
    def career_profiles(self):
        return self.get_collection("career_profiles")

    @property
    def study_plans(self):
        return self.get_collection("study_plans")

    @property
    def learning_progress(self):
        return self.get_collection("learning_progress")

    @property
    def documents(self):
        return self.get_collection("documents")

    @property
    def chat_history(self):
        return self.get_collection("chat_history")

    @property
    def memory(self):
        return self.get_collection("memory")

    @property
    def interview_sessions(self):
        return self.get_collection("interview_sessions")

    @property
    def interview_questions(self):
        return self.get_collection("interview_questions")

    @property
    def evaluation_results(self):
        return self.get_collection("evaluation_results")

    @property
    def agent_logs(self):
        return self.get_collection("agent_logs")

    @property
    def tool_calls(self):
        return self.get_collection("tool_calls")


# Singleton instance
db_manager = DatabaseManager()
