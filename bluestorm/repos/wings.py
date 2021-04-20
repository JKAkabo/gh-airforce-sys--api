from asyncpg import Record, Connection

from bluestorm.models.wings import WingCreate, WingUpdate


async def find_all(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from wings')


async def find_enabled(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from wings where enabled = true')


async def find_disabled(connection: Connection) -> list[Record]:
    return await connection.fetch('select * from wings where enabled = false')


async def find_by_id(connection: Connection, wing_id: int) -> Record:
    return await connection.fetchrow('select * from wings where id = $1', wing_id)


async def save(connection: Connection, wing_create: WingCreate) -> int:
    return await connection.fetchval(
        'insert into wings (name, enabled) values ($1, $2) returning id',
        wing_create.name,
        wing_create.enabled
    )


async def update(connection: Connection, wing_id: int, wing_update: WingUpdate):
    await connection.execute(
        'update wings set name = $1, enabled = $2 where id = $3',
        wing_update.name,
        wing_update.enabled,
        wing_id
    )
