from fastapi import FastAPI
from api.routes import router, set_store
from engine.store import GameStore

app = FastAPI(title="Blackjack API")

store = GameStore()
set_store(store)

app.include_router(router)
