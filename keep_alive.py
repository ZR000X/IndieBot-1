#http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/

import threading
import time


class keep_alive(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        i = 0
        while True:
            # Do something
            i += 1
            # print('keeping this bot alive', i)

            time.sleep(self.interval)