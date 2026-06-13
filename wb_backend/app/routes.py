import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from wb_backend.app.db import get_connection
from wb_backend.app.models import TaskStatus,TaskCreate, TaskUpdate, VALID_TRANSACTION

router = APIRouter(prefix='/api')
