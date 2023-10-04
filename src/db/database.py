from flask_mysqldb import MySQL
import mysql.connector

# Herramientas
import json
from functools import reduce

# Manejo de fechas
import datetime
import calendar
from datetime import timedelta

# Decouple
from decouple import config

class Database():
    def __init__(self, app):
        '''
        Configuración de la base de datos MySQL
        '''
        print('[ORDERS] Inicializando base de datos...')

        self.controller = None

        self.app = app

        # Config session
        self.app.config['MYSQL_USER'] = config('USER')
        self.app.config['MYSQL_HOST'] = config('HOST')
        self.app.config['MYSQL_PASSWORD'] = config('PASSWD')
        self.app.config['MYSQL_DB'] = config('DATABASE')
        self.app.config['MYSQL_CONNECT_TIMEOUT'] = 60
        
        self.mysql = MySQL(self.app)

    #Config Access
    def login_database(self) -> 'mysql.connector.cursor':
        '''
        Iniciamos una conexion a la base de datos.
        '''
        try:
            print('login_database')
            return self.mysql.connection.cursor()
        except mysql.connector.Error as error:
            print('Login database Error: ' + str(error))