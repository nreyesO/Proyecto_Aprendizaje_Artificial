# Evidencia de las tres pruebas

Función predict y cliente HTTP de pruebas de Flask; no capturas de navegador

Las entradas son combinaciones sintéticas para verificar inferencia, no observaciones nuevas.

## Prueba 1

```json
{
  "silencio": 0,
  "sombra": 0,
  "aire_acondicionado": 0,
  "soporte_para_trabajar": 1,
  "asientos": 0,
  "asientos_comodos": 0,
  "enchufes": 0,
  "flujo_personas": 0,
  "banos_cerca": 0,
  "cafeteria_cerca": 0,
  "internet_wifi": 0
}
```

Resultado: **NO APTO**. HTTP 200.

Caso sintético junto a una frontera: al cambiar únicamente silencio entre las pruebas 1 y 2, cambia la clase. Esto muestra sensibilidad a esa variable; no implica una probabilidad calibrada ni una medición real.

## Prueba 2

```json
{
  "silencio": 1,
  "sombra": 0,
  "aire_acondicionado": 0,
  "soporte_para_trabajar": 1,
  "asientos": 0,
  "asientos_comodos": 0,
  "enchufes": 0,
  "flujo_personas": 0,
  "banos_cerca": 0,
  "cafeteria_cerca": 0,
  "internet_wifi": 0
}
```

Resultado: **APTO**. HTTP 200.

Caso sintético junto a una frontera: al cambiar únicamente silencio entre las pruebas 1 y 2, cambia la clase. Esto muestra sensibilidad a esa variable; no implica una probabilidad calibrada ni una medición real. El resultado APTO es discutible porque asientos, asientos_comodos e internet_wifi permanecen en 0. Conviene contrastar esta predicción con la valoración del lugar y ampliar los datos de entrenamiento.

## Prueba 3

```json
{
  "silencio": 1,
  "sombra": 1,
  "aire_acondicionado": 1,
  "soporte_para_trabajar": 1,
  "asientos": 1,
  "asientos_comodos": 1,
  "enchufes": 1,
  "flujo_personas": 1,
  "banos_cerca": 1,
  "cafeteria_cerca": 1,
  "internet_wifi": 1
}
```

Resultado: **APTO**. HTTP 200.

Tercera combinación sintética diferente; se comprueba que la función y la página coinciden.

Se verificaron campos ausentes, adicionales, texto, valores no finitos y valores distintos de 0 y 1.
Las peticiones funcionaron con fit bloqueado para detectar reentrenamiento accidental.
