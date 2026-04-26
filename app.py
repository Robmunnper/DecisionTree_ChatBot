import streamlit as st
import pandas as pd
import mysql.connector
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chatbot Médico", layout="wide")
st.title("Asistente Médico con Árboles de Decisión")

@st.cache_data
def cargar_datos():
    conexion = mysql.connector.connect(
        host="localhost", user="root", password="", database="chatbot_cbd"
    )
    df = pd.read_sql("SELECT * FROM historial_pacientes;", conexion)
    conexion.close()
    
    
    for col in ['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing']:
        df[col] = df[col].map({'Yes': 1, 'No': 0})
    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    df['Blood_Pressure'] = df['Blood_Pressure'].map({'Low': 0, 'Normal': 1, 'High': 2})
    df['Cholesterol_Level'] = df['Cholesterol_Level'].map({'Low': 0, 'Normal': 1, 'High': 2})
    return df


@st.cache_resource
def entrenar_modelo(df):
    X = df[['Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing', 'Age', 'Gender', 'Blood_Pressure', 'Cholesterol_Level']]
    y = df['Disease']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    
    arbol = DecisionTreeClassifier(random_state=42, max_depth=5) 
    arbol.fit(X_train, y_train)
    
    predicciones_examen = arbol.predict(X_test)
    precision = accuracy_score(y_test, predicciones_examen)
    reporte = classification_report(y_test, predicciones_examen, output_dict=True, zero_division=0)
    
    return arbol, X.columns, precision, reporte

try:
    df = cargar_datos()
    arbol, columnas, precision_modelo, reporte_modelo = entrenar_modelo(df)
    
    st.sidebar.header(" Responde paso a paso")
    st.sidebar.write("Responde una pregunta para desbloquear la siguiente.")

    fiebre_val, tos_val, fatiga_val, dif_resp_val = 0, 0, 0, 0
    edad_val, genero_val, presion_val, colest_val = 25, 0, 1, 1
    pasos_completados = 0

    fiebre = st.sidebar.selectbox("1. ¿Tienes fiebre?", ["Sí", "No"], index=None, placeholder="Elige...")
    if fiebre is not None:
        fiebre_val = 1 if fiebre == "Sí" else 0
        pasos_completados += 1

    if pasos_completados >= 1:
        tos = st.sidebar.selectbox("2. ¿Tienes tos?", ["Sí", "No"], index=None, placeholder="Elige...")
        if tos is not None:
            tos_val = 1 if tos == "Sí" else 0
            pasos_completados += 1

    if pasos_completados >= 2:
        fatiga = st.sidebar.selectbox("3. ¿Sientes fatiga?", ["Sí", "No"], index=None, placeholder="Elige...")
        if fatiga is not None:
            fatiga_val = 1 if fatiga == "Sí" else 0
            pasos_completados += 1

    if pasos_completados >= 3:
        dif_resp = st.sidebar.selectbox("4. ¿Dificultad al respirar?", ["Sí", "No"], index=None, placeholder="Elige...")
        if dif_resp is not None:
            dif_resp_val = 1 if dif_resp == "Sí" else 0
            pasos_completados += 1

    if pasos_completados >= 4:
        edad_str = st.sidebar.text_input("5. ¿Cuál es tu edad?", placeholder="Escribe tu edad y pulsa Enter")
        if edad_str.isdigit():
            edad_val = int(edad_str)
            pasos_completados += 1

    if pasos_completados >= 5:
        genero = st.sidebar.selectbox("6. Género", ["Hombre", "Mujer"], index=None, placeholder="Elige...")
        if genero is not None:
            genero_val = 1 if genero == "Hombre" else 0
            pasos_completados += 1

    if pasos_completados >= 6:
        presion = st.sidebar.selectbox("7. Presión Arterial", ["Baja", "Normal", "Alta"], index=None, placeholder="Elige...")
        if presion is not None:
            presion_val = {"Baja": 0, "Normal": 1, "Alta": 2}[presion]
            pasos_completados += 1

    if pasos_completados >= 7:
        colesterol = st.sidebar.selectbox("8. Colesterol", ["Bajo", "Normal", "Alto"], index=None, placeholder="Elige...")
        if colesterol is not None:
            colest_val = {"Bajo": 0, "Normal": 1, "Alto": 2}[colesterol]
            pasos_completados += 1

    sintomas_usuario = [[fiebre_val, tos_val, fatiga_val, dif_resp_val, edad_val, genero_val, presion_val, colest_val]]

    prediccion = arbol.predict(sintomas_usuario)[0]
    
    if pasos_completados == 8:
        st.success(f"###  Diagnóstico Final: **{prediccion}**")
    else:
        st.info(f" Has respondido {pasos_completados} de 8 preguntas. Continúa en el menú para ver tu diagnóstico final. Abajo puedes ver cómo el algoritmo empieza a deducir el resultado.")
    
    st.write("---")
    st.subheader(" Visualización del Árbol de Decisión en Tiempo Real")
    
    camino_nodos = arbol.decision_path(sintomas_usuario).indices
    
    fig, ax = plt.subplots(figsize=(30, 15), dpi=150)
    
    nodos_dibujados = plot_tree(arbol, feature_names=columnas, class_names=arbol.classes_, 
                                filled=True, rounded=True, ax=ax, fontsize=8)
    
    for i, cajita in enumerate(nodos_dibujados):
        fondo_caja = cajita.get_bbox_patch()
        if fondo_caja is not None:
            if i in camino_nodos:
                fondo_caja.set_edgecolor('red')
                fondo_caja.set_linewidth(3) 
                fondo_caja.set_alpha(1.0)
                cajita.set_alpha(1.0) 
            else:
                fondo_caja.set_alpha(0.15) 
                cajita.set_alpha(0.15) 
    
    st.pyplot(fig, use_container_width=True)

    st.write("---")
    st.subheader(" Evaluación del Modelo")
    
    st.metric(label="Precisión General ", value=f"{precision_modelo * 100:.1f}%")
    
    with st.expander("Ver Reporte de Clasificación Detallado"):
        st.write("Este reporte muestra el rendimiento del modelo evaluando el 15% de datos de prueba separados del entrenamiento inicial:")
        df_reporte = pd.DataFrame(reporte_modelo).transpose()
        st.dataframe(df_reporte.style.format("{:.2f}"))

except Exception as e:
    st.error(f"Error: Asegúrate de que el servidor MariaDB está encendido y el nombre de la tabla es correcto. Detalle: {e}")