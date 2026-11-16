# Open Human Memory

Investigación abierta sobre memoria para agentes: qué puede aprender un sistema
de su experiencia, qué puede justificar y cómo evitar que sus errores se
conviertan en certezas permanentes.

> **La pregunta del proyecto.**
> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?
>
> Hoy **no podemos responderla con un experimento**. Este repositorio documenta
> por qué, qué hemos medido en su lugar y qué haría falta para responderla.
> Ver [`docs/problema-central.md`](docs/problema-central.md).

**Estado:** programa de investigación con un **diagnóstico ejecutable**. No hay
producto todavía; hay un harness mínimo para decidir qué capa importa antes de
construir otra arquitectura. Seis prototipos han producido, sobre todo, resultados
negativos y correcciones metodológicas.

## Cómo leer este repositorio

El orden importa. Para revisión por pares, empieza por el manuscrito.

0. **[`docs/manuscrito.md`](docs/manuscrito.md)** — el trabajo completo en formato de
   artículo: hipótesis, método, resultados, discusión, límites y referencias.
   **[`docs/registro-de-ejecuciones.md`](docs/registro-de-ejecuciones.md)** — modelo,
   esfuerzo, semillas, comandos y protocolos de cada experimento.
   **[`docs/para-revisores.md`](docs/para-revisores.md)** — mapa, afirmaciones y
   preguntas para un revisor externo.
   **[`docs/respuesta-a-revision-externa.md`](docs/respuesta-a-revision-externa.md)**
   — el informe del revisor automático (`gpt-6.1-terra`) y qué se corrigió. El
   dictamen fue **rechazar en su estado actual**: el trabajo es metodológico y no
   demuestra aprendizaje acumulativo.
1. **[`docs/teoria.md`](docs/teoria.md)** — qué se afirma, por qué, qué canales
   existen y qué predicciones se derivan. Incluye la proposición que explica por
   qué todos nuestros resultados negativos estaban cantados: en un espacio
   explorable, identificable y presupuestado, la memoria no puede ampliar cobertura.
2. **[`docs/registro-de-afirmaciones.md`](docs/registro-de-afirmaciones.md)** — cada
   afirmación con estado, nivel de evidencia y falsador. Si no está aquí, no existe.
3. **[`precedentes/10-matriz-de-antecedentes.md`](resources/investigation/precedentes/10-matriz-de-antecedentes.md)**
   — sustituida por la revisión real:
   **[`revision-sistematica/`](resources/investigation/revision-sistematica/README.md)**
   (7.100 registros identificados, 177 cribados, 31 incluidos, tabla de extracción).
4. **[`docs/plan.md`](docs/plan.md)** — rondas con puertas. Ninguna empieza con
   código.

Los documentos 01–29, los prototipos y los papers son **registro histórico**. Si
contradicen la teoría o el registro de afirmaciones, se corrigen ellos.

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

La respuesta corta, después de cinco prototipos: **el mecanismo de macros que
probamos no amplía lo que el agente puede expresar; abarata encontrarlo, y solo
mientras el futuro se parezca al pasado.** Con continuidad total, una biblioteca
aprendida iguala la cobertura y usa 41,8 % menos cómputo. Con continuidad cero, el
mismo cómputo rinde 22,1 pp menos.

Eso vale **para ese mecanismo en ese universo**, no como ley sobre aprendizaje. La
experiencia podría permitir descubrir una herramienta o una representación que el
agente no poseía; no lo hemos probado. No hay todavía evidencia de expansión de
competencia ni de validación causal.

## Lo que sí sabemos: el valor de la memoria es condicional

Prototipo 005-A. 64 programas de tres primitivas que, medidos por comportamiento,
son **14 funciones distintas**. Media de 3 semillas, pasos primitivos ejecutados
(medidos, no estimados):

| Continuidad pasado→futuro | Sin memoria d3 | Macros d2 |
|---|---|---|
| 0,00 | **100 %** · 58,0 pasos | 78 % · 57,8 |
| 0,25 | **100 %** · 66,5 | 88 % · 51,5 |
| 0,50 | **100 %** · 81,1 | 80 % · 63,1 |
| 0,75 | **100 %** · 88,4 | 93 % · 56,9 |
| **1,00** | **100 %** · 91,0 | **100 % · 52,9** |

En un flujo de 96 tareas con deriva:

| Política | Acierto | Pasos | Biblioteca |
|---|---|---|---|
| Sin memoria | 76,0 % | 6.877 | 4 |
| **Congelar lo aprendido** | **76,0 %** | **5.074 (−26,2 %)** | 8 |
| Aprender siempre | 67,0 % | 5.621 | 12 |
| Tope con desalojo por uso | 64,6 % | 5.562 | 9 |

Traducido: **8 macros sustituyen a 96 episodios con el mismo acierto y 26 % menos
trabajo** en este simulador. No medimos tokens ni contexto real, así que la frase
«96 episodios no caben en una ventana» **se retira**: no la medimos. Y es una
comparación de dos diseños bajo el mismo presupuesto de pasos (profundidad 3 sin
memoria frente a profundidad 2 con macros), **no una ablación limpia de memoria**.

Acumular sin criterio empeora (−8,7 pp). El controlador que debía decidir *cuándo*
confiar en lo guardado falló y lo publiqué como fallo. Después intenté una política
aprendida; la auditoría encontró cinco fallos de implementación y, corregidos, el
resultado también es negativo.

## La política no supera a una regla de una línea (006-A′)

Cinco correcciones: el control «aleatorio» usaba la política entrenada el 97 % del
tiempo; el estado se contaminaba entre condiciones; la regla manual no aplicaba el
orden que decía aplicar; el conjunto mixto estaba concatenado; y el coste del probe
era una cota superior, no una medición. Corregido todo, semillas 1–2, comparación
pareada por tarea:

