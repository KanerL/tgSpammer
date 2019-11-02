import asyncio
from asyncio import Queue

import telethon
from telethon import TelegramClient

from config import api_id, api_hash
from jobs.Job import Job, Result


class STelegramClient:
    name = None

    def __init__(self, name: str,phone :str, resultQu: Queue, taskQu: Queue, users: list):
        self.resultQ = resultQu
        self.taskQ = taskQu
        self.name = name
        self.client: telethon.TelegramClient
        self.client = None
        self.users = users
        self.phone = phone

    async def start_client(self):
        self.client = TelegramClient(self.name, api_id, api_hash)
        await self.client.connect()
        if not await self.client.is_user_authorized():
            phone = "+" + self.phone
            await self.client.sign_in(phone)  # send code
            code = input('enter code: ')
            await self.client.sign_in(phone, code)
        await self.client.start()
        self.client: telethon.TelegramClient
        await self.resultQ.put(
            (Result.SUCCESS, f"TGClient {self.name} started succesfully", await self.client.get_me()))
        # self.client.run_until_disconnected()
        # await self.run_client()

    async def del_async(self):
        await self.client.disconnect()

    def __del__(self):
        pass

    def __repr__(self):
        return self.name

    async def run_client(self):
        print(f"Runned client {self.name},current task size = {self.taskQ.qsize()}")
        while (task := await self.taskQ.get()) is not None:
            task: Job
            print(f'Client {self.name} starting working on {task},task size {task.taskQu.qsize()}')
            # task_res = asyncio.create_task(task.start(self))
            async for job_result in task.start(self):
                print(f'{self.name}got {job_result}')
                await self.resultQ.put(job_result)
        await self.del_async()
