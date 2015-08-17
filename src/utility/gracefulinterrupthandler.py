# -*- coding: utf-8 -*-
"""
From: http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
"""
import time

import signal

class GracefulInterruptHandler(object):
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):
        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)
        self.released = True
        return True

if __name__ == '__main__':
    with GracefulInterruptHandler() as handler:
        for iteration in range(1000):
            print "start"
            time.sleep(2)
            print "stop"
            if handler.interrupted:
                print 'Exiting gracefully'
                break