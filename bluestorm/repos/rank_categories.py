from asyncpg import Record, Connection

from bluestorm.models.rank_categories import RankCategoryCreate, RankCategoryUpdate


async def find_all(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from rank_categories')


async def find_enabled(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from rank_categories where enabled = true')


async def find_by_id(connection: Connection, rank_category_id: int) -> Record:
    return await connection.fetchrow('select * from rank_categories where id = $1', rank_category_id)


async def find_disabled(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from rank_categories where enabled = false')


async def save(connection: Connection, rank_category_create: RankCategoryCreate) -> int:
    return await connection.fetchval(
        'insert into rank_categories (name, enabled) values ($1, $2) returning id',
        rank_category_create.name,
        rank_category_create.enabled
    )


async def update(connection: Connection, rank_category_id: int, rank_category_update: RankCategoryUpdate):
    await connection.execute(
        'update rank_categories set name = $1, enabled = $2 where id = $3',
        rank_category_update.name,
        rank_category_update.enabled,
        rank_category_id
    )
