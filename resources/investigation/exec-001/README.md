# EXEC-001 — Mapa de aplicación de programas

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado el mapa simbólico** (profundidades 2–5). Las condiciones
`steps` y `nl` quedan pendientes.
**Modelo:** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Código:** `src/ohmem/v7_transfer.py` (condición `oracle`).
**Protocolo:** `protocolo.md`. **Análisis:** `analyze.py`.
**Datos:** `results/oracle-depth-{2,3,4,5}.json`.

## 1. Pregunta

El 007B mostró que, con el programa completo, `luna` resuelve 2/12 tareas de cinco
pasos. ¿Es un problema de ejecución, de orden, de aritmética o de interpretación?
¿A qué profundidad puede aplicar un programa que se le da completo?

## 2. Diseño

Programas de 2 a 5 operaciones sobre las seis operaciones del dominio. Doce tareas
por profundidad, dos ejemplos de soporte. La condición `oracle` entrega el programa
completo; el modelo solo debe aplicarlo. La **longitud mínima equivalente** se
calcula enumerando programas más cortos y comparando su comportamiento en 60 sondas.

## 3. Resultados

| Profundidad nominal | Acierto | Longitud mínima | Acierto |
|---|---|---|---|
| 2 | **11/12 (92 %)** | 2 | **18/21 (86 %)** |
| 3 | 7/12 (58 %) | 3 | 8/18 (44 %) |
| 4 | 8/12 (67 %) | 4 | 4/8 (50 %) |
| 5 | 4/12 (33 %) | 5 | 0/1 (0 %) |

Total: **30/48 (62,5 %)**. La profundidad nominal **no es monótona** (4 acierta más
que 3); la longitud mínima equivalente separa mejor el régimen: 2 operaciones son
aplicables, 3 ya no, 5 está en el suelo.

**Errores observados:** en profundidad 2, un error aritmético en un elemento; en
profundidad 3, valores equivocados (operaciones omitidas o duplicadas); en
profundidad 5, tres permutaciones y cinco errores de valor. El modelo **no falla solo
por el orden**: falla la aplicación de la operación.

## 4. Lectura

1. **Hay un régimen aplicable:** 2 operaciones, 86–92 %. Es el único tramo donde el
   modelo aplica de forma fiable.
2. **La longitud nominal engaña:** una tarea de 5 operaciones puede colapsar a 3; la
   dificultad real es la longitud mínima. El análisis por profundidad nominal mezcla
   tareas fáciles y difíciles.
3. **El cuello del 007 es la aplicación:** con el programa completo, 5 pasos dan
   33 %; el 007B daba 2/12. La memoria no puede arreglar eso.
4. **La memoria debe probarse en 2–3 operaciones efectivas:** ahí el modelo puede
   aplicar, y la pregunta pasa a ser si puede **identificar** el procedimiento sin
   experiencia. En 5 pasos la pregunta está mal planteada.
5. **Pendiente:** `steps` (pedir estados intermedios) y `nl` (programa en lenguaje
   natural) para separar el seguimiento del estado de la interpretación de las
   operaciones.

## 5. Implicación para la memoria

El experimento de memoria debe usar **procedimientos de 2–3 operaciones efectivas**
donde el clon pueda aplicar pero no identificar. Candidatos:

- operaciones con nombres opacos, cuya semántica solo está en el artefacto;
- un motivo de 2 operaciones que no se infiere de dos ejemplos;
- una tarea de 3 operaciones donde el artefacto cubre 2 y los ejemplos dan la
  tercera.

La familia de 5 pasos queda **cerrada** para memoria: mide aplicación, no retención.

## 6. Límites

- Un modelo, una semilla, 12 tareas por profundidad.
- La longitud mínima se calcula sobre 60 sondas; no es una prueba formal de
  equivalencia.
- Solo se ejecutó la condición simbólica; `steps` y `nl` están pendientes.
- Las tareas empiezan por el motivo del 007; para aplicación es irrelevante, pero se
  reporta.
- El “intérprete” es el generador de los valores esperados; no es un control
  independiente. La comprobación es por construcción.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
foreach ($s in 0,1,2,3) {
  python -m ohmem.v7_transfer --n 12 --support 2 --suffix $s `
    --session1-examples 12 --exact-ops --conditions oracle `
    --model gpt-6-luna --effort low --timeout 120 `
    --out "resources/investigation/exec-001/results/oracle-depth-$($s+2).json"
}
python resources/investigation/exec-001/analyze.py
```
