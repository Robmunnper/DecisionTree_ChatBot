import pandas as pd
import mysql.connector

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


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



# 1. Silenciamos el aviso de Pandas para que no moleste en la terminal
import warnings
warnings.filterwarnings('ignore')

# 2. Reemplazamos los 'Yes'/'No' por 1 y 0 en las columnas de síntomas
columnas_sintomas = ['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing']
for col in columnas_sintomas:
    df[col] = df[col].map({'Yes': 1, 'No': 0})

# 3. Convertimos el género ('Male' = 1, 'Female' = 0)
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})

# 4. Convertimos variables como Presión Arterial y Colesterol a números
# Asumimos: Low=0, Normal=1, High=2
df['Blood_Pressure'] = df['Blood_Pressure'].map({'Low': 0, 'Normal': 1, 'High': 2})
df['Cholesterol_Level'] = df['Cholesterol_Level'].map({'Low': 0, 'Normal': 1, 'High': 2})

print("\n✨ Así quedan los datos listos para el árbol (solo números):")
print(df.head())


