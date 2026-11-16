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

La respuesta corta, después del 005-A: **la experiencia no amplía lo que el agente
puede expresar; abarata encontrarlo, y solo mientras el futuro se parezca al
pasado.** Con continuidad total, una biblioteca aprendida iguala la cobertura y usa
41,8 % menos cómputo. Con continuidad cero, el mismo cómputo rinde 22,1 pp menos.
No hay todavía evidencia de expansión de competencia ni de validación causal.

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

Traducido al problema del contexto: **96 episodios no caben en una ventana; 8
macros sí, y hacen el mismo trabajo con 26 % menos cómputo** — mientras la
distribución se mantenga. Acumular sin criterio empeora. El controlador que debía
decidir *cuándo* confiar en lo guardado falló y lo publico como fallo.

## La política aprende a cambiar; su instrumento la arruina (006)

Prototipo 006-A, protocolo congelado en `frozen.sha256` (protocolo + código +
datos), evaluado en semillas no usadas para diseñar. Decisión binaria por tarea:
usar la biblioteca (profundidad 2, macros primero) o buscar (profundidad 3).

| Condición | Similar | Novel | Mixto | Pasos (mixto) |
|---|---|---|---|---|
| Buscar sin memoria | 81,3 % | 85,4 % | 83,3 % | 59,6 |
| Macros primero | 100 % | 81,3 % | 90,6 % | 44,5 |
| **Política aprendida** | **100 %** | **87,5 %** | **93,8 %** | **42,3** |
| Política ciega (control) | 100 % | 81,3 % | 90,6 % | 44,5 |

Las cuatro predicciones congeladas se cumplieron: la política iguala al oráculo en
el conjunto mixto y recupera **+6,25 pp** en tareas nuevas. Pero el probe de
aplicabilidad cuesta **96–122 pasos** por tarea y la decisión solo ahorra **29**:
**la política no paga su propio instrumento.** Para el 007, el probe tiene que ser
barato —cacheado por firma o índice— o no hay política.

## Un agente real acierta 46,9 % (006-B)

`gpt-6-luna` (esfuerzo `low`), sin historial, sin herramientas, tres ejemplos por
tarea, 64 tareas: **30/64 = 46,9 %**. Nuestro BFS de profundidad 2 acierta 51,6 % y
el de profundidad 3, 100 %.

Dos consecuencias:

- **El banco no está saturado** por un agente general. La frase «el espacio es
  diminuto y enumerable» vale para el solucionador exhaustivo, no para un LLM.
- **Los fallos del agente son de resolución, no de memoria.** Abren el experimento
  que de verdad importa: darle un procedimiento recuperado y medir si sube del
  47 % al techo.

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
