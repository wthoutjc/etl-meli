from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

MELI_URL = "https://api.mercadolibre.com/sites/MLA/"

# Definir las funciones de extracción
def extraer_vendedores():
    # Código para extraer datos de vendedores de la API de Mercado Libre
    pass

def extraer_categorias():
    # Código para extraer datos de categorías de la API de Mercado Libre
    pass

def extraer_ubicaciones():
    # Código para extraer datos de ubicaciones de la API de Mercado Libre
    pass

def extraer_ventas():
    # Código para extraer datos de ventas de la API de Mercado Libre
    pass

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
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
tarea_extraer_vendedores = PythonOperator(
    task_id='extraer_vendedores',
    python_callable=extraer_vendedores,
    dag=dag,
)

tarea_extraer_categorias = PythonOperator(
    task_id='extraer_categorias',
    python_callable=extraer_categorias,
    dag=dag,
)

tarea_extraer_ubicaciones = PythonOperator(
    task_id='extraer_ubicaciones',
    python_callable=extraer_ubicaciones,
    dag=dag,
)

tarea_extraer_ventas = PythonOperator(
    task_id='extraer_ventas',
    python_callable=extraer_ventas,
    dag=dag,
)

# Definir las dependencias
tarea_extraer_vendedores >> tarea_extraer_categorias >> tarea_extraer_ubicaciones >> tarea_extraer_ventas
