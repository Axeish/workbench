import sqlite3
from pathlib import Path

DB_PATH = Path("wb_backend/data/workbench.db")

def get_connection() -> sqlite3.Connection:
    '''get SQLConnection. Create db if it doe snot exist'''
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory =sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db() -> None:
    """Create Table if they do not exist"""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS area (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            area_id TEXT NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (area_id) REFERENCES area(id)
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'idea',
            area_id TEXT NOT NULL,
            project_id TEXT NOT NULL,
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NIT NULL,
            FOREIGN KEY (area_id) REFERENCES area(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
        CREATE TABLE IF NOT EXISTS recurring_tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'idea',
            area_id TEXT NOT NULL,
            project_id TEXT NOT NULL,
            schedule TEXY NOT NULL,
            last_completed TEXT,
            next_due TEXT NOT NULL,
            FOREIGN KEY (area_id) REFERENCES area(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
            
        );
        CREATE TABLE IF NOT EXISTS recurring_instances (
            id TEXT PRIMARY KEY,
            recurring_task_id  TEXTNOT NULL,
            completed_at TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            FOREIGN KEY (recurring_task_id) REFERENCES recurring_tasks(id)
        );
        CREATE TABLE IF NOT EXISTS monthly_goal (
            id TEXT PRIMARY KEY,
            month TEXT NOT NULL,
            task_ids TEXT DEFAULT '[]',
            recurring_task_ids TEXT DEFAULT '[]'
        );
    """)

    existing = conn.execute("SELECT COUNT(*) FROM area").fetchone()[0]
    if existing == 0:
        conn.execute("INSERT INTO area (id,name) VALUES ('1','Axeishguy')")
        conn.execute("INSERT INTO area (id,name) VALUES ('2','Cornoddity')")
        conn.commit()
    conn.close()