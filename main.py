from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.courses_db
courses_collection = db.courses
chapters_collection = db.chapters

# Pydantic Models
class Course(BaseModel):
    name: str
    date: int
    description: str
    domain: List[str]
    rating: int
    total_votes: int

class Chapter(BaseModel):
    course_id: str
    name: str
    text: str
    rating: int
    total_votes: int

# Endpoints

@app.get("/courses")
def get_courses(sort_by: Optional[str] = 'name', domain: Optional[List[str]] = Query(None)):
    query = {}
    if domain:
        query['domain'] = {"$in": domain}

    sort_field = {
        'name': ('name', ASCENDING),
        'date': ('date', DESCENDING),
        'rating': ('rating', DESCENDING)
    }.get(sort_by, ('name', ASCENDING))

    courses = list(courses_collection.find(query).sort(*sort_field))
    return courses

@app.get("/courses/{course_id}")
def get_course_overview(course_id: str):
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/courses/{course_id}/chapters/{chapter_id}")
def get_chapter_info(course_id: str, chapter_id: str):
    chapter = chapters_collection.find_one({"_id": ObjectId(chapter_id), "course_id": ObjectId(course_id)})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.post("/courses/{course_id}/chapters/{chapter_id}/rate")
def rate_chapter(course_id: str, chapter_id: str, rating: int):
    if rating not in [1, -1]:
        raise HTTPException(status_code=400, detail="Invalid rating")

    chapter = chapters_collection.find_one({"_id": ObjectId(chapter_id), "course_id": ObjectId(course_id)})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Update chapter rating
    new_rating = chapter['rating'] + rating
    total_votes = chapter['total_votes'] + 1
    chapters_collection.update_one(
        {"_id": ObjectId(chapter_id)},
        {"$set": {"rating": new_rating, "total_votes": total_votes}}
    )

    # Update course rating
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    new_course_rating = course['rating'] + rating
    course_votes = course['total_votes'] + 1
    courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"rating": new_course_rating, "total_votes": course_votes}}
    )

    return {"message": "Rating submitted successfully"}
