# ZyBF — hallazgos

> **Qué es esto.** El log de hallazgos de ZyBF, un intérprete de Brainf\*\*\* escrito en Zymbol, en la forma canónica que pide
> `zymbol-design/LDV.md` § 5.2: un fichero `HALLAZGOS.md`, cuatro secciones
> (`BUG` / `GAP` / `ERROR` / `IDEA`), una tabla resumen e identificadores con el alcance del
> proyecto desde la primera entrada, en **una sola secuencia** para los cuatro tipos.
>
> **Qué es este proyecto.** Un intérprete de Brainf\*\*\* (ocho instrucciones, todas símbolos) en 82
> líneas de Zymbol con nombres en español, `bf.zy`, y un oráculo independiente en Python
> (`oraculo.py`) del que salen las salidas esperadas de sus 13 pruebas. Se escribió el
> **2026-10-01**. Es una aplicación de las que LDV usa para probar el lenguaje, y los tres hallazgos
> salieron de escribirla: dos de lo que le faltó al lenguaje, uno de un error de parseo al teclear.
> **Los hallazgos de velocidad no son de este proyecto:** salieron de los benchmarks y están en
> `ZyBench/HALLAZGOS.md`.
>
> **Estado.** Cada entrada dice el suyo. **Nada se cierra con este documento:** el autor decide por
> hallazgo si implementa, aplaza o rechaza. Este proyecto **no está en la puerta**
> (`zyquality/project/apps.toml`) ni indexado en `LDV.md` § 5.1: eso también lo decide el autor.

---

## Resumen

