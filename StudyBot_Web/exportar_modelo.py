"""Reconstruye el árbol del notebook y lo exporta, fuera del servidor web."""
import argparse
import hashlib
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from configuracion import VARIABLES

BASE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path, help='Ruta del Dataset v1.0.csv original')
    args = parser.parse_args()
    df = pd.read_csv(args.csv)
    columnas = df.drop(columns=['Lugar', 'Target']).columns.tolist()
    if columnas != VARIABLES:
        raise ValueError(f'Las columnas o su orden difieren del original: {columnas}')
    if len(df) != 65 or df[VARIABLES + ['Target']].isna().any().any():
        raise ValueError('Se esperan los 65 registros completos del Dataset v1.0.')
    if not df[VARIABLES + ['Target']].isin([0, 1]).all().all():
        raise ValueError('Las características y Target deben ser binarias.')
    X = df.drop(columns=['Lugar', 'Target']).values
    y = df['Target'].values
    # Mismo orden, semilla, partición y parámetros del notebook anterior.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    modelo = DecisionTreeClassifier(random_state=42)
    modelo.fit(X_train, y_train)
    paquete = {'modelo': modelo, 'variables': VARIABLES,
               'preprocesamiento': 'Variables binarias originales; sin escalado',
               'sklearn_version': sklearn.__version__}
    destino = BASE / 'studybot_model.joblib'
    joblib.dump(paquete, destino)
    recargado = joblib.load(destino)['modelo']
    np.testing.assert_array_equal(modelo.predict(X_test), recargado.predict(X_test))
    informe = {
        'origen': 'Reconstrucción del árbol del notebook de la entrega anterior',
        'dataset_sha256': hashlib.sha256(args.csv.read_bytes()).hexdigest(),
        'registros': len(df), 'entrenamiento': len(X_train), 'prueba': len(X_test),
        'random_state': 42, 'sklearn_version': sklearn.__version__,
        'exactitud_prueba': accuracy_score(y_test, recargado.predict(X_test)),
        'prediccion_tras_recarga': int(recargado.predict(X_test[:1])[0]),
        'predicciones_identicas_tras_recarga': True,
    }
    (BASE / 'exportacion.json').write_text(json.dumps(informe, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(informe, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
