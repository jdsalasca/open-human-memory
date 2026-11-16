# Prototipo 007 — Retención, reinicio y transferencia

**Fecha:** 16 de noviembre de 2026
**Estado:** **exploratorio**. El smoke n=3 sirvió para calibrar la profundidad; la
corrida principal n=12 no está pre-registrada. Se declara.
**Código:** `src/ohmem/v7_transfer.py`.
**Modelo:** `gpt-6.1-terra`, `reasoning_effort = medium`.
**Resultado crudo:** `results/terra-medium-seed0.json`.

## 1. La pregunta

La auditoría pidió una observación nueva, no otro documento:

> ¿Puede un agente conservar algo aprendido, reiniciar por completo su contexto y
> resolver mejor una familia nueva que un clon idéntico?

Este prototipo hace la versión mínima: aprende **un procedimiento verificado** en
una sesión, lo conserva, reinicia, y lo aplica a composiciones más profundas.

## 2. Diseño

**Sesión 1 (aprendizaje).** Una llamada con seis pares entrada-salida de la misma
transformación (`sort_asc → double`). El agente devuelve el programa como secuencia
de operaciones. **Nosotros lo verificamos** sobre 60 entradas nuevas; si no coincide,
el artefacto se rechaza. No se confía en la palabra del modelo.

**Reinicio.** Cada llamada es una sesión Codex `--ephemeral`, sin historial.

**Sesión 2 (transferencia).** Doce tareas de **cinco pasos**: el motivo aprendido
más tres operaciones aleatorias de las seis disponibles. Tres condiciones pareadas,
mismo modelo, mismos ejemplos, misma longitud de prompt:

| Condición | Qué recibe |
|---|---|
| `clone` | Solo la tarea actual |
| `memory` | El programa verificado de la sesión 1 |
| `placebo` | Un programa **falso** de la misma longitud (`sort_desc → double`) |

El placebo controla el efecto de añadir contexto con forma de programa. Si `memory`
solo supera a `clone`, la ganancia es información adicional; si supera también al
placebo, el contenido verificado aporta.

## 3. Predicciones y falsador

| Resultado | Lectura |
|---|---|
| `memory` > `clone` y > `placebo` | Transferencia del procedimiento retenido |
| `memory` > `clone` ≈ `placebo` | Contexto adicional, no conocimiento |
| `memory` ≈ `clone` ≈ `placebo` | Sin transferencia |
| `memory` < `clone` | El artefacto perjudica |

**Falsador:** `memory ≤ clone` en 12 tareas pareadas.

## 4. Métricas

Acierto exacto en la consulta, segundos por llamada, y pares discordantes
(`memory` acierta / `clone` falla y viceversa). Sin prueba de significación con
n=12; se reportan los conteos.

## 5. Límites

- Un modelo, un motivo, una semilla.
- n=12; los intervalos son anchos.
- El artefacto es un programa de dos operaciones; no se prueba un concepto.
- La tarea es sintética y el espacio, finito.
- El smoke n=3 se usó para elegir profundidad 5: hay una decisión de diseño
  informada por resultados previos.

**Corrección de instrumento (16 nov).** La primera versión de los 60 probes de
verificación generaba listas constantes por un error de generación (se creaba un
`Random` nuevo por elemento). Lo detectó `test_placebo_does_not_verify`: el placebo
pasaba la verificación. Se corrigió **antes** de la corrida principal. El smoke n=3
se ejecutó con los probes defectuosos y **no se usa** como evidencia.

## 6. Reproducir

```powershell
$env:PYTHONPATH="src"
python -m ohmem.v7_transfer --n 12 --model gpt-6.1-terra --effort medium `
  --out resources/investigation/prototipo-007-transferencia/results/terra-medium-seed0.json
```

## 7. Resultados

### 7.1 Régimen con 3 ejemplos: saturado

`terra-medium-seed0.json`: **clone 12/12, placebo 12/12, memory 11/12**. El clon
está en techo y el experimento **no discrimina**. La familia de cinco pasos es
trivial para este modelo. No es evidencia sobre transferencia; es un fallo de
calibración.

Se probaron profundidades 7 y 9 con 3 ejemplos: **4/4 en las tres condiciones**.
La familia no crea dificultad suficiente.

### 7.2 Régimen con 1 ejemplo: calibrado

`terra-medium-support1-seed0.json`: en ejecución. Con un solo par de soporte la
tarea es ambigua; el clon debería caer. Si no cae, la familia no sirve y el 007
necesita otro dominio.
