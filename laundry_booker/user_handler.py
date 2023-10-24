import asyncio
from threading import Thread
from dataclasses import dataclass
from laundry_booker.laundry_booker import Booker, Result

def print_amount_of_tasks(tasks):
    print(f'amount of active tasks: {len(tasks)}')

class AsyncLoopThread(Thread):
    '''thread class to run asynio loop forever, because it is blocking main thread'''
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

@dataclass
class User:
    '''class to represent user data'''
    # url for the site to book on
    uri: str
    # log and password for site
    login: str = None
    password: str = None
    # target time for booking in string format (title to find on a web page)
    target_time: str = None

class UserHandler:
    '''Class to handle user connections
    users - dict for users with chat_id as a key
    tasks - dict for tasks from users with chat_id as a key
    thread - thread to run asyncio loop
    delay - time period through which booking process will be called again, minutes
    '''
    def __init__(self, delay):
        self.users = {}
        self.tasks = {}
        self.thread = AsyncLoopThread()
        self.delay = delay*60
    
    def append_user(self, chat_id, uri):
        self.users[chat_id] = User(uri)

    def remove_task(self, chat_id):
        self.tasks.pop(chat_id)
    
    def run(self):
        self.thread.start()
    
    async def __booking(self, chat_id):
        print(f'booking for chat_id: {chat_id} was started')
        print_amount_of_tasks(self.tasks)
        try:
            booker = Booker(self.users[chat_id])
            while True:
                result = booker.check()
                if result is not None:
                    return result
                await asyncio.sleep(self.delay)
        except asyncio.CancelledError:
            print(f'booking for chat_id: {chat_id} was cancelled')
        except Exception:
            print(f'something went wrong with booking for chat: {chat_id}')
        finally:
            self.remove_task(chat_id)
            print_amount_of_tasks(self.tasks)

    def start_booking(self, chat_id):
        self.tasks[chat_id] = asyncio.run_coroutine_threadsafe(self.__booking(chat_id),self.thread.loop)
        return self.tasks[chat_id].result()
    
    def stop_booking(self, chat_id):
        self.tasks[chat_id].cancel()


