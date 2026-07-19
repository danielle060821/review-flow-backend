from fastapi import FastAPI, HTTPException, Depends
from datetime import date
from enums import Difficulty
from schemas import ProblemCreate, ProblemACUpdate, ProblemResponse
from database import Base, engine, get_db
from models import Problem
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
app = FastAPI()
Base.metadata.create_all(bind=engine)

problems = []
    
@app.post("/problems")
def create_problem(problem: ProblemCreate, session: Session=Depends(get_db)):
    problem_exist = session.scalar( select(Problem).where(Problem.title == problem.title))
    if problem_exist:
        raise HTTPException(
            status_code=409,
            detail="Problem already exists"
        )
    new_problem = Problem(
        title = problem.title,
        difficulty = problem.difficulty,
        category = problem.category,
        subcategory = problem.subcategory | None,
        last_ac_date = problem.last_ac_date
    )
    session.add(new_problem)
    session.commit()
    session.refresh(new_problem)
    return {
        "message" : "Problem received successfully!",
        "problem" : new_problem 
    }
    
@app.get("/problems")
def get_problems(session: Session=Depends(get_db)):
    all_problems = session.scalars(select(Problem)).all()
    response = []
    for problem in all_problems:
        problem_response = ProblemResponse(
            id = problem.id,
            title = problem.title,
            difficulty = problem.difficulty,
            category = problem.category,
            subcategory = problem.subcategory | None,
            last_ac_date = problem.last_ac_date
        )
        response.append(problem_response)
    return response

@app.patch("/problems/{title}")
def update_last_ac_date(title: str, new_ac_date: ProblemACUpdate, session: Session = Depends(get_db)):
    problem = session.scalar(select(Problem).where(Problem.title == title))
    if not problem:
        raise HTTPException(
        status_code=404,
        detail="Problem not found"
    )
    
    problem.last_ac_date = new_ac_date.last_ac_date
    session.commit()
    session.refresh(problem)
    return {
        "message": "Date updated successfully!", 
        "problem": problem
    }
    
        
@app.delete("/problems/{title}")
def delete_problem(title: str, session : Session = Depends(get_db)):
    problem = session.scalar(select(Problem).where(Problem.title == title))
    if not problem:
        raise HTTPException(
        status_code=404,
        detail="Problem not found"
    )
    
    session.delete(problem)
    session.commit()
    return {
        "message": "Problem deleted successfully!"
    }
    
   