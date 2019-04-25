import threading


class AtomicCounter:
    def __init__(self, initial=0):
        self._initial = initial
        self._offset = 0
        self._lock = threading.Lock()

    def init(self, initial):
        with self._lock:
            self._initial = initial

    @property
    def initial(self):
        return self._initial

    def get_count(self):
        return self._initial - self._offset

    def increment(self, num=1):
        with self._lock:
            self._offset -= num
            return self.get_count()

    def decrement(self, num=1):
        with self._lock:
            self._offset += num
            return self.get_count()
