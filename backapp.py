from threading import Thread, Event
from random import random
import time


thread = Thread()
thread_stop_event = Event()

class RetThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RetThread, self).__init__()

    def randomNumberGenerator(self):
        print("making random nums")
        while not thread_stop_event.isSet():
            number = round(random()*10, 3)
            print(number)

    def run(self):
        self.randomNumberGenerator()

retThread = RetThread()
retThread.start()
