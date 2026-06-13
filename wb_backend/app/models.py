from datetime import date,datetime
from enum import Enum
from typing import List,Optional
from pydantic import BaseModel

class TaskStatus(str,Enum):

    IDEA = "idea"
    ACTIVE ="active"
    COMPLETED ="completed"
    ARCHIVED = 'archived'

class RecurrenceSchedule(str, Enum):

    WEEKLY ="weekly"
    MONTHLY ="monthly"

VALID_TRANSACTION = {
    TaskStatus.IDEA: [TaskStatus.ACTIVE, TaskStatus.ARCHIVED],
    TaskStatus.ACTIVE: [TaskStatus.COMPLETED,TaskStatus.IDEA, TaskStatus.ARCHIVED],
    TaskStatus.COMPLETED: [TaskStatus.ARCHIVED],
    TaskStatus.ARCHIVED:[],
}

class area(BaseModel):
    id: str
    name: str

class Project(Basemodel):
    id: str
    area_id: str
    name: str

class Task(BaseModel):
    id: str
    description: str =""
    status : TaskStatus = TaskStatus.IDEA
    area_id :str
    project_id : str
    tags: List[str] =[]
    created_at :datetime
    updated_at : datetime

class TaskCreate(BaseModel):
    title: str
    description: str =""
    area_id: str
    project_id: str
    tags: List[str] =[]

class TaskUpdate(BaseModel):
    title: Optional[str] =  None
    description: Optional[str] = None
    tags: Optional[List[str]]= None

class RecurringTask(BaseModel):
    id: str
    title: str
    description: str =""
    area_id: str
    project_id: str
    schedule: RecurrenceSchedule
    last_completed: Optional[date]: None
    next_due: date

class RecurringTaskInstance(BaseModel):
    id: str
    recurring_task_id: str
    completed_at:datetime
    period_start:date
    period_end:date

class MonthlyGoal(BaseModel):
    id: str
    month :str
    task_ids:List[str] = []
    recurring_task_ids: List[str] = []



