#!/usr/bin/env python3

import threading

class PCQueue:

    def __init__ (self):
        self.queue = []
        self.q_lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)

    def put(self,item):
        self.empty.acquire()
        self.q_lock.acquire()
        self.queue.append(item)
        self.q_lock.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.q_lock.acquire()
        item = self.queue.pop(0)
        self.q_lock.release()
        self.empty.release()
        return item

    def markEnd(self):
        self.put('end')
