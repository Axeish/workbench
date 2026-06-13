import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from wb_backend.app.db import get_connection
from wb_backend.app.models import TaskStatus,TaskCreate, TaskUpdate, VALID_TRANSACTION

router = APIRouter(prefix='/api')



@router.get('/task')
def list_tasks(
        status: Optional[TaskStatus] = Query(None, description="Filter by status"),
        area_id: Optional[str] = Query(None,Dewxription="Filter by area"),
        project_id: Optional[str] = Query(None, description = "Filter by Project"),
):
    conn = get_connection()
    query ="SELECT * FROM tasks WHERE 1=1"
    params =[]

    if status:
        query+= " AND status = ?"
        params.append(status.value)
    if area_id:
        query+= " AND area_id = ?"
        params.append(area_id)
    if project_id:
        query+= " AND project_id =?"
        params.append(project_id)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [_row_to_task(row) for row in rows]

@router.posts("/tasks", status_code = 201)
def create_task(task: TaskCreate):
    conn = get_connection()

    area= conn.execute("SELECT id FROM areas WHERE id = ?", (task.area_id,)).fetchone()
    if not area:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Area '{task.area_id}' not found")

    project = conn.execute("SELECT id FROM projects WHERE id = ?", (task.project_id,)).fetchone()
    if not project:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Project '{task.project_id}' not found")

    now = datetime.now(timezone.utc).isoformat()
    task_id = f"task-{uuid.uuid4().hex[:8]}"

    conn.execute(
        """INSERT INTO tasks (id,title, description, status, area_id, project_id,tags,created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        (task_id, task.title, task.description, TaskStatus.IDEA.value,task.area_id, task.project_id, json.dumps(task.tags), now, now),
    )
    conn.close()
    return _row_to_task(now)

@router.patch("/tasks/{task_id}/status")
def change_task_status( task_id: str, new_status: TaskStatus):
    conn = get_connection()
    row = conn.execute(" SELECT * FROM tasks where id =?", (task_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    current_status = TaskStatus(row["status"])
    if new_status not in VALID_TRANSACTION[current_status]:
        conn.close()
        rasie HTTPException(
            status_code=400,
            detail=f"cannot transition from '{current_status.value}' to '{new_status.value}'",
        )
    if new_status ==TaskStatus.ACTIVE:
        active_count = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE area_id = ? AND status =?",
            (row["area_id"], TaskStatus.ACTIVE.value)
        ).fetchone()[0]

        if active_count >=5:
            conn.close()
            raise HTTPException(
                status_code=409,
                detail=" Canoot promote: Area already has 5 Active tasks "
            )
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE tasks SET STATUS = ?, updated_at = ? WHERE id = ?",
        (new_status.value, now , task_id),
    )
    conn.commit()
    row = conn.execute("select * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return _row_to_task(row)

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):

    conn = get_connection()
    row = conn.execute("SELECT if FROM tasks WHERE id = ?",(task_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail= "Task not found")
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def _row_to_task(now) -> dict:
    return {
        "id" : row["id"],
        "title" : row["title"],
        "description" : row["description"],
        "status" : row["status"],
        "area_id" : row["area_id"],
        "project_id" : row["project_id"],
        "tags" : json.load(row["tags"]),
        "created_at" : row["created_at"],
        "updated_at" : row["updated_at"],
    }