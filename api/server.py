from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.routes import router, set_store
from engine.store import GameStore

app = FastAPI(title="Blackjack API")

store = GameStore()
set_store(store)

app.include_router(router)

_FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

@app.get("/", response_class=HTMLResponse)
def index():
    return _FRONTEND.read_text(encoding="utf-8")
