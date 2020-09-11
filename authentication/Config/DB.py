import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

# https://www.ochobitshacenunbyte.com/2018/03/14/configurar-mariadb-y-mysql-para-acceso-remoto/
MARIADB = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HSB',
        'USER': 'hsbproject',
        'PASSWORD': 'A$8mu)U3',
        'HOST': '172.30.19.88',  # Or an IP Address that your database is hosted on
        'PORT': '3306',
        # #optional:
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True,
            'init_command': 'SET '
                            'storage_engine=INNODB,'
                            'character_set_connection=utf8,'
                            'collation_connection=utf8_bin'
            # 'sql_mode=STRICT_TRANS_TABLES,'    # see note below
            # 'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

MARIADB2 = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HSB',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',  # Or an IP Address that your database is hosted on
        'PORT': '3306',
        # #optional:
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True,
            'init_command': 'SET '
                            'storage_engine=INNODB,'
                            'character_set_connection=utf8,'
                            'collation_connection=utf8_bin'
            # 'sql_mode=STRICT_TRANS_TABLES,'    # see note below
            # 'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}
