import pandas as pd
import mysql.connector

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


conexion = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="",
    database="chatbot_cbd"
)

query = "SELECT * FROM historial_pacientes;" 
df = pd.read_sql(query, conexion)
print(df.head())



import warnings
warnings.filterwarnings('ignore')

columnas_sintomas = ['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing']
for col in columnas_sintomas:
    df[col] = df[col].map({'Yes': 1, 'No': 0})

df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})

df['Blood_Pressure'] = df['Blood_Pressure'].map({'Low': 0, 'Normal': 1, 'High': 2})
df['Cholesterol_Level'] = df['Cholesterol_Level'].map({'Low': 0, 'Normal': 1, 'High': 2})

print("\n Así quedan los datos listos para el árbol :")
print(df.head())



X = df[['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing', 'Age', 'Gender', 
        'Blood_Pressure', 'Cholesterol_Level']]

y = df['Disease']

X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(random_state=42)

arbol.fit(X_entrenamiento, y_entrenamiento)

print("¡Árbol de decisión entrenado con éxito!")


paciente_prueba = [[1, 1, 0, 1, 25, 1, 1, 1]] 
prediccion = arbol.predict(paciente_prueba)

print(f" Predicción : {prediccion[0]}")

def iniciar_chatbot():
    print("\n" + "="*50)
    print(" Soy tu asistente médico virtual.")
    print("Voy a hacerte algunas preguntas para darte un diagnóstico")
    print("="*50 + "\n")

    map_sintomas = {'si': 1, 'no': 0}
    map_genero = {'hombre': 1, 'mujer': 0}
    map_niveles = {'bajo': 0, 'normal': 1, 'alto': 2}

    try:
        fiebre = map_sintomas[input("¿Tienes fiebre? (si/no): ").strip().lower()]
        tos = map_sintomas[input("¿Tienes tos? (si/no): ").strip().lower()]
        fatiga = map_sintomas[input("¿Sientes fatiga? (si/no): ").strip().lower()]
        dif_resp = map_sintomas[input("¿Tienes dificultad para respirar? (si/no): ").strip().lower()]
        
        edad = int(input("¿Cuál es tu edad?: ").strip())
        genero = map_genero[input("¿Cuál es tu género? (hombre/mujer): ").strip().lower()]
        
        presion = map_niveles[input("¿Cómo es tu presión arterial? (bajo/normal/alto): ").strip().lower()]
        colesterol = map_niveles[input("¿Cómo es tu nivel de colesterol? (bajo/normal/alto): ").strip().lower()]

        
        sintomas_usuario = [[fiebre, tos, fatiga, dif_resp, edad, genero, presion, colesterol]]

        print("\n Analizando tus síntomas...")
        prediccion = arbol.predict(sintomas_usuario)
        
        print("\n" + "="*50)
        print(f"🩺 DIAGNÓSTICO : Según mis datos, podrías tener {prediccion[0]}.")
        print("="*50 + "\n")

    except KeyError:
        print("\n Error: No he entendido alguna respuesta. Por favor, responde exactamente con las opciones dadas (si/no, etc.).")
    except ValueError:
        print("\n Error: La edad debe ser un número entero.")

iniciar_chatbot()