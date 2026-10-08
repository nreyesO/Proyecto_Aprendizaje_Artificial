# Puede un robot aprender dónde trabajar?

Proyecto de primera evaluación parcial de Aprendizaje Artificial. Equipo 2.

## Información académica

- **Integrantes:** Nora Azucena Reyes Ortiz y Karla Estefanía Tovar Rodríguez.
- **Profesor:** Pedro César Santana Mancilla.
- **Materia:** Aprendizaje Artificial.
- **Maestría:** Maestría en Tecnologías de Internet.

## Descripción del problema

El proyecto busca clasificar un lugar como "Apto" o "No apto" para estudiar durante 30 minutos, a partir de características del entorno codificadas con valores de 0 y 1.

Se implementó un clasificador K-Nearest Neighbors (KNN) desde cero utilizando distancia euclidiana y votación mayoritaria. Después se experimentó con diferentes valores de k y se compararon sus resultados con KNN de scikit-learn y con un árbol de decisión, el modelo asignado al equipo 2.

## Archivos necesarios

- `Proyecto_AA_b (2)(1).ipynb`: notebook con el análisis, código, gráficas y resultados.
- `Dataset v1.0.csv`: versión del dataset utilizada en los experimentos.
- `README.md`: descripción e instrucciones del proyecto.


## Dataset utilizado

Se utilizó el **Dataset v1.0**, con las siguientes características:

- **Registros:** 65 lugares.
- **Distribución de clases:** 34 Aptos (52.31 %) y 31 No aptos (47.69 %).
- **Características predictoras:** 11 variables binarias, codificadas con 0 y 1.
- **Variable objetivo:** `Target`, donde 0 significa No apto y 1 significa Apto.
- **Identificador descriptivo:** `Lugar`, excluido del entrenamiento junto con la variable objetivo al construir X.
- **Archivo:** `Dataset v1.0.csv`.
- **Publicación en Kaggle:** [Dataset v1.0](https://www.kaggle.com/datasets/schiaffino89/lugares-aptos-para-trabajar)

Se conservó la misma división en todos los experimentos: **52 registros de entrenamiento (80 %) y 13 de prueba (20 %)**, con `random_state=42`.

## Requisitos

El notebook utiliza Python 3 y las bibliotecas NumPy, Pandas, Matplotlib, Seaborn y scikit-learn. Se ejecuta en Google Colab.

## Instrucciones de ejecución

### Google Colab

1. Descargar el notebook y `Dataset v1.0.csv` desde el repositorio.
2. Abrir Google Colab e importar el notebook.
3. Subir `Dataset v1.0.csv` al directorio de trabajo de la sesión desde el panel de archivos. Conservar exactamente ese nombre, ya que el código lo utiliza para cargar los datos.
4. Si falta alguna dependencia, ejecutar en una celda:

   ```python
   %pip install numpy pandas matplotlib "seaborn>=0.13" scikit-learn
   ```

5. Ejecutar todas las celdas en orden, desde la primera hasta la última.
6. Consultar las tablas, gráficas y explicaciones generadas.

El CSV debe volver a cargarse si se inicia una nueva sesión de Colab.

## Metodología

1. Analizar las variables y el balance de clases.
2. Implementar KNN desde cero: calcular distancias, ordenarlas, seleccionar los k vecinos y votar por la clase mayoritaria.
3. Dividir el dataset en entrenamiento y prueba.
4. Evaluar k = 1, 3, 5, 7 y 9.
5. Comparar KNN propio con `KNeighborsClassifier` para todos los valores de k.
6. Comparar ambos KNN con k = 3 frente a `DecisionTreeClassifier`.

La métrica utilizada fue la **exactitud (accuracy)**: proporción de predicciones correctas, expresada como porcentaje.

## Principales resultados

### Experimentación con KNN propio

| k | Exactitud de entrenamiento | Exactitud de prueba | Aciertos en prueba |
|---|---|---|---|
| 1 | 100.00 % | 84.62 % | 11 / 13 |
| 3 | 94.23 % | 84.62 % | 11 / 13 |
| 5 | 94.23 % | 76.92 % | 10 / 13 |
| 7 | 96.15 % | 76.92 % | 10 / 13 |
| 9 | 94.23 % | 76.92 % | 10 / 13 |

Se eligió **k = 3** para la comparación final: igualó la mejor exactitud de prueba del KNN propio y basó la decisión en tres vecinos. Aumentar k no mejoró los resultados de prueba.

### Comparación de KNN propio y scikit-learn

| k | Exactitud de prueba: KNN propio | Exactitud de prueba: scikit-learn |
|---|---|---|
| 1 | 84.62 % | 84.62 % |
| 3 | 84.62 % | 76.92 % |
| 5 | 76.92 % | 76.92 % |
| 7 | 76.92 % | 69.23 % |
| 9 | 76.92 % | 76.92 % |

Ambas implementaciones mostraron un desempeño cercano. Las diferencias podrían relacionarse con la selección de vecinos cuando existen distancias empatadas; esta explicación no fue comprobada mediante una comparación de los vecinos seleccionados.

### Comparación final de modelos

| Modelo | Exactitud de entrenamiento | Exactitud de prueba | Aciertos en prueba |
|---|---|---|---|
| KNN propio (k = 3) | 94.23 % | 84.62 % | 11 / 13 |
| KNN de scikit-learn (k = 3) | 98.08 % | 76.92 % | 10 / 13 |
| árbol de decisión | 100.00 % | 100.00 % | 13 / 13 |

El árbol de decisión clasificó correctamente los 6 lugares No aptos y los 7 Aptos del conjunto de prueba. Su matriz de confusión fue:

| Clase real / Clase predicha | No apto (0) | Apto (1) |
|---|---|---|
| No apto (0) | 6 | 0 |
| Apto (1) | 0 | 7 |

## Conclusiones y limitaciones

El árbol de decisión obtuvo el mejor resultado en la división evaluada. Las características binarias podrían favorecer reglas de clasificación basadas en combinaciones especificas de variables. KNN también logró clasificar la mayoría de los lugares, y sus resultados cambiaron al modificar k.

El dataset es pequeño y la evaluación se realizó con solo 13 registros de prueba. Además, se utilizó ese mismo conjunto para comparar valores de k, por lo que sería conveniente validar la selección con validación cruzada y evaluar después con datos independientes. El 100 % obtenido por el árbol no garantiza el mismo desempeño con nuevos lugares.
