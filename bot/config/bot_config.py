import logging
import time
from datetime import datetime
import mysql.connector

import discord

TOKEN = OWNER_ID = None

# DBコンテナの起動を待つ
while True:
    try:
        with mysql.connector.Connect(**{
            "host": "db",
            "port": "3306",
            "user": "application",
            "password": "applicationpassword",
            "database": "Master",
            "charset": "utf8mb4",
            "collation": "utf8mb4_general_ci",
            "autocommit": False
        }) as connect:
            with connect.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM Master.config WHERE name LIKE 'bot_%'")
                data = cur.fetchall()
                for d in data:
                    match d["name"]:
                        case "bot_token":
                            TOKEN = d["value"]
                        case "bot_owner_id":
                            OWNER_ID = int(d["value"])
        break
    except mysql.connector.errors.InterfaceError as e:
        logging.warning("waiting database.....")
        time.sleep(3)
        continue


async def NOTIFY_TO_OWNER(bot, message: str):
    owner = await bot.fetch_user(OWNER_ID)
    dmCh = await owner.create_dm()
    await dmCh.send(
        content="Bot Status Notification",
        embed=discord.Embed().add_field(
            name="Status",
            value=message
        ).set_footer(
            text=str(datetime.now())
        )
    )
