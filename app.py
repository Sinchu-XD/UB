import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session = os.environ.get("SESSION")
group_id = int(os.environ.get("GROUP_ID"))
DELAY = int(os.environ.get("DELAY", 30))
MESSAGE = os.environ.get("MESSAGE")

TAG_FILE = "tagged.txt"

if os.path.exists(TAG_FILE):
    with open(TAG_FILE, "r") as f:
        tagged_users = set(map(int, f.read().splitlines()))
else:
    tagged_users = set()

client = TelegramClient(StringSession(session), api_id, api_hash)

async def main():
    await client.start()
    group = PeerChannel(group_id)
    participants = await client.get_participants(group)

    for user in participants:
        if user.bot or user.deleted:
            continue
        if user.id in tagged_users:
            continue

        try:
            p = await client(GetParticipantRequest(group, user.id))
            if isinstance(p.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                continue
        except:
            continue

        name = user.first_name or "User"
        tag = f"[{name}](tg://user?id={user.id})"

        try:
            await client.send_message(
                group,
                f"{tag} {MESSAGE}",
                parse_mode="md"
            )

            tagged_users.add(user.id)
            with open(TAG_FILE, "a") as f:
                f.write(str(user.id) + "\n")

            await asyncio.sleep(DELAY)
        except:
            await asyncio.sleep(10)

with client:
    client.loop.run_until_complete(main())
