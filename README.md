# bf.zy — Brainf*** en Zymbol, con nombres en español

Intérprete de Brainf*** (8 instrucciones, todas símbolos) escrito en Zymbol.
Un lenguaje de símbolos interpretado por otro lenguaje de símbolos.

| Archivo | Qué es |
|---|---|
| `bf.zy` | el intérprete: `bf::ejecutar(programa, entrada)` devuelve `(salida, pasos)` |
| `bf_cli.zy` | línea de comandos: lee programa y entrada de stdin |
| `pruebas.zy` | 13 pruebas; las salidas esperadas salen de `oraculo.py` |
| `oraculo.py` | intérprete de referencia independiente (Python), misma semántica |

```
zymbol run pruebas.zy
printf '%s\n%s\n' ',[.,]' 'hola' | zymbol run bf_cli.zy
```

Semántica: cinta de 300 celdas de 8 bits que dan la vuelta; el puntero no puede
salir de ella (error legible); `,` sin entrada deja 0; `.` imprime el carácter
cuyo código es el valor de la celda (0..255); corchetes mal emparejados dan error.

Nota sobre Zymbol: no hay una función entero -> carácter, pero un literal con
prefijo de base (`0x41`, `0d65`, `0b1000001`, `0o101`) *es* un carácter. Por eso
`bf.zy` lleva una tabla de 256 literales `0d0 .. 0d255` y la indexa en ejecución.
Funciona con Zymbol v0.0.9 y con la rama v0.0.10.
