import aiosqlite
import asyncio
import config
import logging

async def init_db():
    async with aiosqlite.connect(config.sqlite_file) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, about TEXT, tz TEXT, banned INTEGER)''')
        await db.commit()
        logging.warning('TABLE CREATED')

async def destroy_db():
        async with aiosqlite.connect(config.sqlite_file) as db:
            await db.execute('DROP TABLE IF EXISTS ?', config.sqlite_file)
            await db.commit()
        logging.warning('TABLE DESTROYED')

async def is_user(id):
    async with aiosqlite.connect(config.sqlite_file) as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (id,)) as cursor:
            return (await cursor.fetchone()) is not None
         
async def add_user(id, about="", tz="Etc/UTC"):
    async with aiosqlite.connect(config.sqlite_file) as db:
        try:
            await db.execute("INSERT INTO users (id, about, tz, banned) VALUES (?, ?, ?, ?)", (id, about, tz, 0))
        except aiosqlite.OperationalError:
            await init_db()
            await add_user(id, about)
            return
        except aiosqlite.IntegrityError:
            logging.warning(f'Account< {id} exists')
            return
        await db.commit()
        logging.info(f"Account added: {id}")

async def get_user(user_id):
    async with aiosqlite.connect(config.sqlite_file) as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (user_id,)) as cursor:
            user = await cursor.fetchone()
    logging.info(f"Account got: {user}")
    return user

# Функция для изменения пароля пользователя
async def update_fields(field_name, field_value):
    async with aiosqlite.connect(config.sqlite_file) as db:        
        await db.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        await db.commit()
    print("Пароль пользователя успешно изменен!")

# Пример использования функций
async def main():
    await add_user(1, about="aboutme", tz="Russia/Moscow")
    print( await get_user(1))
# Запуск асинхронной функции
# asyncio.run(main())