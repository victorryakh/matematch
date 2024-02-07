import aiosqlite
import asyncio
import config

async def init_db():
    async with aiosqlite.connect(config.sqlite_file) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, global_name TEXT, name TEXT, about TEXT, )''')
        await db.commit()

# Функция для добавления новой учетной записи пользователя
async def add_user(username, password):
    async with aiosqlite.connect(config.sqlite_file) as db:
        try:
            await db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        except aiosqlite.OperationalError:
            await init_db()
            await add_user(username, password)
            return
        await db.commit()
    print("Учетная запись пользователя успешно добавлена!")

# Функция для удаления учетной записи пользователя
async def delete_user(username):
    async with aiosqlite.connect(config.sqlite_file) as db:
        await db.execute("DELETE FROM users WHERE username = ?", (username,))
        await db.commit()
    print("Учетная запись пользователя успешно удалена!")

# Функция для изменения пароля пользователя
async def update_password(username, new_password):
    async with aiosqlite.connect(config.sqlite_file) as db:
        await db.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        await db.commit()
    print("Пароль пользователя успешно изменен!")

# Пример использования функций
async def main():
    await add_user("user1", "password1")
    await add_user("user2", "password2")

    await delete_user("user1")

    await update_password("user2", "new_password")

# Запуск асинхронной функции
asyncio.run(main())