| Condición | Mixto | Búsqueda + probe (pasos) |
|---|---|---|
| Buscar sin memoria | 83,3 % | 59,5 |
| Macros primero | 90,6 % | 44,5 |
| Regla del probe (una línea) | **93,8 %** | 42,2 + 41,2 = 83,5 |
| Política aprendida | 92,7 % | 43,1 + 41,2 = 84,3 |
| Aleatoria uniforme | 85,4 % | 56,9 |
| Barajada (mismas frecuencias) | 87,5 % | 49,4 |

- **La política pierde contra la regla simple**: −1,0 pp (IC pareado −3,1 a 0).
- Supera a buscar en acierto (+9,4 pp, IC 3,1–15,6) y a su control barajado
  (+5,2 pp, IC 1,0–9,4). La señal aporta algo, pero poco y caro.
- **Cuesta 1,42× la búsqueda sin memoria** (84,3 vs 59,5 pasos) y **1,89× macros
  primero** (84,3 vs 44,5). El probe son 41 pasos y el ahorro frente a buscar, 29.

Se retira la afirmación de que una política aprendida aporta. El 006 corregido es
un resultado negativo, y así queda en el repositorio.

## Un agente real acierta 46,9 % (006-B)

`gpt-6-luna` (esfuerzo `low`), sin historial, sin herramientas, tres ejemplos por
tarea, 64 tareas: **30/64 = 46,9 %**. Nuestro BFS de profundidad 2 acierta 51,6 % y
el de profundidad 3, 100 %.

Dos consecuencias:

- **El banco no está saturado** por un agente general. La frase «el espacio es
  diminuto y enumerable» vale para el solucionador exhaustivo, no para un LLM.
- **Los fallos del agente no son de memoria**, pero tampoco sabemos de qué son:
  el piloto que intentó separarlo tenía tres fallos.

El diagnóstico pareado de 24 tareas **fue invalidado** por la auditoría:

- la condición llamada «memoria» fabricaba el recuerdo con `task.solution.program`,
  es decir, conocía la respuesta; se reetiqueta `ORACLE-MEMORY`;
- la muestra `[:24]` son 16 tareas que empiezan por `sort_asc` y 8 por
  `sort_desc`; ninguna por `add_one` o `double`;
- la condición con intérprete tenía errores de entorno en 16 de 24 trazas y no
  verificó ejecución, validación ni uso del resultado.

**La conclusión «el cuello es identificar la transformación» se retira.** Lo que
queda es una línea base de 46,9 % y una lista de cinco fallos metodológicos.
Detalle en [`docs/errata-006b.md`](docs/errata-006b.md) y el plan en
[`docs/problema-central.md`](docs/problema-central.md).

## Resultado de validez del 004-A: las macros no amplían la capacidad

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
- Los contadores son una **cota superior**; la medición con cortocircuito está en
  el 005. `D8` es post hoc (ver fe de erratas del 004).

Detalles, resultados crudos y protocolos en
[`prototipo-004-validez/`](resources/investigation/prototipo-004-validez/) y
[`prototipo-005-presupuesto/`](resources/investigation/prototipo-005-presupuesto/).

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
| [prototipo-005-presupuesto/](resources/investigation/prototipo-005-presupuesto/) | Memoria bajo presupuesto: continuidad, orden y acumulación |
| [prototipo-006-politica/](resources/investigation/prototipo-006-politica/) | Política de activación congelada: acierta, no paga el probe |
| [prototipo-006-agente-llm/](resources/investigation/prototipo-006-agente-llm/) | Test de techo: `gpt-6-luna` acierta 46,9 % |
| [revision-de-rumbo.md](docs/revision-de-rumbo.md) | Respuesta a la auditoría de dirección y decisión del 007 |
| [teoria.md](docs/teoria.md) | **Documento central:** canales, rivales y predicciones |
| [registro-de-afirmaciones.md](docs/registro-de-afirmaciones.md) | Qué sostenemos, qué refutamos y qué está abierto |
| [plan.md](docs/plan.md) | Rondas F0–F5 con puertas |
| [problema-central.md](docs/problema-central.md) | Análisis previo: las siete capacidades, los cinco confundidores y la escalera |
| [errata-006b.md](docs/errata-006b.md) | Las tres inferencias invalidadas del diagnóstico con LLM |
| [precedentes/10-matriz-de-antecedentes.md](resources/investigation/precedentes/10-matriz-de-antecedentes.md) | Puntero a la revisión; corrige tres errores de la matriz anterior |
| [revision-sistematica/](resources/investigation/revision-sistematica/README.md) | **Revisión ejecutada:** búsquedas, cribado, extracción y síntesis |
| [15-respuesta-directa.md](resources/investigation/15-respuesta-directa.md) | La respuesta corta a la pregunta central |
| [21-revision-critica-fuentes.md](resources/investigation/21-revision-critica-fuentes.md) | Qué evidencia sostiene qué, en dos ejes |
| [23-marco-de-validez.md](resources/investigation/23-marco-de-validez.md) | Fenómeno, traducción y ventaja comparativa |
| [25-protocolo-fuentes-primarias.md](resources/investigation/25-protocolo-fuentes-primarias.md) | Cómo se buscan y evalúan las fuentes |
| [27-plan-de-implementacion.md](resources/investigation/27-plan-de-implementacion.md) | Qué se implementa y qué no (JANUS-C) |
| [precedentes/](resources/investigation/precedentes/) | Qué se ha intentado, incluidos los competidores 2026 |
| [papers/](resources/investigation/papers/) | CUMULUS (EN/ES) y JANUS (ES) v1.1; históricas en `archive/` |

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
