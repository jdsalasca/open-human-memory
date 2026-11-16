# Guía para revisores

**Versión:** `v1.14-review` · 16 de noviembre de 2026
**Manuscrito:** [`manuscrito.md`](manuscrito.md)
**Repositorio:** https://github.com/jdsalasca/open-human-memory

Esta guía existe para que un revisor externo pueda evaluar el trabajo sin leer
treinta documentos. Si algo no está aquí, es un defecto del repositorio.

---

## 1. Qué se somete

Un **programa experimental con resultado negativo y un instrumento de medición**,
no una arquitectura nueva.

| Pieza | Dónde | Qué contiene |
|---|---|---|
| Manuscrito | `docs/manuscrito.md` | Hipótesis, método, resultados, discusión, límites |
| Teoría | `docs/teoria.md` | Canales, proposición, predicciones P1–P6 |
| Registro | `docs/registro-de-afirmaciones.md` | 83 afirmaciones con estado y falsador |
| Ejecuciones | `docs/registro-de-ejecuciones.md` | Modelo, esfuerzo, semillas, comandos |
| Revisión | `resources/investigation/revision-sistematica/` | 31 trabajos, cribado y extracción |
| Código | `src/ohmem/` | 16 módulos, sin dependencias |
| Resultados | `*/results/` | JSON crudos por semilla |

---

## 2. Qué se afirma

| ID | Afirmación | Nivel |
|---|---|---|
| T1 | En espacio explorable, identificable y presupuestado, la memoria no amplía cobertura | E0 + E2 local |
| V1 | Con continuidad total, 41,8 % menos pasos con igual cobertura | E2 local |
| V2 | Con continuidad cero, 22,1 pp menos de acierto | E2 local |
| V3 | Congelar lo aprendido ahorra 26,2 % de trabajo con igual precisión | E2 local |
| P2 | Una política aprendida **no** supera una regla simple (−1,0 pp, IC −3,1 a 0) | E2 local |
| P4 | El probe cuesta 41 pasos y ahorra 29: valor neto negativo | E2 local |
| L1 | `gpt-6-luna` low acierta 30/64 (46,9 %) sin historial | E2 local |
| G1 | Un procedimiento verificado no supera a un placebo tras el reinicio (11/12 vs 11/12) | E2 local |

**Ninguna alcanza E3** (varias distribuciones), **E4** (reproducción con tareas
reales) ni **E5** (longitudinal). El manuscrito lo dice.

## 3. Qué **no** se afirma

- Que la memoria no sirva a los agentes.
- Que las habilidades no funcionen.
- Que exista novedad algorítmica.
- Que haya transferencia entre modelos.
- Que haya formación conceptual.
- Que la revisión de literatura sea exhaustiva.
- Que los resultados de terceros estén replicados.

## 4. Cómo verificar

```bash
python -m unittest discover -s tests -v          # 60 tests
python resources/investigation/prototipo-004-validez/reproduce.py
python resources/investigation/prototipo-005-presupuesto/reproduce.py
python resources/investigation/prototipo-006-politica/reproduce_corrected.py
python resources/investigation/prototipo-006-agente-llm/analyze.py
```

Los protocolos 004-A y 006-A verifican hashes SHA-256 y abortan si el código o los
datos cambiaron. Los JSON crudos están junto a cada `reproduce.py`.

## 5. Limitaciones declaradas

1. Un entorno sintético de cuatro operaciones y 14 clases conductuales.
2. Un modelo (`gpt-6-luna`), un esfuerzo (`low`), una corrida.
3. n=24 en el diagnóstico con LLM; IC de ±20 pp.
4. Ningún competidor reproducido.
5. Revisión con una base y un revisor; 88 candidatos sin evaluar.
6. Mayoría de preprints en 2026.
7. Sin medición de tokens en los experimentos sintéticos.

## 6. Preguntas para el revisor

1. ¿La proposición de `teoria.md` §3 es correcta con las tres condiciones
   (explorabilidad, identificabilidad, presupuesto) o falta alguna?
2. ¿P4 está ahora bien derivada? ¿Distingue información de herramienta/política?
3. ¿El instrumento (`E`/`K`/`P`, clon, canales, cinco etapas) es suficiente para
   una contribución metodológica, o sigue siendo demasiado débil?
4. ¿Qué afirmación del registro no está respaldada por los datos?
5. ¿Qué habría que añadir para que el trabajo pase de «revisión mayor» a
   «aceptable»?

## 7. Historia de las correcciones

| Fecha | Qué se corrigió | Dónde |
|---|---|---|
| 16 nov | Fuga de respuesta en 001 | `prototipo-001` |
| 16 nov | 002 no usaba historial (`MEM-A0`) | `prototipo-002` |
| 16 nov | 003 retirado por límite de profundidad | `prototipo-004` |
| 16 nov | Control aleatorio amañado del 003 | `prototipo-004` |
| 16 nov | Coste como cota, no medición | `docs/errata-006b.md` |
| 16 nov | `retrieved` era oráculo | `docs/errata-006b.md` |
| 16 nov | Muestra `[:24]` sesgada | `docs/errata-006b.md` |
| 16 nov | `tool` con errores de entorno | `docs/errata-006b.md` |
| 16 nov | Proposición sin identificabilidad | `docs/teoria.md` |
| 16 nov | P4 con el signo invertido | `docs/teoria.md` |
| 16 nov | «Verificado» por «declarado» | `revision-sistematica/extraccion.md` |
| 16 nov | Revisión externa `gpt-6.1-terra`: 1,42×, F12, ventana, atribución 006-B, corolario 3, presupuesto y JANUS | `respuesta-a-revision-externa.md` |
| 16 nov | 007: retención + reinicio + placebo; sin ventaja sobre placebo | `prototipo-007-transferencia/` |

El repositorio conserva los resultados antiguos y las erratas. No se reescribió la
historia.




