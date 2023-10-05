from flask_mysqldb import MySQL
import mysql.connector

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
    
    # SELECTS
    def get_categories(self) -> list:
        '''
        Obtenemos las categorias de la base de datos.
        '''
        try:
            ncursor = self.login_database()
            query = "SELECT * FROM Categories"
            ncursor.execute(query)
            return ncursor.fetchall(), True
        except mysql.connector.Error as error:
            print('Error get_categories: ' + str(error))
            return [[], False]
        
    def get_sellers(self) -> list:
        '''
        Obtenemos los vendedores de la base de datos.
        '''
        try:
            ncursor = self.login_database()
            query = "SELECT * FROM Sellers"
            ncursor.execute(query)
            return ncursor.fetchall(), True
        except mysql.connector.Error as error:
            print('Error get_sellers: ' + str(error))
            return [[], False]

    # INSERTS
    def insert_sellers(self, seller: dict):
        '''
        Insertamos los vendedores en la base de datos.
        Args:
            - k_seller: int
            - name: str
            - rating: float

        '''
        try:
            ncursor = self.login_database()
            query = "INSERT INTO Sellers VALUES (%s, %s, %s, %s)"
            ncursor.execute(query, (
                seller['id'], 
                seller['nickname'], 
                seller['seller_reputation']['transactions']['ratings']['positive'], 
                seller.get('eshop', {}).get('site_id', None)
                ))
        except mysql.connector.Error as error:
            print('Error consultar_presupuestos_vendedor: ' + str(error))
            return [[], False]
    
    def insert_categories(self, category: dict):
        '''
        Insertamos las categorias en la base de datos.
        Args:
            - k_category: str
            - name: str
        '''
        try:
            ncursor = self.login_database()
            query = "INSERT INTO Categories VALUES (%s, %s)"
            ncursor.execute(query, (category['id'], category['name']))
            self.mysql.connection.commit()
            return f"Categoria: {category['name']} añadida satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error consultar_presupuestos_vendedor: ' + str(error))
            return [[], False]
    
    def insert_products(self, product: dict):
        '''
        Insertamos los productos en la base de datos.
        Args:
            - k_product: str
            - name: str
            - price: float
            - condition: str
            - category: str
        '''
        try:
            ncursor = self.login_database()
            query = "INSERT INTO Products VALUES (%s, %s, %s, %s, %s)"
            ncursor.execute(query, (product['id'], product['title'], product['price'], product['condition'], product['category_id']))
            self.mysql.connection.commit()
            return f"Producto: {product['title']} añadido satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error consultar_presupuestos_vendedor: ' + str(error))
            return [[], False]

    def insert_product_details(self, details: dict):
        '''
        Insertamos los detalles de los productos en la base de datos.
        Args:
            - k_product: int (auto increment)
            - date: datetime
            - amount_sold: int
            - available_quantity: int
            - k_product: str
            - k_seller: int
        '''
        try:
            ncursor = self.login_database()
            query = "INSERT INTO ProductDetails VALUES (NULL, %s, %s, %s, %s, %s)"
            ncursor.execute(query, (
                details['date'], 
                details['amount_sold'], 
                details['available_quantity'],
                details['product_id'], 
                details['seller_id']
                ))
            self.mysql.connection.commit()
            return f"Producto: {details['product_id']} añadido satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error consultar_presupuestos_vendedor: ' + str(error))
            return [[], False]
    
    def insert_locations(self, location: dict):
        '''
        Insertamos las ubicaciones en la base de datos.
        Args:
            - department: str PK
            - city: str
            - country: str
        '''
        try:
            ncursor = self.login_database()
            query = "INSERT INTO Locations VALUES (%s, %s, %s)"
            ncursor.execute(query, (location['id'], location['name'], location['type'], location['parent_id']))
            self.mysql.connection.commit()
            return f"Ubicacion: {location['name']} añadida satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error consultar_presupuestos_vendedor: ' + str(error))
            return [[], False]