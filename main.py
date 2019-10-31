import re
import threading

from telethon import TelegramClient, events
import utils
import asyncio
from asyncio import Queue
from queue import Queue as Que
# Use your own values here
from TelegramClient import STelegramClient
from config import clients_users
from jobs import Job
from jobs.DialogsParserJob import DialogsParserJob
from jobs.UserParserJob import UserParserJob


# async def main():
#     async with TelegramClient('name', api_id, api_hash) as client:
#         await client.send_message('me', 'Hello, myself!')
#         channels = await utils.get_all_users(client)
#         for item,i in enumerate(channels):
#             print(item,i)
#         i = int(input("choose item"))
#         qu = Queue()
#         qu.put(channels[i][1])
#         parsingJob = UserParserJob(client,qu)
#         await parsingJob.start()
def worker(clients, resultq, loop,users):
    asyncio.set_event_loop(loop)
    menu = WorkerMenu(clients, resultq)
    while True:
        i = int(input('Write num'))
        menu.menu[i]()
        if i == 4:
            print('Exiting...')
            break


class WorkerMenu():
    def __init__(self, clients, resultq):
        self.users = []
        self.clients = clients
        self.resultq = resultq
        self.task = None
        self.task: Job
        self.menu = {1: self.create_new_task,
                     2: self.add_new_item_to_task,
                     3: self.submit_task,
                     4: self.done_tasking}
        super().__init__()

    def create_new_task(self):
        print(asyncio.get_event_loop())
        self.task = UserParserJob(Queue())

    def run_cor(self, cor):
        return asyncio.run_coroutine_threadsafe(cor, asyncio.get_event_loop()).result()

    def add_new_item_to_task(self, self_channel_mode=True):
        if self_channel_mode:
            for i, item in enumerate(self.clients):
                print(i, item)
            i = int(input("choose client"))
            client = self.clients[i].client
            channels = self.run_cor(utils.get_all_users(client))
            for item, i in enumerate(channels):
                print(item, i)
            i = input('choose items:')
            channels = list(map(lambda x: channels[int(x)][1], i.split(' ')))
        else:
            i = input('Input http link to channel')
            channels = i.split(',')
        for channel in channels:
            print(channel)
            self.run_cor(self.task.taskQu.put(channel))

    # TODO выбрать форму заданий и распределения заданий между акками
    def submit_task(self):
        for client in self.clients:
            self.run_cor(client.taskQ.put(self.task))

    def done_tasking(self):
        for client in self.clients:
            self.run_cor(client.taskQ.put(None))


async def init_clients(n):
    users = []
    q = Queue()
    resq = Queue()
    clients = []
    start_tasks = []
    for _ in range(n):
        client = STelegramClient(f'tg{_}', resq, q,users)
        clients.append(client)
        start_tasks.append(asyncio.create_task(client.start_client()))
    for _ in range(n):
        await start_tasks[_]
    return q, resq, clients


async def main():
    q, resultQu, clients,users = await init_clients(2)
    _, _, user1 = await resultQu.get()
    _, _, user2 = await resultQu.get()
    print(user1)
    print(user2)
    clients_users.append(user1.id)
    clients_users.append(user2.id)
    print(clients_users)
    print(1)
    task2 = asyncio.create_task(clients[0].run_client())
    task3 = asyncio.create_task(clients[1].run_client())
    thread_menu = threading.Thread(target=worker, args=[clients, resultQu, asyncio.get_event_loop()],
                                   daemon=True)
    thread_menu.start()
    await task2
    await task3
    thread_menu.join()
    print('MainThread')



if __name__ == '__main__':
    asyncio.run(main())
