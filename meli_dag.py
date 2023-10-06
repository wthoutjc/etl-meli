import requests

# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Database
from src.db.database import Database
database = Database()

# Decouple
from decouple import config

# Utils
from src.utils.get_auth import get_auth

MELI_API_URL = "https://api.mercadolibre.com"
APP_ID = config('APP_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

# Definir las funciones de extracción
auth_token = get_auth(APP_ID, CLIENT_SECRET, MELI_API_URL)

# 1. Extraer categorías
def extraer_categorias():
    search_url = f'{MELI_API_URL}/sites/MCO/categories'
    search_response = requests.get(search_url)
    categories = search_response.json()
    for category in categories:
        database.insert_categories(category)

def extraer_productos():
    categories, success = database.get_categories()

    if success:
        for category in categories:
            search_url = f'{MELI_API_URL}/sites/MCO/search?category={category[0]}'
            search_response = requests.get(search_url)
            top_5_products = sorted(search_response.json()['results'], key=lambda product: product['sold_quantity'], reverse=True)[:5]

            for product in top_5_products:
                message , sucess = database.insert_products(product)
                print(f"[DEBUG] . extraer_productos/insert_products: {message}, {sucess}]")

                location = {
                    "id": product['seller_address']['city']['name'],
                    "state": product['seller_address']['state']['name'],
                    "country": product['seller_address']['country']['name']
                }
                message , sucess = database.insert_locations(location)
                print(f"[DEBUG] . extraer_productos/insert_locations: {message}, {sucess}]")

                message , sucess = database.insert_sellers(product['seller'], product['seller_address']['city']['name'])
                print(f"[DEBUG] . extraer_productos/insert_sellers: {message}, {sucess}]")

                details = {
                    "date": datetime.now(),
                    "amount_sold": product['sold_quantity'],
                    "available_quantity": product['available_quantity'],
                    "k_product": product['id'],
                    "k_seller": product['seller']['id']
                }
                message , sucess = database.insert_product_details(details)
                print(f"[DEBUG] . extraer_productos/insert_product_details: {message}, {sucess}]")

                

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'extraccion_mercadolibre',
    default_args=default_args,
    description='Un DAG para extraer datos de la API de Mercado Libre',
    schedule_interval=timedelta(days=1),
)

# Definir las tareas
tarea_extraer_productos = PythonOperator(
    task_id='extraer_productos',
    python_callable=extraer_productos,
    dag=dag,
)

tarea_extraer_categorias = PythonOperator(
    task_id='extraer_categorias',
    python_callable=extraer_categorias,
    dag=dag,
)


# Definir las dependencias
tarea_extraer_categorias >> tarea_extraer_productos
