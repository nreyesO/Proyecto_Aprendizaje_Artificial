# StudyBot de modelo a aplicación web

Aplicación Flask que utiliza el árbol de decisión de la entrega anterior para clasificar un lugar como **APTO** o **NO APTO** para estudiar durante 30 minutos. El formulario recibe las mismas once variables binarias del Dataset v1.0.

## Ejecutar la aplicación

Requisitos: Python 3.13 y pip. Abre una terminal en la carpeta principal del proyecto, donde se encuentran los archivos app.py y requirements.txt, y ejecuta los siguientes comandos:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000 en el navegador. Completa los once campos del formulario introduciendo 0 si el lugar no presenta la característica indicada o 1 si la presenta. Pulsa **Evaluar lugar** para obtener la clasificación APTO o NO APTO.

Para detener el servidor, presiona Ctrl+C en la terminal. Para volver a iniciarlo, ejecuta `python app.py`. No es necesario entrenar ni exportar nuevamente el modelo.

Opcionalmente, antes de instalar, crea un entorno virtual con `python -m venv .venv` y actívalo en PowerShell con `.\.venv\Scripts\Activate.ps1`.

El archivo `studybot_model.joblib` ya contiene el modelo entrenado. El servidor debe poder leerlo en la misma carpeta que `app.py`.

## Archivos principales

| Archivo | Función |
| --- | --- |
| `app.py` | Iniciar Flask, cargar el modelo y atender GET y POST |
| `templates/index.html` | Formulario y resultado de la predicción |
| `studybot_model.joblib` | Árbol entrenado y metadatos de sus entradas |
| `prediccion.py` | Validar los valores y ejecutar predict |
| `configuracion.py` | Nombres y orden de las variables y etiquetas |
| `requirements.txt` | Versiones de las bibliotecas |
| `exportar_modelo.py` | Reconstruir el entrenamiento del notebook y guardar el modelo |
| `probar_aplicacion.py` | Ejecutar tres predicciones y validar las rutas de Flask |
| `EVIDENCIA.md` | Entradas, resultados e interpretación de las pruebas |
| `evidencia_pruebas.json` | Evidencia estructurada y huella del modelo utilizado |
| `exportacion.json` | Partición, exactitud y comprobación de la recarga |
| `Dataset v1.0.csv` | Dataset original de 65 registros |
| `Proyecto_Aprendizaje_Artificial.ipynb` | Notebook de la entrega anterior |

## Variables y preprocesamiento

El orden de entrada es:

```text
silencio, sombra, aire_acondicionado, soporte_para_trabajar,
asientos, asientos_comodos, enchufes, flujo_personas,
banos_cerca, cafeteria_cerca, internet_wifi
```

Todas las variables admiten únicamente 0 y 1 conforme a la codificación original. `Lugar` es un identificador descriptivo y `Target` es la respuesta: ninguno entra al modelo como predictor. `Target=0` significa NO APTO y `Target=1` significa APTO.

El modelo utiliza las once variables binarias originales del Dataset v1.0, sin aplicar normalización, escalado ni imputación de datos. La aplicación valida los valores ingresados y conserva el orden de las variables utilizado durante el entrenamiento. No se incorporan variables adicionales, como temperatura o nivel de ruido continuo, debido a que no forman parte del modelo original.

## Guardado del modelo

El notebook original contiene el entrenamiento, pero no un archivo serializado. Para obtenerlo se reconstruyó el árbol con el mismo CSV, `DecisionTreeClassifier(random_state=42)` y la misma partición: `train_test_split(test_size=0.20, random_state=42)`, sin estratificación. Se utilizaron 52 registros para entrenamiento y 13 para prueba.

Para repetir esta exportación por separado:

```powershell
python exportar_modelo.py "Dataset v1.0.csv"
```

El script guarda el modelo con `joblib.dump`, lo recarga con `joblib.load` y comprueba que sus predicciones en los 13 registros de prueba sean idénticas antes y después del guardado. El árbol alcanzó 13/13 aciertos en esta partición; el conjunto es pequeño y este resultado no garantiza el mismo desempeño con lugares nuevos.


La exportación es una operación de preparación. **El servidor no ejecuta el script de entrenamiento ni llama a fit.**

## Flujo de una predicción

1. Al iniciar Flask, `cargar_modelo` abre el archivo joblib y verifica sus columnas y clases.
2. El navegador envía los once campos mediante POST a `/`.
3. `validar_entradas` rechaza campos faltantes o adicionales, texto, valores no finitos y números distintos de 0 y 1. La ruta rechaza también campos duplicados.
4. `predecir` organiza una fila en el orden original y llama a `modelo.predict`.
5. La clase 0 o 1 se convierte en NO APTO o APTO y se muestra en la página.

Las comprobaciones de entrada y la traducción de etiquetas no deciden si el lugar es apto: esa clasificación la produce el árbol guardado.

## Repetir las pruebas

```powershell
python probar_aplicacion.py
```

Primero se prueban tres combinaciones con la función de predicción y después se envían a la ruta POST mediante el cliente de pruebas de Flask. Se comprueba que ambos resultados coincidan y que la página responda con HTTP 200. También se prueban entradas inválidas y se bloquea `fit` durante las peticiones para detectar cualquier intento de entrenamiento.

El script actualiza `EVIDENCIA.md` y `evidencia_pruebas.json`. Las dos primeras combinaciones difieren en una sola variable y producen clases distintas. Son casos sintéticos para estudiar una frontera discreta del clasificador, no mediciones de nuevos lugares. La tercera combinación es diferente de ambas.

Para comprobar el arranque y reinicio reales, con el puerto 5000 libre:

```powershell
python verificar_reinicio.py
```

Esta comprobación inicia `python app.py`, verifica la página y las tres predicciones por HTTP, detiene el proceso y repite el procedimiento. Ambos arranques respondieron con HTTP 200 y las tres predicciones esperadas. Los resultados están en `verificacion_reinicio.json`. La comprobación se realizó con las dependencias ya instaladas en Python 3.13; no equivale a una instalación en un equipo limpio.

## Repositorio del proyecto

El proyecto StudyBot forma parte de la actividad desarrollada en la materia de Aprendizaje Artificial. El repositorio contiene el dataset original, el notebook de entrenamiento, el modelo guardado, el código fuente de la aplicación web y las evidencias de las pruebas realizadas.

Repositorio:
https://github.com/nreyesO/Proyecto_Aprendizaje_Artificial
