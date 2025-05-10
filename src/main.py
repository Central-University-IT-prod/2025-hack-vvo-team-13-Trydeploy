from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
from datetime import datetime
from pathlib import Path

app = FastAPI()

# Database file configuration
DB_FILE = Path("points_db.json")

# Ensure the database file exists
if not DB_FILE.exists():
    DB_FILE.write_text("[]")


class Point(BaseModel):
    longitude: float
    latitude: float
    name: str
    description: str
    picture_links: List[str]
    categories: List[str]
    address: Optional[str] = None
    website: Optional[str] = None


class PointResponse(Point):
    id: str
    created_at: datetime


def read_db() -> List[dict]:
    """Read all points from the database file"""
    return json.loads(DB_FILE.read_text())

def del_db():
    DB_FILE.write_text(
        '[]'
    )

def write_db(data: List[dict]):
    """Write all points to the database file"""
    DB_FILE.write_text(json.dumps(data, indent=2, default=str))

@app.post("/del-db-for-real/")
def del_db_fr():
    DB_FILE.write_text(
        "[]"
    )
    return "ОК"

@app.post("/del-db/")
def del_db():
    return "nuh-uh"
@app.post("/points/", response_model=PointResponse)
async def add_point(point: Point):
    """Add a new point to the database"""
    points = read_db()
    point_id = str(uuid.uuid4())
    # noinspection PyDeprecation
    created_at = datetime.utcnow()

    new_point = {
        **point.dict(),
        "id": point_id,
        "created_at": created_at
    }

    points.append(new_point)
    write_db(points)

    return new_point


@app.get("/points/", response_model=List[PointResponse])
async def get_all_points():
    return read_db()


@app.get("/points/{point_id}", response_model=PointResponse)
async def get_point(point_id: str):
    points = read_db()
    for point in points:
        if point["id"] == point_id:
            return point
    raise HTTPException(status_code=404, detail="Point not found")
