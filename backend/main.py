from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, expenses, categories

# ─── App Instance ─────────────────────────────────────────────
app = FastAPI(
    title="Expense Approval System",
    description="Backend API ",
    version="1.0.0",
)

# ─── CORS Middleware ──────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # update to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)

# ─── Health Check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Expense Approval API is running"}

# NOTE: DB tables are managed by the database team — no auto-create here
