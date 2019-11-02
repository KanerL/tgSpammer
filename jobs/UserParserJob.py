from asyncio import Queue

import telethon
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import ChannelParticipantsSearch, Updates

from User import User
from config import clients_users
from jobs.Job import Job, Result


class UserParserJob(Job):
    taskName = 'Parser'

    async def start(self, clientTG):
        client = clientTG.client
        while not self.taskQu.empty():
            channel = await self.taskQu.get()
            print(channel)
            if type(channel) is str:
                channel = channel.replace('https://', '')
                try:
                    chan = client.get_entity(channel)
                except ValueError as e:
                    if str(
                            e) == 'Cannot get entity from a channel (or group) that you are not part of. Join the group and retry':
                        hash = channel[channel.rfind('/') + 1:]
                        updates: Updates = client(ImportChatInviteRequest(hash))
                        try:
                            print(f'Успешно вступлено в группу {updates.chats[0].title}')
                            channel = chan
                        except:
                            print(f'Не удалось вступить в группу {channel}')

                    else:
                        print(f'Не удалось вступить в группу {channel}')
                        continue
            try:
                all_participants = await client.get_participants(channel, aggressive=True)
                self.result_data = []
                for part in all_participants:
                    part: telethon.tl.types.User
                    if part.id in clients_users:
                        continue
                    self.result_data.append(User(username=part.username,
                                                 phone=part.phone,
                                                 fullname=(part.first_name if part.first_name else "") + (
                                                     " " + part.last_name if part.last_name else ""),
                                                 userid=part.id,
                                                 user_entity=part))
                    self.result = Result.SUCCESS
                yield self.__copy__()
            except Exception as e:
                self.result = Result.FAILED
                self.result_data = [str(e)]
                yield self.__copy__()
