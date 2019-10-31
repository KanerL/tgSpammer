import telethon


async def get_all_users(client : telethon.client.TelegramClient):
    dialogs = await client.get_dialogs()
    dialogs = [[dialog.name,dialog.entity] for dialog in dialogs if (dialog.is_channel and dialog.entity.megagroup) or dialog.is_group]
    # for dialog in dialogs:
    #     print(dialog)
    return dialogs