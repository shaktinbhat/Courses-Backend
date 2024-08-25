import json
from pymongo import MongoClient, ASCENDING, DESCENDING

# Read data from courses.json file
with open('courses.json') as file:
    courses_data = json.load(file)

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.courses_db

# Create collections
courses_collection = db.courses
chapters_collection = db.chapters

# Create indices for efficient retrieval
courses_collection.create_index([('name', ASCENDING)])
courses_collection.create_index([('date', DESCENDING)])
courses_collection.create_index([('rating', DESCENDING)])

# Insert course and chapter data
for course in courses_data:
    course_id = courses_collection.insert_one({
        "name": course["name"],
        "date": course["date"],
        "description": course["description"],
        "domain": course["domain"],
        "rating": 0,  # Initialize rating
        "total_votes": 0
    }).inserted_id

    for chapter in course["chapters"]:
        chapters_collection.insert_one({
            "course_id": course_id,
            "name": chapter["name"],
            "text": chapter["text"],
            "rating": 0,
            "total_votes": 0
        })

print("Data insertion completed.")
