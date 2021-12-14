import threading
import ctypes
import time
class TPlay(threading.Thread):
    def __init__(self, ruta):
        self.ruta = ruta