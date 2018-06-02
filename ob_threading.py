import threading

class ob_Thread(threading.Thread):
    def __init__(self):
        self.active = True
        self.stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """Method representing the thread's activity.
        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.
        """

        while not self.stop_event.is_set():
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            finally:
            # Avoid a recycle if the thread is running a function with
            # an argument that has a member that points to the thread.

                del self._target, self._args, self._kwargs

