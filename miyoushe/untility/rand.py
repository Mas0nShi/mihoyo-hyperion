import random
from ctypes import CDLL
import os
RAND_DICT = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def randString(length):
    return "".join(random.sample(RAND_DICT, length))


def randFromSystem():
    un = os.uname()

    if un.sysname == "Linux":
        libc = CDLL('libc.so.6')
        libc.srand(libc.time(0))
        return libc.rand()

    if un.sysname == "Darwin":
        libc = CDLL('libc.dylib')
        libc.srand(libc.time(0))
        return libc.rand()

    if un.sysname == "Windows":
        import ctypes
        libc = ctypes.cdll.msvcrt
        libc.srand(libc.time(0))
        return libc.rand()

    raise Exception("Unsupported OS")

