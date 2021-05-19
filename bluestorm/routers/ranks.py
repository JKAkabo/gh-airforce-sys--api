from typing import Optional,List

from asyncpg import Pool, Connection, Record
from fastapi import APIRouter, Depends

from bluestorm.dependencies import get_db_pool
from bluestorm.models.ranks import RankPublic, RankCreate, RankUpdate
from bluestorm.repos import ranks as ranks_repo

router = APIRouter(prefix='/ranks', tags=['ranks'])


@router.get('', response_model=List[RankPublic])
async def read_ranks(enabled: Optional[bool] = None, db_pool: Pool = Depends(get_db_pool)) -> List[Record]:
    ranks: List[Record]
    connection: Connection
    async with db_pool.acquire() as connection:
        if enabled is None:
            ranks = await ranks_repo.find_all(connection)
        elif enabled:
            ranks = await ranks_repo.find_enabled(connection)
        else:
            ranks = await ranks_repo.find_disabled(connection)
    return ranks


@router.get('/{rank_id}', response_model=RankPublic)
async def read_rank(rank_id: int, db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        rank = await ranks_repo.find_by_id(connection, rank_id)
    return rank


@router.post('', response_model=RankPublic)
async def create_rank(rank_create: RankCreate, db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        rank_id: int = await ranks_repo.save(connection, rank_create)
        rank = await ranks_repo.find_by_id(connection, rank_id)
    return rank


@router.put('', response_model=RankPublic)
async def update_rank(rank_id: int, rank_update: RankUpdate, db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        await ranks_repo.update(connection, rank_id, rank_update)
        rank = await ranks_repo.find_by_id(connection, rank_id)
    return rank
