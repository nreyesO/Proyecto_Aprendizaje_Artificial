"""Comprueba dos arranques reales del servidor y tres POST en cada uno."""
import json
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:5000/'


def main():
    pruebas = json.loads((BASE / 'evidencia_pruebas.json').read_text(encoding='utf-8'))['pruebas']
    resultados = []
    for intento in (1, 2):
        with (BASE / f'arranque_{intento}.log').open('w', encoding='utf-8') as log:
            proceso = subprocess.Popen([sys.executable, 'app.py'], cwd=BASE, stdout=log, stderr=log,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            try:
                limite = time.monotonic() + 30
                while True:
                    if proceso.poll() is not None:
                        raise RuntimeError('El servidor terminó antes de responder. Revisa el log.')
                    try:
                        with urllib.request.urlopen(URL, timeout=1) as r:
                            assert r.status == 200 and 'STUDYBOT' in r.read().decode()
                        break
                    except (OSError, TimeoutError):
                        if time.monotonic() >= limite:
                            raise
                        time.sleep(0.3)
                for prueba in pruebas:
                    cuerpo = urllib.parse.urlencode(prueba['entradas']).encode()
                    with urllib.request.urlopen(URL, data=cuerpo, timeout=5) as r:
                        assert r.status == 200
                        assert f"<strong>{prueba['resultado']}</strong>" in r.read().decode()
                resultados.append({'arranque': intento, 'get': 200, 'predicciones_verificadas': 3})
            finally:
                proceso.terminate()
                proceso.wait(timeout=10)
    (BASE / 'verificacion_reinicio.json').write_text(json.dumps(resultados, indent=2), encoding='utf-8')
    print(json.dumps(resultados, indent=2))


if __name__ == '__main__':
    main()
