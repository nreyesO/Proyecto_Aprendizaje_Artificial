"""Genera evidencia real mediante la función y las rutas de Flask."""
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from configuracion import VARIABLES
from prediccion import cargar_modelo, predecir

BASE = Path(__file__).resolve().parent


def main():
    modelo = cargar_modelo()
    # Buscar dos entradas binarias adyacentes con distinta clasificación.
    # Son casos sintéticos de prueba, no nuevos registros observados.
    espacio = np.array(list(itertools.product([0, 1], repeat=len(VARIABLES))))
    clases = modelo.predict(espacio)
    indice = {tuple(fila): i for i, fila in enumerate(espacio)}
    par = None
    for i, fila in enumerate(espacio):
        for j in range(len(VARIABLES)):
            vecina = fila.copy()
            vecina[j] = 1 - vecina[j]
            k = indice[tuple(vecina)]
            if clases[i] != clases[k]:
                par = (fila, vecina, j)
                break
        if par is not None:
            break
    if par is None:
        raise AssertionError('No se encontró una frontera binaria con este modelo.')
    a, b, cambio = par
    tercera = next(f for f in espacio[::-1] if not np.array_equal(f, a) and not np.array_equal(f, b))
    casos = [dict(zip(VARIABLES, map(int, f))) for f in (a, b, tercera)]
    # Paso 2: probar la función antes de importar/iniciar Flask.
    resultados = [predecir(caso, modelo) for caso in casos]
    from app import app
    from sklearn.tree import DecisionTreeClassifier
    from unittest.mock import patch
    pruebas = []
    with patch.object(DecisionTreeClassifier, 'fit', side_effect=AssertionError('Inferencia intentó entrenar')):
        with app.test_client() as cliente:
            assert cliente.get('/').status_code == 200
            for i, (caso, resultado) in enumerate(zip(casos, resultados), 1):
                respuesta = cliente.post('/', data=caso)
                assert respuesta.status_code == 200
                assert f'<strong>{resultado}</strong>' in respuesta.get_data(as_text=True)
                interpretacion = (
                    f'Caso sintético junto a una frontera: al cambiar únicamente {VARIABLES[cambio]} '
                    'entre las pruebas 1 y 2, cambia la clase. Esto muestra sensibilidad a esa '
                    'variable; no implica una probabilidad calibrada ni una medición real.'
                    if i <= 2 else 'Tercera combinación sintética diferente; se comprueba que la función y la página coinciden.'
                )
                if i == 2:
                    interpretacion += (
                        ' El resultado APTO es discutible porque asientos, asientos_comodos '
                        'e internet_wifi permanecen en 0. Conviene contrastar esta predicción '
                        'con la valoración del lugar y ampliar los datos de entrenamiento.'
                    )
                pruebas.append({'prueba': i, 'entradas': caso, 'resultado': resultado,
                                'http': respuesta.status_code, 'interpretacion': interpretacion})
            for valor in ('texto', '', 'NaN', 'inf', '-1', '2', '0.5'):
                invalido = {**casos[0], VARIABLES[0]: valor}
                assert cliente.post('/', data=invalido).status_code == 400
            assert cliente.post('/', data={}).status_code == 400
            assert cliente.post('/', data={**casos[0], 'extra': '1'}).status_code == 400
    evidencia = {
        'fecha_utc': datetime.now(timezone.utc).isoformat(),
        'modelo_sha256': hashlib.sha256((BASE / 'studybot_model.joblib').read_bytes()).hexdigest(),
        'metodo': 'Función predict y cliente HTTP de pruebas de Flask; no capturas de navegador',
        'pruebas': pruebas, 'validacion_entradas': 'correcta', 'fit_bloqueado_durante_peticion': True,
    }
    (BASE / 'evidencia_pruebas.json').write_text(json.dumps(evidencia, indent=2, ensure_ascii=False), encoding='utf-8')
    lineas = ['# Evidencia de las tres pruebas', '', evidencia['metodo'], '',
              'Las entradas son combinaciones sintéticas para verificar inferencia, no observaciones nuevas.', '']
    for prueba in pruebas:
        lineas += [f"## Prueba {prueba['prueba']}", '', '```json',
                   json.dumps(prueba['entradas'], indent=2, ensure_ascii=False), '```', '',
                   f"Resultado: **{prueba['resultado']}**. HTTP {prueba['http']}.", '', prueba['interpretacion'], '']
    lineas += ['Se verificaron campos ausentes, adicionales, texto, valores no finitos y valores distintos de 0 y 1.',
               'Las peticiones funcionaron con fit bloqueado para detectar reentrenamiento accidental.', '']
    (BASE / 'EVIDENCIA.md').write_text('\n'.join(lineas), encoding='utf-8')
    print(json.dumps(evidencia, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
