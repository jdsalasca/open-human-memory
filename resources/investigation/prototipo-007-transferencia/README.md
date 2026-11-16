# Prototipo 007 — Retención, reinicio y transferencia

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, resultado negativo.** Primera prueba del proyecto con
retención real, reinicio de contexto y control placebo.
**Modelo (evidencia):** `gpt-6-luna`, `reasoning_effort = low`, `codex-cli 0.169.0`.
**Modelo (exploratorio):** `gpt-6.1-terra` medium; sus cifras no cuentan como
evidencia.
**Código:** `src/ohmem/v7_transfer.py`.
**Resultados:** `results/luna-low-support1-12ex.json`,
`results/luna-low-support2-12ex.json` (evidencia); `results/terra-medium-*.json`
(exploratorio); `results/summary.json` (pares).

## 1. La pregunta

> ¿Puede un agente conservar un procedimiento verificado, reiniciar por completo su
> contexto y resolver mejor una familia nueva que un clon idéntico?

Es la versión mínima de la pregunta del proyecto, y la que la auditoría exigió como
siguiente paso.

## 2. Diseño

**Sesión 1.** Una llamada con pares de la transformación `sort_asc → double`. El
agente devuelve el programa; **nosotros lo verificamos** con 60 entradas nuevas. Si
no coincide, se rechaza. No se confía en el modelo.

**Reinicio.** Cada llamada es una sesión `--ephemeral`, sin historial.

**Sesión 2.** Tareas de **cinco pasos**: el motivo aprendido más tres operaciones
aleatorias. Tres condiciones pareadas, mismo modelo, mismos ejemplos, misma longitud
de prompt:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea actual |
| `memory` | El programa verificado en la sesión 1 |
| `placebo` | Un programa **falso** de la misma longitud (`sort_desc → add_one`) |

## 3. Resultados con `luna` low (evidencia)

### 3.1 Adquisición

| Sesión 1 | Programa devuelto | ¿Verifica? | Decisión |
|---|---|---|---|
| 6 ejemplos | `double → reverse → sort_desc` | **No** | aborta antes de la sesión 2 |
| 12 ejemplos + «exactamente 2 operaciones» | `double → sort_asc` | **Sí** | pasa a la sesión 2 |

La guarda funciona: con 6 ejemplos **no se entregó un artefacto no verificado**. Con
más información, `luna` adquiere un programa conductualmente equivalente al motivo.

### 3.2 Transferencia con un ejemplo de soporte

| Condición | Acierto |
|---|---|
| `clone` | 0/12 |
| `memory` | 0/12 |
| `placebo` | 2/12 |

**Suelo.** El clon no resuelve la tarea y la memoria tampoco. La familia no
discrimina en este régimen: no hay margen que la memoria pueda ocupar.

### 3.3 Transferencia con dos ejemplos de soporte

| Condición | Acierto |
|---|---|
| `clone` | 1/12 |
| `memory` | 3/12 |
| `placebo` | 6/12 |

Pares discordantes (tarea a tarea):

| Comparación | Acierta A / falla B | Acierta B / falla A | Ambos | Ninguno |
|---|---|---|---|---|
| `memory` vs `clone` | 3 | 1 | 0 | 8 |
| `placebo` vs `clone` | 6 | 1 | 0 | 5 |
| `memory` vs `placebo` | 1 | **4** | 2 | 5 |

**El artefacto falso supera al verificado.** Cuatro tareas donde solo acierta el
placebo y una donde solo acierta la memoria. Con 12 tareas, ninguna diferencia es
significativa (test de signos: `memory` vs `clone` p = 0,63; `placebo` vs `clone`
p = 0,13; `memory` vs `placebo` p = 0,38). El resultado es negativo: no hay ventaja
atribuible al contenido retenido, y la dirección observada es la contraria.

## 4. Lectura

1. **La familia no tiene margen para `luna` low.** Con un ejemplo, clon y memoria
   están en el suelo (0/12). Con dos, el clon sigue en 1/12 y la memoria en 3/12.
   Es una familia demasiado difícil para el modelo de experimentos: no mide
   transferencia, mide que la tarea está fuera del alcance.
