import os
from pathlib import Path

#esto permite obtener la ruta del directorio del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #ruta del proyecto / dirección donde quieras guardar la db
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES={
    'default':{
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':'db',
        'USER':'postgres',
        'PASSWORD':'15101220',
        'HOST':'localhost',
        'PORT':'5432'
    }
}