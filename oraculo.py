#!/usr/bin/env python3
"""Intérprete de referencia en Python con la MISMA semántica que bf.zy.
Sirve de oráculo: genera las salidas esperadas de pruebas/oraculo.zy de forma independiente."""
def ejecutar(prog, entrada=""):
    n = len(prog); saltos = [0]*(n+2); pila = []
    for i, c in enumerate(prog, 1):
        if c == '[': pila.append(i)
        elif c == ']':
            if not pila: return "error: sobra un ] en la posición %d" % i, 0
            j = pila.pop(); saltos[i] = j; saltos[j] = i
    if pila: return "error: falta cerrar el [ de la posición %d" % pila[0], 0
    cinta = [0]*301; p = 1; ip = 1; ie = 0; out = []; pasos = 0
    while ip <= n:
        c = prog[ip-1]
        if c == '>': p += 1
        elif c == '<': p -= 1
        elif c == '+': cinta[p] = (cinta[p]+1) % 256
        elif c == '-': cinta[p] = (cinta[p]+255) % 256
        elif c == '.':
            v = cinta[p]
            out.append(chr(v))
        elif c == ',':
            if ie < len(entrada): cinta[p] = ord(entrada[ie]); ie += 1
            else: cinta[p] = 0
        elif c == '[':
            if cinta[p] == 0: ip = saltos[ip]
        elif c == ']':
            if cinta[p] != 0: ip = saltos[ip]
        else: pasos -= 1
        if p < 1 or p > 300:
            return "".join(out) + "\n[error: el puntero salió de la cinta]", pasos
        ip += 1; pasos += 1
    return "".join(out), pasos

CASOS = [
 ("A (8x8+1)",            "++++++++[>++++++++<-]>+.", ""),
 ("Hola mundo clásico",   "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.", ""),
 ("invertir (con centinela)", ">,[>,]<[.<]", "Zymbol"),
 ("eco (cat)",            ",[.,]", "Hola, Zymbol 0.0.10!\nsegunda línea"),
 ("comentarios ignorados","suma: ++++[>+++++<-] resultado >++++++++++++++++++++++++++++++++++++++++++++++++. fin", ""),
 ("3 bucles anidados (11^3 mod 256 = '3')", "+++++++++++[>+++++++++++[>+++++++++++[>+<-]<-]<-]>>>.", ""),
 ("vuelta de 8 bits (empieza en 255)",  "-+++++++[>+++++++++<-]>+++.", ""),
 ("sin entrada: , deja 0 (y 10 más = salto)", ",++++++++++.", ""),
 ("salto de línea (código 10)", "++++++++++.", ""),
 ("vuelta a 255 = ÿ (U+00FF)", "-.", ""),
 ("corchete sobrante",    "+]", ""),
 ("corchete sin cerrar",  "[[+]", ""),
 ("puntero fuera de la cinta", "<+", ""),
]
if __name__ == "__main__":
    for t, p, e in CASOS: print(t, "->", repr(ejecutar(p, e)))
