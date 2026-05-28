from threading import Lock

class Singleton(type):
    """
    Thread-safe implementation of Singleton.
    """
    _instances = {}

	# Lock object used to synchronise threads during first access to the Singleton.
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]