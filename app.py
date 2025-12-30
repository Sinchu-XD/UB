import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
group_id = int(os.environ.get("GROUP_ID"))
DELAY = int(os.environ.get("DELAY", 30))
MESSAGE = os.environ.get("MESSAGE")

client = TelegramClient("userbot", api_id, api_hash)

tagged_users = set()

async def main():
    await client.start()
    group = PeerChannel(group_id)
    participants = await client.get_participants(group)

    for user in participants:
        if user.bot or user.deleted:
            continue
        if user.id in tagged_users:
            continue

        if user.username:
            tag = f"@{user.username}"
        else:
            tag = f"[User](tg://user?id={user.id})"

        try:
            await client.send_message(
                group,
                f"{tag} {MESSAGE}",
                parse_mode="md"
            )
            tagged_users.add(user.id)
            await asyncio.sleep(DELAY)
        except:
            await asyncio.sleep(10)

with client:
    client.loop.run_until_complete(main())
