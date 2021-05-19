from typing import Optional, List

from asyncpg import Pool, Connection, Record
from fastapi import APIRouter, Depends

from bluestorm.dependencies import get_db_pool
from bluestorm.models.wings import WingPublic, WingCreate, WingUpdate
from bluestorm.repos import wings as wings_repo

router = APIRouter(prefix='/wings', tags=['wings'])


@router.get('', response_model=List[WingPublic])
async def read_wings(enabled: Optional[bool] = None, db_pool: Pool = Depends(get_db_pool)) -> List[Record]:
    wings: List[Record]
    connection: Connection
    async with db_pool.acquire() as connection:
        if enabled is None:
            wings = await wings_repo.find_all(connection)
        elif enabled:
            wings = await wings_repo.find_enabled(connection)
        else:
            wings = await wings_repo.find_disabled(connection)
    return wings


@router.get('/{wing_id}', response_model=WingPublic)
async def read_wing(wing_id: int, db_pool: Pool = Depends(get_db_pool)) -> Record:
    wing: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        wing = await wings_repo.find_by_id(connection, wing_id)
    return wing


@router.post('', response_model=WingPublic)
async def create_wing(wing_create: WingCreate, db_pool: Pool = Depends(get_db_pool)) -> Record:
    wing: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        wing_id: int = await wings_repo.save(connection, wing_create)
        wing = await wings_repo.find_by_id(connection, wing_id)
    return wing


@router.put('/{wing_id}', response_model=WingPublic)
async def update_wing(wing_id: int, wing_update: WingUpdate, db_pool: Pool = Depends(get_db_pool)) -> Record:
    wing: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        await wings_repo.update(connection, wing_id, wing_update)
        wing = await wings_repo.find_by_id(connection, wing_id)
    return wing
