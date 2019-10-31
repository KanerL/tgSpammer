from abc import ABC, abstractmethod
from asyncio import Queue

import telethon


class Result(enumerate):
    SUCCESS = 0
    FAILED = 1


class Job(ABC):
    result = Result.FAILED
    result_data = None
    client = None
    taskQu: Queue
    taskName = None

    def __init__(self, taskQ=Queue()):
        self.taskQu = taskQ

    @abstractmethod
    async def start(self, client):
        pass

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone
    def __str__(self):
        return f"{self.taskName} Result :{'Succes' if self.result == Result.SUCCESS else 'Failed'} ; Result data : {self.result_data}"
    def __repr__(self):
        return [self.taskName,f"Result :{'Succes' if self.result == Result.SUCCESS else 'Failed'} ; Result data : {self.result_data}"]
