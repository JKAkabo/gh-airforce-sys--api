from asyncpg import Record, Connection
from typing import List
from bluestorm.models.ranks import RankCreate, RankUpdate


async def find_all(connection: Connection) -> List[Record]:
    return await connection.fetch('select * from ranks')


async def find_enabled(connection: Connection) -> List[Record]:
    return await connection.fetch('select * from ranks where enabled = true')


async def find_disabled(connection: Connection) -> List[Record]:
    return await connection.fetch('select * from ranks where enabled = false')


async def find_by_id(connection: Connection, rank_id: int) -> Record:
    return await connection.fetchrow('select * from ranks where id = $1', rank_id)


async def find_all_by_rank_category_id(connection: Connection, rank_category_id: int) -> List[Record]:
    return await connection.fetch('select * from ranks where rank_category_id = $1', rank_category_id)


async def find_enabled_by_rank_category_id(connection: Connection, rank_category_id: int) -> List[Record]:
    return await connection.fetch(
        'select * from ranks where enabled = true and rank_category_id = $1',
        rank_category_id
    )


async def find_disabled_by_rank_category_id(connection: Connection, rank_category_id: int) -> List[Record]:
    return await connection.fetch(
        'select * from ranks where enabled = false and rank_category_id = $1',
        rank_category_id
    )


async def save(connection: Connection, rank_create: RankCreate) -> int:
    return await connection.fetchval(
        'insert into ranks (name, enabled, rank_category_id) values ($1, $2, $3)',
        rank_create.name,
        rank_create.enabled,
        rank_create.rank_category_id
    )


async def update(connection: Connection, rank_id: int, rank_update: RankUpdate):
    await connection.execute(
        'update ranks set name = $1, enabled = $2, rank_category_id = $3 where id = $4',
        rank_update.name,
        rank_update.enabled,
        rank_update.rank_category_id,
        rank_id
    )
