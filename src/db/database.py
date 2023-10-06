import mysql.connector

# Decouple
from decouple import config

# Utils
from src.utils.get_category import get_category

MELI_API_URL = "https://api.mercadolibre.com"

class Database():
    def __init__(self):
        '''
        Configuración de la base de datos MySQL
        '''
        print('[ETL] Inicializando base de datos...')

        # Config session
        self.config = {
            'user': config('USER'),
            'host': config('HOST'),
            'password': config('PASSWD'),
            'database': config('DATABASE'),
            'connect_timeout': 60
        }
        self.mysql = None

    #Config Access
    def login_database(self) -> 'mysql.connector.cursor':
        '''
        Iniciamos una conexion a la base de datos.
        '''
        try:
            print('login_database')
            self.mysql = mysql.connector.connect(**self.config)
            return self.mysql.cursor()
        except mysql.connector.Error as error:
            print('Login database Error: ' + str(error))
    
    def logout_database(self):
        '''
        Cerramos la conexion a la base de datos.
        '''
        if self.mysql:
            self.mysql.close()

    # SELECTS
    def get_category(self, category_id: str) -> list:
        '''
        Obtenemos una categoria de la base de datos.
        '''
        try:
            ncursor = self.login_database()
            query = "SELECT * FROM Categories WHERE k_categories = %s"
            ncursor.execute(query, (category_id,))
            category = ncursor.fetchone()
            return category, True if category else False
        except mysql.connector.Error as error:
            print('Error get_category: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()

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
        finally:
            self.logout_database()
        
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
        finally:
            self.logout_database()

    # INSERTS
    def insert_sellers(self, seller: dict, location: str):
        '''
        Insertamos los vendedores en la base de datos.
        Args:
            - k_seller: int
            - name: str
            - rating: float
        '''
        try:
            ncursor = self.login_database()
            # Debug LOG
            print(f"""[DEBUG]|DB - insert_sellers: {(
                seller['id'], 
                seller['nickname'], 
                seller['seller_reputation']['transactions']['ratings']['positive'], 
                location
            )}""")

            query = "INSERT INTO Sellers VALUES (%s, %s, %s, %s)"
            ncursor.execute(query, (
                seller['id'], 
                seller['nickname'], 
                seller['seller_reputation']['transactions']['ratings']['positive'], 
                location
                ))
            self.mysql.commit()
            return f"Vendedor: {seller['nickname']} añadido satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error insert_sellers: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()

    def insert_categories(self, category: dict):
        '''
        Insertamos las categorias en la base de datos.
        Args:
            - k_category: str
            - name: str
        '''
        try:
            ncursor = self.login_database()
            # Debug LOG
            print(f"[DEBUG]|DB - insert_categories: {category}")

            query = "INSERT INTO Categories VALUES (%s, %s)"
            ncursor.execute(query, (category['id'], category['name']))
            self.mysql.commit()
            return f"Categoria: {category['name']} añadida satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error insert_categories: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()

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
            # Debug LOG
            print(f"[DEBUG]|DB - insert_products: {product['id'], product['title'], product['price'], product['condition'], product['category_id']}")
            category , success = self.get_category(product['category_id'])
            print(f"[DEBUG]|DB - insert_products/get_category: {category}, {success}]")
            if not success:
                category = get_category(MELI_API_URL, product['category_id'])
                print(f"[DEBUG]|DB - insert_products/get_category: {category}]")
                message, success= self.insert_categories(category)
                print(f"[DEBUG]|DB - insert_products/insert_categories: {message}, {success}]")
                if not success:
                    return message, success

            ncursor = self.login_database()
            query = "INSERT INTO Products VALUES (%s, %s, %s, %s, %s)"
            ncursor.execute(query, (product['id'], product['title'], product['price'], product['condition'], product['category_id']))
            self.mysql.commit()
            return f"Producto: {product['title']} añadido satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error insert_products: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()

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
            # Debug LOG
            print(f"[DEBUG]|DB - insert_product_details: {details}")

            query = "INSERT INTO Product_Details VALUES (NULL, %s, %s, %s, %s, %s)"
            ncursor.execute(query, (
                details['date'], 
                details['amount_sold'], 
                details['available_quantity'],
                details['k_product'], 
                details['k_seller']
                ))
            self.mysql.commit()
            return f"Producto: {details['product_id']} añadido satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error insert_product_details: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()

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
            # Debug LOG
            print(f"[DEBUG]|DB - insert_locations: {location}")

            query = "INSERT INTO Locations VALUES (%s, %s, %s)"
            ncursor.execute(query, (location['id'], location['state'], location['country']))
            self.mysql.commit()
            return f"Ubicacion: {location['id']} añadida satisfactoriamente.", True
        except mysql.connector.Error as error:
            print('Error insert_locations: ' + str(error))
            return [[], False]
        finally:
            self.logout_database()