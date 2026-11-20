from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel,Field
from database import get_connection

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int = Field(ge=3, le=25)


class StudentPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=3, le=25)


@app.get("/students")
def get_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentInfo")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentInfo WHERE id = %s", (student_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return row


@app.post("/students")
def create_student(student: Student):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO studentInfo (name, age) VALUES (%s, %s)",
        (student.name, student.age),
    )
    conn.commit()
    conn.close()
    return {"message": "Student added"}


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE studentInfo SET name = %s, age = %s WHERE id = %s",
        (student.name, student.age, student_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM studentInfo WHERE id = %s", (student_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

@app.patch("/students/{student_id}")
def patch_student(student_id: int, student: StudentPatch):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE studentInfo SET "
        "name = COALESCE(%s, name), "
        "age = COALESCE(%s, age) "
        "WHERE id = %s",
        (student.name, student.age, student_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated"}