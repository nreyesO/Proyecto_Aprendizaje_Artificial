"""Servidor Flask de StudyBot. Carga el modelo una vez al iniciar."""
from flask import Flask, render_template, request
from configuracion import VARIABLES
from prediccion import cargar_modelo, predecir


def crear_app():
    app = Flask(__name__)
    modelo = cargar_modelo()

    @app.route('/', methods=['GET', 'POST'])
    def inicio():
        valores, resultado, error = {}, None, None
        estado = 200
        if request.method == 'POST':
            valores = request.form.to_dict()
            try:
                if any(len(request.form.getlist(k)) != 1 for k in request.form):
                    raise ValueError('No se permiten campos duplicados.')
                resultado = predecir(valores, modelo)
            except ValueError as exc:
                error, estado = str(exc), 400
        return render_template(
            'index.html', variables=VARIABLES, valores=valores,
            resultado=resultado, error=error,
        ), estado

    return app


app = crear_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
