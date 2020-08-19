from apps.Util_apps.LogProject import logging
from apps.Util_apps.Decoradores import execute_in_thread, count_elapsed_time


@count_elapsed_time
@execute_in_thread()
def mis_mensajes(value):
    logging.debug('Esto es un mensaje debug {}'.format(value))
    logging.info('Esto es un mensaje info {}'.format(value))
    logging.warning('Esto es un mensaje warning {}'.format(value))
    logging.error('Esto es un mensaje error {}'.format(value))
    logging.critical('Esto es un mensaje critical {}'.format(value))


mis_mensajes(50)
