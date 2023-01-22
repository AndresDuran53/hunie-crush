import threading
from threading import Thread

class CustomThreads(Thread):

    def __init__(self, sleepSeconds, func, eventStopper):
        Thread.__init__(self)
        self.sleepSeconds = sleepSeconds
        self.func = func
        self.stopped = eventStopper

    def run(self):
        while not self.stopped.wait(self.sleepSeconds):
            self.func()