| ID | Tipo | Módulo | Qué | Motores | Estado |
|----|------|--------|-----|---------|--------|
| [GAP-BF-001](#gap-bf-001) | GAP | lenguaje | un valor calculado no se puede convertir en `Char`; solo hay literal por código | los tres | **ABIERTO** — hay rodeo (tabla de 256 literales) |
| [ERROR-BF-002](#error-bf-002) | ERROR | `LLM.md`, `GUIDE.md`, `07_base_literals` | un literal con prefijo de base (`0xFF`, `0d65`) es siempre `Char`; tres textos dicen `Int` | los tres coinciden, la documentación no | **ABIERTO** — clase 1 de ZyDDT |
| [IDEA-BF-003](#idea-bf-003) | IDEA | `zymbol-parser` | tras `x = e` una segunda sentencia en la misma línea falla con un error que no dice por qué | `zytw`, `zyvm` | **ABIERTO** |

---

## GAP

### GAP-BF-001

**Un valor calculado no se puede convertir en `Char`. Zymbol tiene un literal por código
(`0x41`, `0d65`), pero ninguna forma de pasar de un entero que existe solo en ejecución a su
carácter.**

Encontrado el **2026-10-01** al escribir la instrucción `.` de `bf.zy`, que tiene que imprimir
«el carácter cuyo código es el valor de la celda». Con `n = 65`:

| intento | `zytw` / `zyvm` (v0.0.9) | `zytw` / `zyvm` (v0.0.10) | `zyjs` |
|---|---|---|---|
| `##'n` | `expected expression, found HashHashApos` | `expected expression, found '##''` | `expected expression, found CAST_CHAR` |
| `c + 1` con `c = 'A'` | `+ is arithmetic only — use juxtaposition…` | igual | igual |
| `"{n}"` | el **texto** `65` | igual | igual |

`##'` existe, pero solo como conversión de **entrada** (`<< ##' "msg" c`, que pide un texto de
longitud 1); como expresión no se acepta. `##!` convierte `Char` → `Int` y es «la única vía
directa» (`ZyQuality/corpus/casts/06_char_to_int.zy`); **no hay ningún caso del sentido
inverso** entre los 666 programas del corpus ni en `ZyDDT/HALLAZGOS/` (los `chr(…)` y
`fromCodePoint` que aparecen ahí son código de apoyo en Python y JavaScript).

**El rodeo** (el que usa `bf.zy`): una tabla de literales indexada en ejecución,
`tabla = [0d0, 0d1, …, 0d255]` y `tabla[valor + 1]`. Funciona en los tres motores y en las dos
versiones (13 de 13 pruebas contra el oráculo), pero obliga a escribir la tabla en cada programa
que la necesite y **no cubre un rango abierto** (cualquier punto de código Unicode).

**Qué se desconoce.** Si es una decisión de diseño: hay una lógica —un literal por código evita
los escapes `\uXXXX`, y nada cruza una frontera sin escribirse—, pero no responde a cómo se
convierte un valor que solo existe al ejecutar. Y si la forma natural es `##'` aplicado a un
`Int` (ya existe, con otro significado en la entrada) u otra distinta: **no se propone sintaxis**.

**Qué lo sujetaría:** un caso `casts/` del sentido inverso (entero → carácter, con el rango
fuera de `0..255`), junto al `06_char_to_int` que ya existe.

**Estado.** **ABIERTO.** Pregunta de diseño; sin respuesta. Registrado en ZyDDT como
[`GLB-109`](../ZyDDT/HALLAZGOS/GLOBAL.md) (2026-10-09), validado contra la rama `v0.0.10`: en los tres
motores `##'n` sigue siendo un error de parseo, y `zyjs` lo dice ya con las palabras de Rust.

---

## ERROR

### ERROR-BF-002

**Un literal con prefijo de base es siempre un `Char`; tres textos que lo describen dicen otra
cosa y se contradicen entre sí.**

Encontrado el **2026-10-01** leyendo `corpus/arithmetic/07_base_literals.zy` contra su
`.expected`, mientras se buscaba GAP-BF-001. Con `a = 0xFF`, `b = 0x3042`, `c = 0d65`:

```
##' 255      // el tipo y ##!a
##' 12354
##' 65
```

Idéntico en `zytw`, `zyvm` y `zyjs` (v0.0.9; `zytw` y `zyvm` también en la v0.0.10 `820a60a`).
`0xFF` es `ÿ`, `0x3042` es `あ`, y `0d65` —«decimal explícito» en la guía— es `A`, no el 65.

| dónde | dice |
|---|---|
| `LLM.md`, tabla de tipos | `0x41`, `0b1010`, `0o17`, `0d99` son **`Int`** |
| `GUIDE.md`, «Base Literals and Conversions» | resultado **`Char` si es ASCII, `Int` en caso contrario** |
| `GUIDE.md`, línea ~312 | «Numeric character codes: `0x41`…» — los trata como **códigos de carácter** |
| `07_base_literals.zy`, comentario | «Higher hex values **(Int result)**» |
| `07_base_literals.expected` (del mismo caso) | registra `ÿ`: es un **`Char`** |

Cuatro afirmaciones sobre una misma cosa; solo la última coincide con lo que ejecutan los
motores. El caso pasa en verde porque compara contra lo que el motor hizo, no contra lo que su
propio comentario afirma: la forma exacta que `ZyDDT/HALLAZGOS/GLOBAL.md` describe para la
**clase 1** (los tres coinciden y los tres están mal frente a la documentación), que en la rama
`main` de ZyDDT se decía que seguía sin aparecer.

**Consecuencia práctica:** no hay forma de escribir un entero en hexadecimal. `0xFF + 1` falla
con `+ is arithmetic only…`; hay que escribir `##!0xFF + 1` (→ `256`) o usar decimal. Y la frase
de la guía no se puede cumplir tal como está: no existe el «`Int` en caso contrario».

**Qué se desconoce.** La intención. Los usos en las aplicaciones (`0d27`, `0d9`, `0d127`, `0x1b`)
son todos códigos de control ASCII: son `Char` bajo cualquiera de las dos lecturas, **no deciden
nada**. Tampoco se sabe si `zyjs` en la rama v0.0.10 coincide.

**Decisiones que son del autor** (compatibles con los datos las tres):
1. **La documentación está mal:** un literal con prefijo de base es siempre un carácter. Tres
   frases y un comentario; coincide con el golden y los tres motores. Sigue sin haber literal
   hexadecimal entero.
2. **El código está mal:** fuera de ASCII debe ser `Int`. Coincide con la guía, pero cambia
   `0xFF` de `ÿ` a `255`, rompe el `.expected` de `07_base_literals` y crea un tipo que depende
   del valor (el resto del lenguaje evita las coerciones).
3. **Separar las dos cosas con una forma nueva**, p. ej. un literal de entero hexadecimal
   distinto del de carácter. Resuelve «no hay hexadecimal entero» sin tocar lo existente; la más cara.

**Para ZyDDT.** En la rama `v0.0.10` (`b54a2df`, 2026-10-06) la numeración de `GLOBAL.md` llega a
`GLB-103` y `GLB-008` **ya está ocupado** (otro hallazgo); el ID `GLB-008` que se propuso antes
para este caso en la rama `main` **queda sin efecto**. Siguiente libre: `GLB-104`; lo asigna el
autor. No hay nada sobre literales de base ni sobre entero → carácter en `HALLAZGOS/` (se
buscó). Un pin con el comportamiento observado acompaña a este hallazgo
(`GLB-008_literal_de_base.zy`, a renombrar).

**Estado.** **ABIERTO.** Registrado en ZyDDT como [`GLB-110`](../ZyDDT/HALLAZGOS/GLOBAL.md)
(2026-10-09), que sustituye al `GLB-008` propuesto arriba. Validado contra la rama `v0.0.10`: `zyjs` coincide
con los motores Rust, y el diseño ya lo decide —`zymbol-design/SYMBOLS.md`: *«base prefixes for character
codes»*—, así que es la opción 1: corregir los tres textos.

---

## IDEA

### IDEA-BF-003

**Después de `x = e`, una segunda sentencia en la misma línea falla con un error que apunta al
`=` o al `+=` de la segunda y no dice que la primera se la comió.**

Encontrado el **2026-10-01** (al escribir `pruebas.zy`) y reproducido el **2026-10-07** en la rama v0.0.10 `820a60a`. Con
`s = 0`, `i = 1` y la sentencia dentro de `@ i <= 2 { … }`:

| escrito en una línea | resultado |
|---|---|
| `s += 1  i += 1` | corre |
| `s += 1  i = i + 1` | corre |
| `s = s + 1  i += 1` | `error: unexpected token: '+='` |
| `s = s + 1  i = i + 1` | `error: unexpected token: '='` |
| `s = s + 1` ⏎ `i = i + 1` (dos líneas) | corre |
| `s = s + 1; i = i + 1` | corre |

El mensaje completo, p. ej. para `x = (x * 75 + 74) % 65537  a = a + x`:

```
error: unexpected token: '='
  --> m2.zy:3:41
  = help: expected statement (>>, <<, ?, ??, @, @!, @>, !?, <~, ¶, \\, or identifier)
```

El mismo patrón, con `¶`: `>> ¶ ok " de " (ok + mal) ¶` da `unexpected token: " de "`
con la misma lista — `¶` cierra la sentencia de salida, `ok` es una sentencia nueva, y la cadena
que la sigue ya no cabe en ninguna.

**Hipótesis (no se ha leído el parser):** la parte derecha de una asignación simple acepta
yuxtaposición (como `>>`), así que `1  i` se lee como dos operandos de la misma expresión y el
error salta recién en el `=`; la asignación compuesta no la acepta, por eso corre. Si es así, hay
**una asimetría entre `=` y `+=`** además del mensaje.

**Qué se pide, si se acepta:** que el error diga lo que pasó («`i` se tomó como parte de la
expresión anterior; separa las sentencias con un salto de línea o `;`») en lugar de listar lo que
se esperaba. La lista de `expected statement (…)` es cierta y no ayuda a quien tropieza.

**Estado.** **ABIERTO.** No es un defecto de ejecución; es de diagnóstico. Registrado en ZyDDT como
[`GLB-111`](../ZyDDT/HALLAZGOS/GLOBAL.md) (2026-10-09). La hipótesis se confirmó al medir: `t = "a" b "c"`
da `axc` y `t += "a" b "c"` se rechaza, y `s = 1  i` da `11` sin aviso.

---

## Qué costó, y qué dice

Tres hallazgos en 82 líneas de programa, dos de ellos leyendo el corpus de ZyQuality al buscar el
primero: lo de siempre en LDV, el dominio —aquí, programar *otro* lenguaje de símbolos— pidió al
lenguaje lo que le faltaba.

Lo que se equivocó por el camino, apuntado porque forma parte del método:

- **Una numeración chocó:** el `GLB-008` propuesto para ERROR-BF-002 ya existe en la rama `v0.0.10` de ZyDDT.
- **Una cifra del corpus era errónea:** se dijo 733 pruebas; son 666.
- **Una `GUIDE.md` leída por la web estaba atrasada** respecto del clon (la leída por la web era de la v0.0.7;
  la del clon, de la v0.0.9): para escribir Zymbol hay que fiarse del repositorio, no de la página.
  No se determinó por qué (caché o rama).

Lo que sí funcionó: **un oráculo independiente** (el intérprete de `bf.zy` en Python), que dio las salidas
esperadas sin pasar por el código que se prueba.

---

## Ficheros

| fichero | qué es |
|---|---|
| `bf/bf.zy`, `bf/bf_cli.zy`, `bf/pruebas.zy`, `bf/oraculo.py` | el intérprete, su línea de comandos, las 13 pruebas, el oráculo |
| `GLB-008_literal_de_base.md`, `cases/pin/GLB-008_literal_de_base.zy`, `GAP_int_a_caracter.md` | las fichas ZyDDT de ERROR-BF-002 y GAP-BF-001, a renumerar |