2. **La memoria no supera al placebo.** En el único régimen donde algo se mueve
   (dos ejemplos), el placebo acierta el doble. El encuadre de subrutina basta para
   producir algo; el contenido verificado no añade.
3. **No hay evidencia de transferencia.** La respuesta a la pregunta del §1 es:
   **no en esta familia, con este modelo y este tamaño de muestra**. No se extiende a
   la transferencia en general.
4. **El cuello es la familia, no el prompt.** Ya se corrigió la adquisición (más
   ejemplos y el número de operaciones) sin tocar la verificación. Seguir moviendo
   el soporte es calibrar el mismo instrumento: hace falta **007B** con un dominio
   donde el clon falle de forma estable y el artefacto sea necesario.

## 5. Qué haría falta (007B)

Se intentó un artefacto de **4 operaciones** para cubrir 4 de 5 pasos. `luna` low no
lo adquiere: cuatro intentos con 12 y 24 ejemplos (motivos de 3 y 4 operaciones)
fueron rechazados por la verificación. El 007B de 4/5 queda **bloqueado en
adquisición**.

La corrida diagnóstica usó el motivo de 2 operaciones y añadió dos condiciones a las
mismas 12 tareas del soporte 2:

- `history`: los 12 pares de la sesión 1 (experiencias de origen, sin programa).
- `oracle`: el programa completo de 5 operaciones (fuga; control de ejecución).

Resultado: clon 1/12, memoria 3/12, placebo 6/12, historial 4/12, **oráculo 2/12**.
Con el programa completo el modelo apenas ejecuta 2 de 12: **el cuello es la
ejecución**, no la retención. Detalle en
[`../prototipo-007b-transferencia/`](../prototipo-007b-transferencia/).

## 6. Límites

- Un modelo (`luna` low), un motivo, una semilla, 12 tareas por condición.
- Las diferencias de 1–6 tareas no permiten significación; se reportan conteos y
  valores p exactos del test de signos.
- La adquisición con 12 ejemplos se eligió tras el fallo con 6. **No es
  pre-registrado.**
- El soporte 1 y 2 se eligieron para calibrar el margen; ninguno lo produjo.
- La verificación del artefacto usa 60 entradas; no es una prueba formal.
- **Sesgo de construcción:** las 12 tareas de la sesión 2 empiezan por el motivo
  aprendido. Es una prueba de **reutilización favorable**, no de transferencia a una
  familia independiente. El clon y el placebo mitigan el efecto, pero no lo eliminan.
- **Longitud de prompt no igualada:** el clon recibe una nota neutra y las otras
  condiciones reciben la subrutina. No se asegura igualdad de tokens.
- **Equivalencia conductual:** el agente devolvió `double → sort_asc` en lugar de
  `sort_asc → double`. Son equivalentes en este dominio; la verificación es
  conductual, no de identidad del programa.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --model gpt-6-luna --effort low `
  --n 12 --support 2 --session1-examples 12 --exact-ops `
  --out resources/investigation/prototipo-007-transferencia/results/luna-low-support2-12ex.json
```

## Apéndice. Corrida exploratoria con `terra` medium

| Régimen | `clone` | `memory` | `placebo` |
|---|---|---|---|
| 3 ejemplos de soporte | **12/12** | 11/12 | **12/12** |
| 1 ejemplo, artefacto como programa completo | 10/12 | **2/12** | 11/12 |
| 1 ejemplo, artefacto como subrutina | 9/12 | **11/12** | **11/12** |

Con `terra`, el clon está en techo: la familia tampoco discrimina, por arriba.
Presentar el artefacto como programa completo lo vuelve dañino (8 pares a favor del
clon, 0 en contra); como subrutina, empata con el placebo. **No se usa como
evidencia** porque el modelo no es el de experimentos. Confirma el diagnóstico: el
problema es la familia, no el modelo.
