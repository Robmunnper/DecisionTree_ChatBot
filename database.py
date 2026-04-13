import pandas as pd
import mysql.connector

# Conexión a MariaDB
conexion = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="",
    database="chatbot_cbd"
)

# Extraer los datos a un DataFrame de Pandas
query = "SELECT * FROM historial_pacientes;" 
df = pd.read_sql(query, conexion)
print(df.head())
