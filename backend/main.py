from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, logs, tasks
from app.database import engine  # add this
from app import models            # add this

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)  # add this

app = FastAPI(
    title="DevLog API",
    description="Personal developer journal and task tracker",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

@app.get("/")
def root():
    return {"message": "DevLog API is running"}