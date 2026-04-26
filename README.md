# Manual de Instalación del Asistente Médico con Árbol de Decisión

1. Requisitos previos
Para el correcto funcionamiento de la aplicación, es necesario contar con el siguiente software instalado en el sistema:

* Python 3.10 o superior.
* Servidor de base de datos MariaDB o MySQL.
* Aplicación HeidiSQL para la gestión de la base de datos.

2. Instalación de dependencias de Python
Es necesario instalar las librerías de Python que permiten la ejecución de la interfaz, el procesamiento de datos y la conexión con el servidor. Ejecute el siguiente comando en su terminal:

`python -m pip install streamlit pandas mysql-connector-python scikit-learn matplotlib`

3. Configuración de la base de datos en HeidiSQL
Siga estos pasos para preparar el entorno de datos:

* Inicie su sesión local en HeidiSQL.

* Cree una nueva base de datos desde HeidiSQL

* Crear una nueva tabla en la base de datos ya creada y ejecutar la siguiente consulta para crear la tabla según el csv proporcionado

`CREATE TABLE historial_pacientes (
    Disease VARCHAR(100),
    Fever VARCHAR(10),
    Cough VARCHAR(10),
    Fatigue VARCHAR(10),
    Difficulty_Breathing VARCHAR(10),
    Age INT,
    Gender VARCHAR(20),
    Blood_Pressure VARCHAR(20),
    Cholesterol_Level VARCHAR(20),
    Outcome_Variable VARCHAR(20)
);`

*Importar el archivo CSV proporcionado  (Diseases) utilizando la herramienta de importación de archivos de texto y revisar los datos de la tabla, comprobando que se ha importado el csv correctamente.

*En el código de los módulos app.py y database.py a la hora de hacer la conexion con la BD y cargar los datos, en el código, poner los nombres que habeis usado a la hora de gestionar la BD( nombre de la tabla, usuario, contraseña...)

4. Estructura de archivos del proyecto
El directorio de trabajo debe contener los siguientes archivos fundamentales para garantizar la integridad del sistema:
* app.py: Contiene el código de la interfaz de Streamlit y el entrenamiento del modelo.
* database.py: Versión del asistente para ejecución en consola o terminal.
* Diseases.csv: Archivo de datos fuente.


5. Ejecución de la aplicación
Una vez configurada la base de datos y las dependencias, inicie la aplicación web ejecutando el siguiente comando en la terminal desde la ruta del proyecto:

`python -m streamlit run app.py`

Al ejecutarlo, se abrirá automáticamente una pestaña en su navegador predeterminado con la interfaz del chatbot médico.

6. Información del modelo y métricas
El sistema implementa las siguientes capacidades de análisis de datos:
* División de datos en 85% para entrenamiento y 15% para pruebas.
* Cálculo de precisión (Accuracy) en tiempo real mediante la librería scikit-learn.
* Generación de un reporte de clasificación detallado para las enfermedades incluidas.
* Visualización dinámica del árbol de decisión con resaltado del camino lógico seguido durante el diagnóstico.

