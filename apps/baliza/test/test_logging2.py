from multiprocessing import Process
import requests

from apps.Util_apps.LogProject import logging


# def execute_in_process(name=None, daemon=None):


def _execute_in_process(f):
    """
        Decorator.
        Execute the function in thread.
    """

    def wrapper(*args, **kwargs):
        print("Se ha lanzado un nuevo proceso")
        process = Process(target=f, args=args, kwargs=kwargs)
        process.start()

        ret = f(*args, **kwargs)
        return ret

    return wrapper


@_execute_in_process
def mostrarData(value):
    print(value)


if __name__ == "__main__":
    # process = Process(target=mostrarData, args=('5',))
    # process.start()

    mostrarData(10)
