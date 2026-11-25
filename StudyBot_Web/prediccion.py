"""Inferencia exclusivamente: este módulo nunca entrena un modelo."""
from pathlib import Path
import math
import joblib
import numpy as np
from configuracion import VARIABLES, ETIQUETAS


def cargar_modelo(ruta=None):
    ruta = Path(ruta) if ruta else Path(__file__).with_name('studybot_model.joblib')
    if not ruta.is_file():
        raise FileNotFoundError(
            'Falta studybot_model.joblib. Ejecuta primero exportar_modelo.py '
            'con el Dataset v1.0.csv original, según el README.'
        )
    paquete = joblib.load(ruta)
    if paquete['variables'] != VARIABLES:
        raise ValueError('Las columnas del modelo no coinciden con la aplicación.')
    modelo = paquete['modelo']
    if modelo.n_features_in_ != len(VARIABLES):
        raise ValueError('El modelo tiene un número de variables incompatible.')
    if set(modelo.classes_) != {0, 1}:
        raise ValueError('El modelo debe clasificar las clases 0 y 1.')
    return modelo


def validar_entradas(valores):
    if set(valores) != set(VARIABLES):
        raise ValueError('Envía exactamente las once variables del formulario.')
    fila = []
    for variable in VARIABLES:
        try:
            valor = float(valores[variable])
        except (TypeError, ValueError):
            raise ValueError(f'{variable}: introduce un valor numérico, 0 o 1.') from None
        if not math.isfinite(valor) or valor not in (0, 1):
            raise ValueError(f'{variable}: solo se permiten 0 y 1.')
        fila.append(int(valor))
    return np.array([fila], dtype=int)


def predecir(valores, modelo):
    fila = validar_entradas(valores)
    clase = int(modelo.predict(fila)[0])
    if clase not in ETIQUETAS:
        raise ValueError('El modelo devolvió una clase desconocida.')
    return ETIQUETAS[clase]
