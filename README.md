# Open Human Memory

Investigación abierta sobre memoria para agentes: qué puede aprender un sistema
de su experiencia, qué puede justificar y cómo evitar que sus errores se
conviertan en certezas permanentes.

> **La pregunta del proyecto.**
> Si mañana este agente reinicia su contexto, cambia de tarea y encuentra un
> problema que nunca ha visto, ¿qué aprendizaje adquirido en sus experiencias
> anteriores modifica realmente su manera de comprenderlo y resolverlo?
>
> **Respuesta actual, en dos partes.** En tareas que el modelo no puede aplicar, no
> hay evidencia: el 007 pedía cinco operaciones y el oráculo mismo acertaba 2/12. En
> una tarea de **dos operaciones efectivas**, un artefacto **verificado fuera del
> prompt** y presentado como conocimiento aplicable se usa: 10–11/12 frente a 3–5/12
> del clon. Eso es **uso de un procedimiento correcto**, no expansión de competencia:
> las doce tareas ya son identificables desde los dos ejemplos, el clon tiene la
> información y el artefacto ahorra el coste de inferirla. Ver
> [`docs/programa-de-investigacion.md`](docs/programa-de-investigacion.md).

**Estado:** programa de investigación con un **diagnóstico ejecutable** y un **primer
resultado positivo condicionado**. No hay producto; hay un harness mínimo para
separar información, aplicación, verificación y encuadre antes de construir otra
arquitectura. Un procedimiento correcto presentado como verificado se usa en 2
operaciones; las tareas ya son identificables desde los ejemplos y un programa escrito
por un programador rinde igual, así que no es adquisición ni expansión de competencia.

## Cómo leer este repositorio

El orden importa. Para revisión por pares, empieza por el manuscrito.

0. **[`docs/manuscrito.md`](docs/manuscrito.md)** — el trabajo completo en formato de
   artículo: hipótesis, método, resultados, diagnóstico, resultado positivo
   condicionado, discusión, límites y referencias.
   **[`docs/para-revisores.md`](docs/para-revisores.md)** — mapa, claims, trazabilidad
   y comandos para verificar cada número.
   **[`docs/registro-de-ejecuciones.md`](docs/registro-de-ejecuciones.md)** — modelo,
   esfuerzo, semillas, comandos y número de llamadas de cada experimento.
1. **[`docs/programa-de-investigacion.md`](docs/programa-de-investigacion.md)** — el
   programa rector: memoria útil, lenguaje útil y comunicación aprendida.
2. **[`docs/teoria.md`](docs/teoria.md)** — qué se afirma, por qué, qué canales
   existen y qué predicciones se derivan. Incluye la proposición del espacio
   enumerable y la distinción entre **uso de memoria** y **expansión de competencia**.
3. **[`docs/registro-de-afirmaciones.md`](docs/registro-de-afirmaciones.md)** — cada
   afirmación con estado, nivel de evidencia y falsador. Si no está aquí, no existe.
4. **[`docs/plan.md`](docs/plan.md)** — rondas con puertas. Ninguna empieza con
   código.

Los documentos históricos, los prototipos y los papers son **registro**. Si
contradicen la teoría o el registro de afirmaciones, se corrigen ellos. Las
retractaciones están en [`docs/errata-006b.md`](docs/errata-006b.md) y
[`docs/errata-lire-001b.md`](docs/errata-lire-001b.md).

## Inicio rápido

