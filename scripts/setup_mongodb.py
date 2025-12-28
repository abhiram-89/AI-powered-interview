"""
MongoDB Database Setup Script
Creates collections and indexes for the AI Interview Assistant
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import os

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ai_interviews"

def setup_database():
    """Initialize MongoDB collections and indexes"""
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print(f"Connected to MongoDB: {DATABASE_NAME}")
    
    # Collections
    collections = {
        "interviews": {
            "indexes": [
                ("created_at", DESCENDING),
                ("candidate_email", ASCENDING),
                ("status", ASCENDING)
            ]
        },
        "questions": {
            "indexes": [
                ("role", ASCENDING),
                ("difficulty", ASCENDING),
                ("skill", ASCENDING)
            ]
        },
        "responses": {
            "indexes": [
                ("interview_id", ASCENDING),
                ("question_id", ASCENDING),
                ("created_at", DESCENDING)
            ]
        },
        "evaluations": {
            "indexes": [
                ("interview_id", ASCENDING),
                ("created_at", DESCENDING)
            ]
        }
    }
    
    # Create collections and indexes
    for collection_name, config in collections.items():
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
        
        collection = db[collection_name]
        for index in config["indexes"]:
            collection.create_index([index])
            print(f"Created index on {collection_name}: {index[0]}")
    
    # Seed sample questions
    questions_collection = db["questions"]
    if questions_collection.count_documents({}) == 0:
        sample_questions = [
            {
                "role": "Frontend Developer",
                "skill": "React",
                "difficulty": "intermediate",
                "question": "Explain the difference between controlled and uncontrolled components in React.",
                "topics": ["React", "Components", "State Management"],
                "created_at": datetime.utcnow()
            },
            {
                "role": "Frontend Developer",
                "skill": "JavaScript",
                "difficulty": "intermediate",
                "question": "What are closures in JavaScript and how are they useful?",
                "topics": ["JavaScript", "Closures", "Scope"],
                "created_at": datetime.utcnow()
            },
            {
                "role": "Backend Developer",
                "skill": "Python",
                "difficulty": "intermediate",
                "question": "Explain the difference between async/await and threading in Python.",
                "topics": ["Python", "Async", "Concurrency"],
                "created_at": datetime.utcnow()
            },
            {
                "role": "Backend Developer",
                "skill": "APIs",
                "difficulty": "intermediate",
                "question": "What are the key differences between REST and GraphQL APIs?",
                "topics": ["APIs", "REST", "GraphQL"],
                "created_at": datetime.utcnow()
            },
            {
                "role": "Full Stack Developer",
                "skill": "System Design",
                "difficulty": "advanced",
                "question": "How would you design a scalable real-time chat application?",
                "topics": ["System Design", "Scalability", "WebSockets"],
                "created_at": datetime.utcnow()
            }
        ]
        
        questions_collection.insert_many(sample_questions)
        print(f"Seeded {len(sample_questions)} sample questions")
    
    # Setup ai_interviews database with reports collection
    ai_interviews_db = client["ai_interviews"]
    
    reports_collection_name = "reports"
    if reports_collection_name not in ai_interviews_db.list_collection_names():
        ai_interviews_db.create_collection(reports_collection_name)
        print(f"Created collection: {reports_collection_name} in ai_interviews database")
    
    reports_collection = ai_interviews_db[reports_collection_name]
    # Create indexes for reports collection
    reports_collection.create_index([("interview_id", ASCENDING)])
    reports_collection.create_index([("generated_at", DESCENDING)])
    reports_collection.create_index([("candidate_email", ASCENDING)])
    print("Created indexes on reports collection")
    
    print("Database setup complete!")
    client.close()

if __name__ == "__main__":
    setup_database()
