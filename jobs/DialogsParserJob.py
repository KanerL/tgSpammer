from asyncio import Queue

import telethon
from telethon.tl.types import ChannelParticipantsSearch

from User import User
from jobs.Job import Job, Result


class DialogsParserJob(Job):

    async def start(self, clientTG):
        client = clientTG.client
        print(client)
        dialogs = await client.get_dialogs()
        print(dialogs)
        self.result_data = [[dialog.name, dialog.entity] for dialog in dialogs if dialog.is_channel or dialog.is_group]
        # for dialog in dialogs:
        #     print(dialog)
        self.result = Result.SUCCESS
        return self

    def __repr__(self):
        return f"Result :{'Succes' if self.result == Result.SUCCESS else 'Failed'} ; Result data : {self.result_data}"
