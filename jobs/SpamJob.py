import telethon

from jobs.Job import Job, Result


class SpamJob(Job):
    async def start(self, clientTG):
        client: telethon.TelegramClient = clientTG.client
        while not self.taskQu.empty():
            user, message = (await self.taskQu.get())
            try:
                success = await client.send_message(user,message)
                if success:
                    self.result = Result.SUCCESS
                    self.result_data = f"Message {success} is sent by {clientTG.name}"
                else:
                    self.result_data = f"Problem with sending message by {clientTG.name}"
                    self.result = Result.FAILED
                yield self.__copy__()
            except Exception as e:
                self.result = Result.FAILED
                self.result_data = [str(e)]
                yield self.__copy__()
