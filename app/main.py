from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import task_router, learning_router, roadmap_router, habit_router, note_router, learning_log_router, mistake_router, milestone_router, orin_router, search_router, notification_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dhananjay's System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(learning_router.router, prefix="/api/learning", tags=["Learning"])
app.include_router(roadmap_router.router, prefix="/api/roadmap", tags=["Roadmap"])
app.include_router(milestone_router.router, prefix="/api/milestones", tags=["Milestones"])
app.include_router(habit_router.router, prefix="/api/habits", tags=["Habits"])
app.include_router(note_router.router, prefix="/api/notes", tags=["Notes"])
app.include_router(learning_log_router.router, prefix="/api/learning-logs", tags=["Learning Logs"])
app.include_router(mistake_router.router, prefix="/api/mistakes", tags=["Mistakes"])
app.include_router(orin_router.router, prefix="/api/orin", tags=["Orin"])
app.include_router(search_router.router, prefix="/api/search", tags=["Search"])
app.include_router(notification_router.router, prefix="/api/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Dhananjay's System API"}