```bash
python -m unittest discover -s tests -v          # 87 tests
python docs/verificar_afirmaciones.py            # 95 claims
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

La respuesta corta, después de los experimentos 002–007 y del diagnóstico
007B/EXEC-001: **el mecanismo de macros que probamos no amplía lo que el agente puede
expresar; abarata encontrarlo, y solo mientras el futuro se parezca al pasado.** Con
continuidad total, una biblioteca aprendida iguala la cobertura y usa 41,8 % menos
cómputo. Con continuidad cero, el mismo cómputo rinde 22,1 pp menos.

Un **procedimiento correcto presentado como verificado** sí se usa en una tarea de dos
operaciones: 10–11/12 frente a 3–5/12 del clon, 2–3/12 del placebo y 0/12 de un placebo
etiquetado como verificado. Eso es **uso de información**, no expansión: las doce
tareas ya son identificables desde los dos ejemplos, el clon tiene la información y el
artefacto ahorra el coste de inferirla. La expansión sigue sin demostrarse; exige una
tarea que el modelo pueda
aplicar y que no quepa en el presupuesto.

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

## 007: retención real, reinicio y placebo (negativo)

Primera prueba con retención genuina: el agente aprende un procedimiento, **nosotros
lo verificamos** con 60 entradas, se reinicia el contexto y lo aplica a
composiciones de cinco pasos.

**Con `gpt-6-luna` low (modelo de experimentos), la adquisición falló con seis
ejemplos:** el programa devuelto no reprodujo el motivo y el experimento **abortó
antes de la sesión 2**, como está diseñado. Con **doce ejemplos y «exactamente dos
operaciones»** verificó (`double → sort_asc`, equivalente).

| Régimen (`luna` low) | `clone` | `memory` | `placebo` |
|---|---|---|---|
| 1 ejemplo de soporte | 0/12 | 0/12 | 2/12 |
| 2 ejemplos de soporte | 1/12 | 3/12 | **6/12** |

Con un ejemplo, el clon está en el suelo. Con dos, **el placebo acierta el doble que
la memoria** (cuatro tareas discordantes a favor del placebo, una a favor de la
memoria; p = 0,38). El artefacto verificado no supera a uno falso: **no hay ventaja
atribuible al contenido retenido**.

El diagnóstico **007B** añadió dos condiciones: **historial de origen** (los 12 pares
de la sesión 1) y **oráculo** (el programa completo). Resultado con `luna` low:
clon 1/12, memoria 3/12, placebo 6/12, historial 4/12, **oráculo 2/12**. Con el
programa completo, el modelo apenas resuelve 2 de 12 tareas: **el cuello está en la
aplicación del programa, no en la memoria**. No se distingue todavía si falla la
ejecución, la interpretación de las operaciones, el seguimiento de instrucciones o
una heurística. La familia de 5 pasos exige más de lo que `luna` low aplica de forma
fiable; el siguiente paso es medir esa capacidad (EXEC-001) antes de volver a la
memoria. Detalle en
[`prototipo-007b-transferencia/`](resources/investigation/prototipo-007b-transferencia/).

La corrida con terra (exploratoria, no evidencia) mostró el mismo problema por
arriba: clon 9–12/12, memoria 11/12 y placebo 11/12. Tampoco discrimina.

## LIRE-001b (retractado): las 120 reglas eran una sola fórmula

> **Retractado como medida de información.** Cada regla era `C{i}` / umbral `{i}` /
> `S{i}`: una fórmula reconstruye la tabla. El verificador no comprobaba la
> pertenencia del código y el orden de casos no estaba aleatorizado. Las cifras de
> abajo describen el seguimiento de una tabla redundante, no información retenida.
> Ver [`docs/errata-lire-001b.md`](docs/errata-lire-001b.md) y **LIRE-002**.

120 reglas, doce casos, **`gpt-6-luna` low** (modelo de experimentos):

| Representación | Acierto | Caracteres | Bytes | Tokens (mín.) |
|---|---|---|---|---|
| Español | 8/12 | 9.267 | 9.388 | 28.250 |
| Inglés | 10/12 | 9.034 | 9.034 | 28.100 |
| Chino | **11/12** | **4.258** | 8.412 | 27.861 |
| Español conciso | 8/12 | **3.052** | **3.295** | **26.534** |
| DSL simbólico | 7/12 | 4.963 | 4.963 | 27.009 |

- **El ahorro es real pero pequeño:** 0,5–6,1 % de la llamada completa.
- **Todos los fallos son de umbral:** el modelo devuelve el código correcto con el
  estado equivocado, o `NONE` en un caso válido. No es un fallo de búsqueda.
- **El chino es el mejor compromiso:** 11/12 y −1,4 % de tokens.
- **El español conciso y el DSL ahorran más y fallan más:** 4–5 de 12, incluyendo
  falsos negativos.
- La corrida con terra (6/6 en todas) es **exploratoria y no se usa**.

Detalle y límites en [`lire-001b/`](resources/investigation/lire-001b/).

## LIRE-002: el idioma no era el problema; la condición sí

Tabla de 120 reglas con **código, umbral, estado y excepción aleatorios e
independientes** (~3.759 bits), 12 casos estratificados y **control sin tabla**.
`gpt-6-luna` low:

| Representación | Positivos | Secundarios | Total | Tokens incr. |
|---|---|---|---|---|
| Español | 6/7 | 4/5 | 10/12 | 2.841 |
| Inglés | **7/7** | **5/5** | **12/12** | 2.605 |
| Chino | **7/7** | 4/5 | 11/12 | **2.949** |
| Español conciso | **7/7** | 3/5 | 10/12 | **1.477** |
| DSL | **7/7** | **5/5** | **12/12** | 2.490 |
| JSON | 6/7 | 2/5 | 8/12 | 2.356 |
| Tabla TSV | 6/7 | 2/5 | 8/12 | **1.400** |
| Sin tabla | **0/7** | 5/5 | 5/12 | 0 |

- **La tabla es necesaria:** sin ella, 0/7 positivos. El 5/12 total es la estrategia
  de responder siempre `NONE`; la métrica estratificada lo desenmascara.
- **La recuperación funciona; la condición falla:** el modelo encuentra la regla,
  pero devuelve el estado cuando el importe no cumple el umbral o falla la excepción.
- **El chino no ahorra tokens** (2.949 vs 2.841) **ni acierta más** (11 vs 10): la
  ventaja de LIRE-001b no se replica con información independiente.
- **La compresión cuesta fidelidad:** tabla −51 % de tokens y 8/12; conciso −48 % y
  10/12; inglés/DSL 12/12 sin compresión.
- Las diferencias entre idiomas no se establecen con 12 casos.

Detalle y límites en [`lire-002/`](resources/investigation/lire-002/).

## MEM-002/MEM-003/MEM-005: un procedimiento correcto presentado como verificado

EXEC-001 mostró que `luna` aplica 2 operaciones al 86 %, 3 al 44–58 % y 5 al 0–33 %.
MEM-002 bajó la tarea a 2 operaciones, donde hay margen. MEM-003 comparó el **mismo
programa** con dos encuadres:

| Condición | Acierto |
|---|---|
| Clon | 3/12 |
| Memoria (candidata) | 4/12 |
| Placebo | 3/12 |
| Historial de origen | 10/12 |
| **Memoria verificada** | **11/12** |
| **Oráculo** | **12/12** |

- **El encuadre y la instrucción explican parte de la diferencia:** el mismo programa
  pasa de 4/12 a 11/12 al presentarlo como «retenido y verificado; aplícalo» en vez
  de «subrutina candidata; verifícala» (7 pares, p = 0,016). El diseño no separa
  cuánto corresponde al estado comunicado y cuánto a la instrucción; MEM-005 lo hace.
- **El contenido importa:** verificada 11/12 vs placebo 3/12 (8 pares, p = 0,008).
- **Las doce tareas ya se resuelven con los dos ejemplos:** el clon tiene la
  información; el artefacto entrega el programa explícito. El resultado mide
  **inferir frente a recibir**, no un hecho que solo estuviera en la memoria.
- **La etiqueta sola no basta:** en MEM-004, un programa falso etiquetado «verificado»
  acierta **0/12**; la memoria verificada, 10/12 (10 pares, p = 0,002). El modelo no
  verifica por sí mismo: aplica el programa falso. El placebo verificado es
  **obediencia peligrosa**, no seguridad.
- **El procedimiento correcto presentado como verificado empata con el historial y el
  oráculo** (11, 10 y 12 sobre 12); el artefacto comprimido conserva la información en
  este régimen.
- **El encuadre de candidata es tóxico:** 4/12, peor que el historial (10/12). Pedir
  verificación en cada uso hace que el modelo desaproveche un procedimiento ya
  verificado.
- **Condición de seguridad:** la etiqueta «verificado» debe provenir de una
  verificación real fuera del prompt; un artefacto falso etiquetado así se aplica y
  falla. El modelo no puede ser el verificador de su propia memoria.

### MEM-005: el factorial y el control escrito

MEM-005 separó contenido, estado e instrucción (2×2×2) y añadió un **programa escrito
por un programador** sin sesión previa, con orden aleatorizado por tarea y semilla 1:

| Condición | Acierto |
|---|---|
| Clon | 6/12 |
| Correcto · candidata · verificar | 8/12 |
| Correcto · candidata · aplicar | 9/12 |
| Correcto · verificada · verificar | 8/12 |
| **Correcto · verificada · aplicar** | **12/12** |
| Placebo · verificada · aplicar | **1/12** |
| **Escrito por un programador** | **12/12** |

- **El efecto grande está en una sola celda:** verificado+aplicar 12/12 vs placebo 1/12
  (11 pares, p = 0,001). Candidato+verificar apenas separa (8 vs 6).
- **El programa escrito por un programador acierta lo mismo que el aprendido**
  (12/12 vs 12/12). **La adquisición previa no añade nada en esta tarea.** El positivo
  es contenido correcto más instrucción definitiva, no memoria acumulativa.
- **La autoridad sobre contenido falso es peligrosa:** placebo+verificado+aplicar
  acierta 1/12. El modelo aplica el programa falso porque la etiqueta dice «verificado».

Detalle en [`mem-002/`](resources/investigation/mem-002/),
[`mem-003/`](resources/investigation/mem-003/),
[`mem-004/`](resources/investigation/mem-004/) y
[`mem-005/`](resources/investigation/mem-005/).

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
| [prototipo-006-agente-llm/](resources/investigation/prototipo-006-agente-llm/) | Línea base del agente: 46,9 % |
| [prototipo-007-transferencia/](resources/investigation/prototipo-007-transferencia/) | Retención + reinicio + placebo: sin ventaja en 5 pasos |
| [prototipo-007b-transferencia/](resources/investigation/prototipo-007b-transferencia/) | Historial, oráculo y aplicación: el cuello no era la memoria |
| [exec-001/](resources/investigation/exec-001/) | Aplicación: 2 ops 86 %, 3 ops 44 %, 5 ops 0–33 % |
| [lire-001/](resources/investigation/lire-001/) | Exploratorio (terra); sustituido por 001b |
| [lire-001b/](resources/investigation/lire-001b/) | **Retractado**: la tabla era una fórmula; ver errata |
| [lire-002/](resources/investigation/lire-002/) | Información independiente: sin tabla 0/7; la condición falla |
| [mem-002/](resources/investigation/mem-002/) | 2 ops: memoria 7/12, historial 9/12, oráculo 11/12 |
| [mem-003/](resources/investigation/mem-003/) | Encuadre: verificada 11/12 vs candidata 4/12 |
| [mem-004/](resources/investigation/mem-004/) | Placebo verificado: el contenido, no la etiqueta |
| [errata-lire-001b.md](docs/errata-lire-001b.md) | La retractación de las 120 reglas |
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
- **Que el resultado de MEM-003/004 sea expansión de competencia.** Es uso de memoria
  en una tarea enumerable de 2 operaciones; ahorra identificación, no amplía el
  espacio de lo expresable.
- **Que la adquisición previa aporte algo.** MEM-005: un programa escrito por un
  programador, sin aprendizaje previo, acierta 12/12, igual que el aprendido.
- **Que las tareas requieran información que el clon no tenga.** Las doce tareas ya
  están determinadas por los dos ejemplos; el artefacto entrega el programa explícito.
  El resultado mide **inferir frente a recibir**.
- **Que haya transferencia a familias reservadas.** Las tareas empiezan por el motivo
  aprendido; es reutilización favorable.
- **Que sea general.** n=12 por condición, una semilla, un modelo; la réplica de 24
  tareas está pre-registrada y pendiente.
- **Que el modelo pueda verificar su propia memoria.** La etiqueta «verificado» debe
  provenir de una verificación externa; un placebo verificado acierta 0/12.
- **Que el chino sea mejor.** LIRE-002 no replica la ventaja; no ahorra tokens ni
  acierta más con información independiente.

## Estructura

```
docs/                        manuscrito, teoría, registro, plan, guía para revisores
resources/investigation/     experimentos, datos crudos, revisión sistemática
src/ohmem/                   harness y experimentos
tests/                       87 tests, sin llamadas al modelo
```

## Repositorio

https://github.com/jdsalasca/open-human-memory

Documentos de trabajo, no arbitrados. La afiliación MIT es la declarada por el
autor humano y debe verificarse antes de un envío; la participación de IA debe
declararse conforme a las normas del venue.




