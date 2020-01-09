import threading


class Thread(threading.Thread):
    def __init__(self, thread_id, task_handle, task_pool):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.task_handle = task_handle
        self.task_pool = task_pool
        print("Thread", self.thread_id, "start")

    def run(self):
        while 1:
            task = self.task_pool()
            if task == None:
                break
            self.task_handle(self.thread_id, task)

    def __del__(self):
        print("Thread", self.thread_id, "close")
