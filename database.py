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


# 5. Separamos los datos
# X son nuestras características (todo menos la enfermedad y el Outcome_Variable)
X = df[['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing', 'Age', 'Gender', 
        'Blood_Pressure', 'Cholesterol_Level']]

# y es lo que queremos predecir (la enfermedad en texto)
y = df['Disease']

# 6. (Opcional pero recomendado) Separamos un pequeño porcentaje de datos para probar si el árbol es bueno
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Creamos el "cerebro" (el árbol de decisión)
arbol = DecisionTreeClassifier(random_state=42)

# 8. Entrenamos el árbol dándole los síntomas y diciéndole qué enfermedad era
arbol.fit(X_entrenamiento, y_entrenamiento)

print("🌳 ¡Árbol de decisión entrenado con éxito!")

# Vamos a hacer una prueba rápida para ver si funciona:
# Simulamos un paciente: Fiebre(1), Tos(1), Fatiga(0), Dif.Respirar(1), Edad(25), Género(1-Hombre), Presión(1-Normal), Colest.(1-Normal)
paciente_prueba = [[1, 1, 0, 1, 25, 1, 1, 1]] 
prediccion = arbol.predict(paciente_prueba)

print(f"🩺 Predicción para el paciente de prueba: {prediccion[0]}")

def iniciar_chatbot():
    print("\n" + "="*50)
    print("🤖 ¡Hola! Soy tu asistente médico virtual.")
    print("Voy a hacerte algunas preguntas para darte un diagnóstico preliminar.")
    print("="*50 + "\n")

    # Diccionarios para traducir las respuestas de texto a números
    map_sintomas = {'si': 1, 'no': 0}
    map_genero = {'hombre': 1, 'mujer': 0}
    map_niveles = {'bajo': 0, 'normal': 1, 'alto': 2}

    try:
        # Preguntamos al usuario y usamos .strip().lower() para limpiar espacios y mayúsculas
        fiebre = map_sintomas[input("¿Tienes fiebre? (si/no): ").strip().lower()]
        tos = map_sintomas[input("¿Tienes tos? (si/no): ").strip().lower()]
        fatiga = map_sintomas[input("¿Sientes fatiga? (si/no): ").strip().lower()]
        dif_resp = map_sintomas[input("¿Tienes dificultad para respirar? (si/no): ").strip().lower()]
        
        edad = int(input("¿Cuál es tu edad?: ").strip())
        genero = map_genero[input("¿Cuál es tu género? (hombre/mujer): ").strip().lower()]
        
        presion = map_niveles[input("¿Cómo es tu presión arterial? (bajo/normal/alto): ").strip().lower()]
        colesterol = map_niveles[input("¿Cómo es tu nivel de colesterol? (bajo/normal/alto): ").strip().lower()]

        # Agrupamos las respuestas en el formato que espera el árbol (una lista dentro de otra lista)
        # El orden debe ser EXACTAMENTE el mismo que usamos al crear la variable X
        sintomas_usuario = [[fiebre, tos, fatiga, dif_resp, edad, genero, presion, colesterol]]

        # Le pedimos al árbol que haga la predicción
        print("\n⏳ Analizando tus síntomas...")
        prediccion = arbol.predict(sintomas_usuario)
        
        print("\n" + "="*50)
        print(f"🩺 DIAGNÓSTICO PRELIMINAR: Según mis datos, podrías tener {prediccion[0]}.")
        print("⚠️ AVISO: Esto es un proyecto académico. ¡Consulta siempre a un médico real!")
        print("="*50 + "\n")

    except KeyError:
        print("\n❌ Error: No he entendido alguna respuesta. Por favor, responde exactamente con las opciones dadas (si/no, etc.).")
    except ValueError:
        print("\n❌ Error: La edad debe ser un número entero.")

# ¡Llamamos a la función para que empiece el chat!
iniciar_chatbot()