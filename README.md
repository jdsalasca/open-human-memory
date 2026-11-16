# Open Human Memory

Investigación abierta sobre memoria para agentes: qué puede aprender un sistema
de su experiencia, qué puede justificar y cómo evitar que sus errores se
conviertan en certezas permanentes.

**Estado:** programa de investigación con un **diagnóstico ejecutable**. No hay
producto todavía; hay un harness mínimo para decidir qué capa importa antes de
construir otra arquitectura.

## Inicio rápido

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m ohmem.experiment --train 200 --eval 50
```

En Windows PowerShell:

```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests -v
python -m ohmem.experiment --train 200 --eval 50
```

El harness compara seis condiciones (sin memoria, solucionador actual,
retrieval, oráculo, procedimiento y abstracción) en tres distribuciones
(instancias nuevas, familias nuevas con la misma estructura y familias
estructuralmente nuevas). Es un instrumento sintético, no un benchmark de LLM.

Licencia: MIT (`LICENSE`).

## La pregunta

> ¿Puede un agente acumular conocimiento procedimental durante meses,
> transferirlo entre modelos y mejorar sin reentrenar el LLM, sin convertir
> errores del pasado en conocimiento canónico?

La respuesta corta: **no hay todavía evidencia de que la experiencia amplíe la
competencia.** El prototipo más honesto del programa midió su propio mecanismo
contra un control sin memoria y perdió: las abstracciones aprendidas ahorran
cómputo bajo presupuesto acotado, pero no resuelven nada que la búsqueda profunda
no resuelva. La validación causal sigue abierta.

## Resultado de validez: las macros no amplían la capacidad (sintético)

Prototipo 004-A, protocolo congelado antes de medir, rejilla completa de 64
programas de profundidad 3, media de 3 semillas:

| Condición | Aciertos /64 | Candidatos | Candidatos por acierto |
|---|---|---|---|
| Sin memoria, profundidad 2 | 33 (51,6 %) | 876 | 26,6 |
| **Sin memoria, profundidad 3** | **64 (100 %)** | 1.761 | 27,5 |
| Azar, mismo lenguaje, profundidad 2 | 50,7 (79,3 %) | 1.543 | 30,5 |
| Macros aprendidas, profundidad 2 | 54 (84,4 %) | 1.448 | 26,8 |
| Macros aprendidas, profundidad 3 | 64 (100 %) | 2.247 | 35,1 |

- **Sin historial y con búsqueda de tres pasos se resuelve todo.** El límite de dos
  pasos del 003 lo impusimos nosotros.
- La biblioteca aprendida **ahorra 17,8 % de candidatos y pierde 15,6 pp de
  cobertura**; por acierto el ahorro es 2,6 %. Con profundidad 3 permitida,
  **encarece** la búsqueda un 27,6 %.
- El control `RANDOM` del 003 estaba amañado: **250/560** bibliotecas arbitrarias
  del mismo lenguaje eran perfectas en su conjunto de evaluación.
- La curva se satura en **6 experiencias**.
- Única ganancia defendible: con presupuesto ≤ 40 candidatos por tarea, la
  biblioteca acierta más. Es un **prior barato**, no una capacidad nueva.

Detalles, resultados crudos y protocolo en
[`prototipo-004-validez/`](resources/investigation/prototipo-004-validez/).

El Prototipo 002 fue un **benchmark de solucionador**: `MEM-A0` (mismo
solucionador sin historial) empató con `MEM-E` en todo. El 001 quedó invalidado
por target leakage. El 003 se conserva como registro exploratorio de la conclusión
que el 004 retiró.

## Por dónde empezar

| Documento | Para qué |
|---|---|
| [24-programa-de-investigacion-v2.md](resources/investigation/24-programa-de-investigacion-v2.md) | Horizontes, hipótesis y experimento diferencial A–E |
| [28-programa-de-competencia.md](resources/investigation/28-programa-de-competencia.md) | Programa v3: continuidad, competencia y expansión |
| [29-experimento-diagnostico.md](resources/investigation/29-experimento-diagnostico.md) | El experimento que decide qué capa importa |
| [prototipo-002-diagnostico/](resources/investigation/prototipo-002-diagnostico/) | Benchmark de solucionador; A0 == E sin historial |
| [prototipo-003-aprendizaje/](resources/investigation/prototipo-003-aprendizaje/) | Registro exploratorio; su conclusión fue retirada por el 004 |
| [prototipo-004-validez/](resources/investigation/prototipo-004-validez/) | Validación con protocolo congelado: las macros no amplían capacidad |
| [15-respuesta-directa.md](resources/investigation/15-respuesta-directa.md) | La respuesta corta a la pregunta central |
| [21-revision-critica-fuentes.md](resources/investigation/21-revision-critica-fuentes.md) | Qué evidencia sostiene qué, en dos ejes |
| [23-marco-de-validez.md](resources/investigation/23-marco-de-validez.md) | Fenómeno, traducción y ventaja comparativa |
| [25-protocolo-fuentes-primarias.md](resources/investigation/25-protocolo-fuentes-primarias.md) | Cómo se buscan y evalúan las fuentes |
| [27-plan-de-implementacion.md](resources/investigation/27-plan-de-implementacion.md) | Qué se implementa y qué no (JANUS-C) |
| [precedentes/](resources/investigation/precedentes/) | Qué se ha intentado, incluidos los competidores 2026 |
| [papers/](resources/investigation/papers/) | CUMULUS (EN/ES), revisión v0.2 y JANUS v0.2 |

## Las tres líneas

1. **CUMULUS** — hipótesis de portabilidad: contratos procedurales agnósticos al
   modelo, auditoría ciega y enrutamiento por portabilidad. En revisión; su
   novedad amplia fue retirada.
2. **JANUS** — hipótesis de validación: memoria con identificabilidad declarada,
   sin prometer causalidad cuando no se puede estimar. En revisión.
3. **ESCM** — línea fundamental: memoria experimental y autocorrectiva, con
   incertidumbre, ignorancia, agenda de experimentos y anti-persistencia
   selectiva. Pendiente de experimento.

## Lo que este proyecto no afirma

- Que la biología justifique una arquitectura.
- Que CUMULUS o JANUS sean superiores sin evidencia comparativa.
- Que la memoria contrafactual sea un terreno inexplorado.
- Que persistir abstracciones siempre mejore al agente.
- Que la capa social mejore el aprendizaje por sí sola.

## Estructura

```
docs/plan.md                     rondas y criterios
resources/investigation/         investigación, precedentes, papers
```

## Repositorio

https://github.com/jdsalasca/open-human-memory

Documentos de trabajo, no arbitrados. La afiliación MIT es la declarada por el
autor humano y debe verificarse antes de un envío; la participación de IA debe
declararse conforme a las normas del venue.
