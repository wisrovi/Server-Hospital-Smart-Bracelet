import logging
import authentication.settings as SETTINGS
import authentication.Config.CONFIG_LOG as CONFIG_LOG


logging.basicConfig(
    level=CONFIG_LOG.MESSAGES_LOG_VIEW,
    format='{'
           '"Type": "%(levelname)s", '
           '"Date": "%(asctime)s", '
           '"Details": {'
           '"PathName": "%(pathname)s", '
           '"File": "%(filename)s", '
           '"Function": "%(funcName)s", '
           '"Line": "%(lineno)s", '
           '"Module": "%(module)s", '
           '"Name": "%(name)s", '
           '"Thread_number": "%(thread)s", '
           '"Thread_name": "%(threadName)s", '
           '"Process_number": "%(process)s", '
           '"Process_name": "%(processName)s" '
           '}, '
           '"Message": "%(message)s"'
           '}',
    #datefmt='%H:%M:%S',
    filename=SETTINGS.BASE_DIR + '/logProject.txt'  # Para almacenar los mensajes
)
