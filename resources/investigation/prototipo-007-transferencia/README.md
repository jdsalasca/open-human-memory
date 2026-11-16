# Prototipo 007 — Retención, reinicio y transferencia

**Fecha:** 16 de noviembre de 2026
**Estado:** **ejecutado, resultado negativo**. Primera prueba del proyecto con
retención real, reinicio de contexto y control placebo.
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium`, `codex-cli 0.169.0`
— **exploratoria, no evidencia**. La evidencia válida es `gpt-6-luna` low, en curso.
**Código:** `src/ohmem/v7_transfer.py`.
**Resultados:** `results/terra-medium-*.json` y `results/summary.json`.

## 1. La pregunta

> ¿Puede un agente conservar un procedimiento verificado, reiniciar por completo su
> contexto y resolver mejor una familia nueva que un clon idéntico?

Es la versión mínima de la pregunta del proyecto, y la que la auditoría exigió como
siguiente paso.

## 2. Diseño

**Sesión 1.** Una llamada con seis pares de la transformación `sort_asc → double`.
El agente devuelve el programa; **nosotros lo verificamos** con 60 entradas nuevas.
Si no coincide, se rechaza. No se confía en el modelo.

**Reinicio.** Cada llamada es una sesión `--ephemeral`, sin historial.

**Sesión 2.** Tareas de **cinco pasos**: el motivo aprendido más tres operaciones
aleatorias. Tres condiciones pareadas, mismo modelo, mismos ejemplos, misma longitud
de prompt:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea actual |
| `memory` | El programa verificado en la sesión 1 |
| `placebo` | Un programa **falso** de la misma longitud (`sort_desc → double`) |

## 3. Resultados

### 3.1 Tres regímenes

| Régimen | `clone` | `memory` | `placebo` |
|---|---|---|---|
| 3 ejemplos de soporte, profundidad 5 | **12/12** | 11/12 | **12/12** |
| 1 ejemplo, artefacto presentado como **programa completo** | 10/12 | **2/12** | 11/12 |
| 1 ejemplo, artefacto presentado como **subrutina** | 9/12 | **11/12** | **11/12** |

### 3.2 Pares discordantes

| Comparación | `clone` acierta / `memory` falla | `memory` acierta / `clone` falla |
|---|---|---|
| Programa completo | **8** | 0 |
| Subrutina | 0 | 2 |

| Comparación | `clone` acierta / `placebo` falla | `placebo` acierta / `clone` falla |
|---|---|---|
| Programa completo | 0 | **1** |
| Subrutina | 0 | 2 |

Con el encuadre de subrutina, `memory` y `placebo` aciertan **lo mismo** (11/12) y
difieren entre sí en 1 tarea a favor de cada uno.

## 4. Lectura

1. **El clon está en techo.** `gpt-6.1-terra` medium resuelve profundidad 5 con uno
   o tres ejemplos. Probamos también profundidad 7 y 9 con tres ejemplos: 4/4 en
   todas las condiciones. **La familia no tiene margen para que la memoria aporte.**
2. **Presentar el artefacto como el programa completo lo vuelve dañino**: 2/12
   frente a 10/12, ocho tareas discordantes, cero en la dirección contraria. Es un
   efecto de anclaje: el agente aplica la subrutina y no completa el resto.
3. **Presentarlo como subrutina elimina el daño, pero no crea ventaja.** La memoria
   empata con un artefacto falso. Los dos superan al clon en las mismas dos tareas:
   el efecto es de **contexto o formato**, no del contenido verificado.
4. **No hay evidencia de transferencia.** La respuesta a la pregunta del §1 es:
   **no en esta familia**. Un procedimiento verificado retenido no mejora el
   desempeño futuro más que un placebo.

### 4.1 Corrida con `luna` low (modelo de experimentos)

La sesión 1 devolvió `double → reverse → sort_desc`, que **no reproduce el motivo**
en las 60 sondas. La verificación falló y el experimento **abortó antes de la
sesión 2**, como está diseñado: no se entrega un artefacto no verificado.

Por tanto, **con el modelo de experimentos no hay datos de transferencia**: el cuello
es la **adquisición** del artefacto, no su uso. Siguiente intento: más ejemplos, un
motivo más simple, o pedir explícitamente el número de operaciones. No se relaja la
verificación para que pase.

## 5. Qué falló y qué haría falta

- **Fallo de calibración:** el clon resuelve la tarea. Sin espacio para fallar, no
  hay nada que transferir.
- **El artefacto no era necesario:** el modelo puede inferir el programa completo
  con un ejemplo. La subrutina ahorra un paso que el modelo no necesitaba.
- **Siguiente régimen:** una familia donde el clon falle de forma estable —
  horizonte de 20+ pasos, vocabulario abierto, o un dominio sin priors fuertes— y
  donde el artefacto sea **necesario**, no solo útil.

## 6. Límites

- Un modelo, un motivo, una semilla, 12 tareas por condición.
- Los pares discordantes (0/2) no permiten significación; se reportan conteos.
- El smoke n=3 se usó para calibrar profundidad; el régimen de 1 ejemplo se eligió
  tras ver el techo. **No es pre-registrado.**
- La primera corrida con 1 ejemplo usaba un prompt que presentaba el artefacto como
  programa completo; se corrigió y se reportan ambos.
- La verificación del artefacto usa 60 entradas; no es una prueba formal.
- **Sesgo de construcción:** las 12 tareas de la sesión 2 empiezan por el motivo
  aprendido. Es una prueba de **reutilización favorable**, no de transferencia a una
  familia independiente. El clon y el placebo mitigan el efecto, pero no lo eliminan.
- **Longitud de prompt no igualada:** el clon recibe una nota neutra y las otras
  condiciones reciben la subrutina. No se asegura igualdad de tokens.
- **Equivalencia conductual:** en una corrida el agente devolvió `double → sort_asc`
  en lugar de `sort_asc → double`. Son equivalentes en este dominio; la verificación
  es conductual, no de identidad del programa.

## 7. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --n 12 --model gpt-6.1-terra --effort medium `
  --out resources/investigation/prototipo-007-transferencia/results/terra-medium-seed0.json
python -m ohmem.v7_transfer --n 12 --support 1 --model gpt-6.1-terra --effort medium `
  --out resources/investigation/prototipo-007-transferencia/results/terra-medium-support1-subroutine-seed0.json
python resources/investigation/prototipo-007-transferencia/analyze.py
```
