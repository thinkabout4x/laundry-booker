import asyncio
from threading import Thread



class AsyncLoopThread(Thread):
    '''thread class to run asynio loop forever, because it is blocking main thread'''
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class User:
    '''class to represent user data'''
    def __init__(self, uri):
        # url for the site to book on
        self.uri = uri
        # log and password for site
        self.login = None
        self.password = None
        # target time for booking in string format (title to find on a web page)
        self.target_time = None
        # booking state
        self.isbooked = False

class UserHandler:
    '''Class to handle user connections
    users - dict for users with chat_id as a key
    tasks - dict for tasks from users with chat_id as a key
    thread - thread to run asyncio loop
    delay - time period through which booking process will be called again
    '''
    def __init__(self, delay):

        self.users = {}
        self.tasks = {}
        self.thread = AsyncLoopThread()
        self.delay = delay
    
    def append_user(self, chat_id, uri):
        self.users[chat_id] = User(uri)
    
    def run(self):
        self.thread.start()
    
    async def __booking(self, chat_id):
        print(f'booking for chat_id: {chat_id} was started')
        try:
            while True:
                pass
                print('booooooking')
                await asyncio.sleep(self.delay)
        except asyncio.CancelledError:
            print(f'booking for chat_id: {chat_id} was cancelled')
        
    def start_booking(self, chat_id):
        self.tasks[chat_id] = asyncio.run_coroutine_threadsafe(self.__booking(chat_id),self.thread.loop)
    
    def stop_booking(self, chat_id):
        self.tasks[chat_id].cancel()

