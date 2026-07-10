from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
from enum import Enum
app = FastAPI()

problems = []
class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    
class ProblemCreate(BaseModel):
    title : str
    difficulty: Difficulty
    category: str
    subcategory: str
    last_ac_date: date

class ProblemACUpdate(BaseModel):
    last_ac_date: date

   
@app.post("/problems")
def create_problem(problem: ProblemCreate):
    for p in problems:
        if problem.title.lower() == p.title.lower():
            raise HTTPException(
                status_code=409,
                detail="Problem already exists"
            )
    problems.append(problem)
    return {
        "message" : "Problem received successfully!",
        "problem" : problem 
    }
    
@app.get("/problems")
def get_problems():
    return problems

@app.patch("/problems")
def update_last_ac_date(title: str, update: ProblemACUpdate):
    for p in problems:
        if p.title == title:
            p.last_ac_date = update.last_ac_date
            return {
                "message": "Date updated successfully!", 
                "problem": p
            }
    raise HTTPException(
        status_code=404,
        detail="Problem not found"
    )
        
@app.delete("/problems/{title}")
def delete_problem(title: str):
    for p in problems:
        if p.title == title:
            problems.remove(p)
            return {
                "message": "Problem deleted successfully!"
            }
    raise HTTPException(
        status_code=404,
        detail="Problem not found"
    )
    
review_intervals = {
    Difficulty.easy : 20,
    Difficulty.medium : 10,
    Difficulty.hard : 5
}   
@app.get("/reviews")
def get_reviews():
    due_problems = []
    for p in problems:
        days_since_ac = (date.today() - p.last_ac_date).days
        required_interval = review_intervals[p.difficulty]
        if days_since_ac >= required_interval:
            due_problems.append(p)
    return due_problems