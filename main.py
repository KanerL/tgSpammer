import asyncio
import threading
from asyncio import Queue

import utils
# Use your own values here
from TelegramClient import STelegramClient
from config import clients_users
from jobs import Job
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
def worker(clients, resultq, loop, users):
    asyncio.set_event_loop(loop)
    menu = WorkerMenu(clients, resultq)
    while True:
        i = int(input('Write num'))
        menu.menu[i]()
        if i == 4:
            print('Exiting...')
            break


def run_cor(cor):
    return asyncio.run_coroutine_threadsafe(cor, asyncio.get_event_loop()).result()


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

    def add_new_item_to_task(self, self_channel_mode=True):
        if self_channel_mode:
            for i, item in enumerate(self.clients):
                print(i, item)
            i = int(input("choose client"))
            client = self.clients[i].client
            channels = run_cor(utils.get_all_users(client))
            for item, i in enumerate(channels):
                print(item, i)
            i = input('choose items:')
            channels = list(map(lambda x: channels[int(x)][1], i.split(' ')))
        else:
            i = input('Input http link to channel')
            channels = i.split(',')
        for channel in channels:
            print(channel)
            run_cor(self.task.taskQu.put(channel))

    # TODO выбрать форму заданий и распределения заданий между акками
    def submit_task(self):
        for client in self.clients:
            run_cor(client.taskQ.put(self.task))

    def done_tasking(self):
        run_cor(self.resultq.put(None))
        for client in self.clients:
            run_cor(client.taskQ.put(None))


async def init_clients(clients_phones):
    users = []
    q = Queue()
    resq = Queue()
    clients = []
    start_tasks = []
    print(clients_phones)
    for _ in range(len(clients_phones)):
        client = STelegramClient(f'tg{_}',clients_phones[_], resq, q, users)
        clients.append(client)
        start_tasks.append(asyncio.create_task(client.start_client()))
    for _ in range(len(clients_phones)):
        await start_tasks[_]
    return q, resq, clients, users


async def proccess_results(result_q: Queue):
    while (result := await result_q.get()) is not None:
        print(result)


async def main():
    q, resultQu, clients, users = await init_clients([380675111025,380666913447])
    _, _, user1 = await resultQu.get()
    _, _, user2 = await resultQu.get()
    print(user1)
    print(user2)
    clients_users.append(user1.id)
    clients_users.append(user2.id)
    print(clients_users)
    print(1)
    task1 = asyncio.create_task(proccess_results(resultQu))
    task2 = asyncio.create_task(clients[0].run_client())
    task3 = asyncio.create_task(clients[1].run_client())
    thread_menu = threading.Thread(target=worker, args=[clients, resultQu, asyncio.get_event_loop(), users],
                                   daemon=True)
    thread_menu.start()
    await task2
    await task3
    await task1
    thread_menu.join()
    print('MainThread')


if __name__ == '__main__':
    asyncio.run(main())
