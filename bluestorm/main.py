import uvicorn
import asyncpg
from fastapi import Depends, FastAPI

from bluestorm.routers.users import router as users_router
from bluestorm.routers.access_tokens import router as access_tokens_router
from bluestorm.routers.persons import router as persons_router
from bluestorm.routers.wings import router as wings_router
from bluestorm.routers.rank_categories import router as rank_categories_router
from bluestorm.dependencies import get_settings
app = FastAPI()


@app.on_event('startup')
async def startup():
    db_pool: asyncpg.Pool = await asyncpg.create_pool(get_settings().DATABASE_URL)
    app.state.db_pool = db_pool


@app.on_event('shutdown')
async def shutdown():
    await app.state.db_pool.close()


app.include_router(persons_router)
app.include_router(users_router)
app.include_router(access_tokens_router)
app.include_router(wings_router)
app.include_router(rank_categories_router)
