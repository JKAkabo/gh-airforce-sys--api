from typing import Optional

from asyncpg import Pool, Connection, Record
from fastapi import APIRouter, Depends

from bluestorm.dependencies import get_db_pool
from bluestorm.models.rank_categories import RankCategoryPublic, RankCategoryCreate, RankCategoryUpdate
from bluestorm.models.ranks import RankPublic
from bluestorm.repos import rank_categories as rank_categories_repo, ranks as ranks_repo

router = APIRouter(prefix='/rank-categories', tags=['rank categories'])


@router.get('', response_model=list[RankCategoryPublic])
async def read_rank_categories(enabled: Optional[bool] = None, db_pool: Pool = Depends(get_db_pool)) -> list[Record]:
    rank_categories: list[Record]
    connection: Connection
    async with db_pool.acquire() as connection:
        if enabled is None:
            rank_categories = await rank_categories_repo.find_all(connection)
        elif enabled:
            rank_categories = await rank_categories_repo.find_enabled(connection)
        else:
            rank_categories = await rank_categories_repo.find_disabled(connection)
    return rank_categories


@router.get('/{rank_category_id}', response_model=RankCategoryPublic)
async def read_rank_category(rank_category_id: int, db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank_category: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        rank_category = await rank_categories_repo.find_by_id(connection, rank_category_id)
    return rank_category


@router.post('', response_model=RankCategoryPublic)
async def create_rank_category(rank_category_create: RankCategoryCreate,
                               db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank_category: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        rank_category_id: int = await rank_categories_repo.save(connection, rank_category_create)
        rank_category = await rank_categories_repo.find_by_id(connection, rank_category_id)
    return rank_category


@router.put('/{rank_category_id}', response_model=RankCategoryPublic)
async def update_rank_category(rank_category_id: int, rank_category_update: RankCategoryUpdate,
                               db_pool: Pool = Depends(get_db_pool)) -> Record:
    rank_category: Record
    connection: Connection
    async with db_pool.acquire() as connection:
        await rank_categories_repo.update(connection, rank_category_id, rank_category_update)
        rank_category = await rank_categories_repo.find_by_id(connection, rank_category_id)
    return rank_category


@router.get('/{rank_category_id}/ranks', response_model=list[RankPublic])
async def read_ranks_for_rank_category(rank_category_id: int, enabled: Optional[bool] = None,
                                       db_pool: Pool = Depends(get_db_pool)) -> list[Record]:
    ranks: list[Record]
    connection: Connection
    async with db_pool.acquire() as connection:
        if enabled is None:
            ranks = await ranks_repo.find_all_by_rank_category_id(connection, rank_category_id)
        elif enabled:
            ranks = await ranks_repo.find_enabled_by_rank_category_id(connection, rank_category_id)
        else:
            ranks = await ranks_repo.find_disabled_by_rank_category_id(connection, rank_category_id)
    return ranks
