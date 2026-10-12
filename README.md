# ZyBF — Brainf*** en Zymbol, con nombres en español

🌐 [zymbol-lang.org](https://zymbol-lang.org) · ▶ [playground](https://zymbol-lang.org/playground.html)

Intérprete de Brainf*** (8 instrucciones, todas símbolos) escrito en Zymbol.
Un lenguaje de símbolos interpretado por otro lenguaje de símbolos.

Es un **mini LDV** de Zymbol v0.0.10: una aplicación pequeña escrita para poner el
lenguaje a prueba en un dominio. Sus tres hallazgos (`HALLAZGOS.md`) cambiaron el
lenguaje, y la propia aplicación usa ya lo que pidió: `##'`, la conversión de un
entero en su carácter.

| Archivo | Qué es |
|---|---|
| `bf.zy` | el intérprete: `bf::ejecutar(programa, entrada)` devuelve `(salida, pasos)` |
| `bf_cli.zy` | línea de comandos: lee programa y entrada de stdin |
| `pruebas/oraculo.zy` | 13 pruebas; las salidas esperadas salen de `oraculo.py` |
| `oraculo.py` | intérprete de referencia independiente (Python), misma semántica |
| `pesado2.zy` | un programa de 4 bucles anidados de 16 vueltas (419 430 pasos), para medir |
| `HALLAZGOS.md` | el log de hallazgos, en la forma de `zymbol-design/LDV.md` § 5.2 |

```bash
zymbol run pruebas/oraculo.zy
printf '%s\n%s\n' ',[.,]' 'hola' | zymbol run bf_cli.zy
```

Semántica: cinta de 300 celdas de 8 bits que dan la vuelta; el puntero no puede
salir de ella (error legible); `,` sin entrada deja 0; `.` imprime el carácter
cuyo código es el valor de la celda (0..255); corchetes mal emparejados dan error.

Requiere Zymbol **v0.0.10**: la instrucción `.` es `salida = salida ##'cinta[p]`.
Hasta la v0.0.9 no había paso de entero a carácter, y `bf.zy` llevaba una tabla de
256 literales `0d0 .. 0d255` indexada en ejecución (GAP-BF-001).

Las pruebas corren en los tres motores (`zymbol run`, `zymbol run --vm` y el del
navegador) y forman parte de la puerta de calidad de Zymbol
(`zyquality/project/apps.toml`, id `zybf`).
