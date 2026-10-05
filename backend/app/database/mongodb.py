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

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger("edumind.database")

# Local fallback file path
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
LOCAL_DB_FILE = os.path.join(DATA_DIR, "local_db.json")


class LocalCollection:
    """In-memory collection with JSON file persistence fallback."""
    def __init__(self, name: str, parent_db):
        self.name = name
        self.parent_db = parent_db

    def _apply_projection(self, doc: Dict[str, Any], projection: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not projection or not isinstance(projection, dict):
            return dict(doc)
        # Inclusion projection e.g. {'username': 1, 'email': 1}
        has_inclusions = any(v == 1 or v is True for v in projection.values() if v not in (0, False))
        if has_inclusions:
            result = {}
            if projection.get("_id", 1) != 0 and "_id" in doc:
                result["_id"] = doc["_id"]
            for k, v in projection.items():
                if (v == 1 or v is True) and k in doc:
                    result[k] = doc[k]
            return result
        else:
            # Exclusion projection
            result = dict(doc)
            for k, v in projection.items():
                if (v == 0 or v is False) and k in result:
                    result.pop(k, None)
            return result

    def find(self, query: Optional[Dict[str, Any]] = None, projection: Optional[Dict[str, Any]] = None, *args, **kwargs) -> List[Dict[str, Any]]:
        docs = self.parent_db.data.get(self.name, [])
        if not query:
            return [self._apply_projection(d, projection) for d in docs]
        
        result = []
        for doc in docs:
            match = True
            for k, v in query.items():
                if k == "$or" and isinstance(v, list):
                    or_match = any(all(doc.get(sub_k) == sub_v for sub_k, sub_v in condition.items()) for condition in v)
                    if not or_match:
                        match = False
                        break
                elif isinstance(v, dict) and "$in" in v:
                    if doc.get(k) not in v["$in"]:
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                result.append(self._apply_projection(doc, projection))
        return result

    def find_one(self, query: Optional[Dict[str, Any]] = None, projection: Optional[Dict[str, Any]] = None, *args, **kwargs) -> Optional[Dict[str, Any]]:
        docs = self.find(query, projection)
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


class MongoCollectionWrapper:
    """Wrapper around a PyMongo collection that converts ObjectId fields to strings for FastAPI/Pydantic."""
    def __init__(self, collection):
        self._col = collection

    def _convert_query_ids(self, query):
        if not isinstance(query, dict):
            return query
        from bson import ObjectId
        new_q = {}
        for k, v in query.items():
            if k == "_id" and isinstance(v, str) and ObjectId.is_valid(v):
                new_q[k] = ObjectId(v)
            elif isinstance(v, dict):
                new_q[k] = self._convert_query_ids(v)
            else:
                new_q[k] = v
        return new_q

    def _sanitize(self, doc):
        if doc is None:
            return None
        if isinstance(doc, dict):
            clean = {}
            for k, v in doc.items():
                if k == "_id":
                    clean["_id"] = str(v)
                elif isinstance(v, dict):
                    clean[k] = self._sanitize(v)
                elif isinstance(v, list):
                    clean[k] = [self._sanitize(item) if isinstance(item, dict) else (str(item) if hasattr(item, "generation_time") else item) for item in v]
                elif hasattr(v, "generation_time"):  # Check if ObjectId
                    clean[k] = str(v)
                else:
                    clean[k] = v
            return clean
        return doc

    def find(self, filter=None, *args, **kwargs):
        filter = self._convert_query_ids(filter) if filter else {}
        cursor = self._col.find(filter, *args, **kwargs)
        return [self._sanitize(doc) for doc in cursor]

    def find_one(self, filter=None, *args, **kwargs):
        filter = self._convert_query_ids(filter) if filter else {}
        doc = self._col.find_one(filter, *args, **kwargs)
        return self._sanitize(doc)

    def insert_one(self, doc, *args, **kwargs):
        res = self._col.insert_one(doc, *args, **kwargs)
        if isinstance(doc, dict):
            if "_id" in doc and (hasattr(doc["_id"], "generation_time") or not isinstance(doc["_id"], (str, int, float, bool))):
                doc["_id"] = str(doc["_id"])
        return res

    def insert_many(self, docs, *args, **kwargs):
        res = self._col.insert_many(docs, *args, **kwargs)
        for doc in docs:
            if isinstance(doc, dict):
                if "_id" in doc and (hasattr(doc["_id"], "generation_time") or not isinstance(doc["_id"], (str, int, float, bool))):
                    doc["_id"] = str(doc["_id"])
        return res

    def update_one(self, filter, update, *args, **kwargs):
        filter = self._convert_query_ids(filter)
        return self._col.update_one(filter, update, *args, **kwargs)

    def update_many(self, filter, update, *args, **kwargs):
        filter = self._convert_query_ids(filter)
        return self._col.update_many(filter, update, *args, **kwargs)

    def delete_one(self, filter, *args, **kwargs):
        filter = self._convert_query_ids(filter)
        return self._col.delete_one(filter, *args, **kwargs)

    def delete_many(self, filter, *args, **kwargs):
        filter = self._convert_query_ids(filter)
        return self._col.delete_many(filter, *args, **kwargs)

    def count_documents(self, filter=None, *args, **kwargs):
        filter = self._convert_query_ids(filter) if filter else {}
        return self._col.count_documents(filter, *args, **kwargs)

    def aggregate(self, *args, **kwargs):
        cursor = self._col.aggregate(*args, **kwargs)
        return [self._sanitize(doc) for doc in cursor]

    def __getattr__(self, name):
        return getattr(self._col, name)


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
        # Configure public DNS servers to resolve MongoDB SRV cluster records rapidly
        try:
            import dns.resolver
            res = dns.resolver.Resolver()
            res.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
            dns.resolver.default_resolver = res
        except Exception:
            pass

        try:
            # Try connecting to MongoDB with a 5-second timeout
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_connected = True
            logger.info(f"Connected successfully to live MongoDB instance ({self.db_name}).")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB not reachable at {self.mongo_uri[:35]}... ({e}). Using persistent Local JSON Database engine.")
            self.db = FallbackDatabase()
            self.is_connected = False

    def get_collection(self, name: str):
        if self.db is None:
            self._init_connection()
        if self.is_connected and self.db is not None:
            return MongoCollectionWrapper(self.db[name])
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
