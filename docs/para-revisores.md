# Guía para revisores

**Versión:** `v1.25-review` · 16 de noviembre de 2026
**Manuscrito:** [`manuscrito.md`](manuscrito.md)
**Repositorio:** https://github.com/jdsalasca/open-human-memory
**Tag de referencia:** `v1.25-review`

Esta guía existe para que un revisor externo pueda evaluar el trabajo sin leer
treinta documentos. Si algo no está aquí, es un defecto del repositorio.

---

## 1. Qué se somete

Un **programa experimental metodológico** con tres partes:

1. **Resultados negativos** (002–007): en espacios enumerables, identificables y
   presupuestados, la memoria no amplía cobertura; solo reduce coste, y de forma
   condicional.
2. **Diagnóstico** (007B, EXEC-001, LIRE-002): por qué los negativos no eran
   interpretables como falta de memoria. La aplicación de programas y la evaluación
   de condiciones son cuellos separados del almacenamiento.
3. **Primer resultado positivo condicionado** (MEM-002/003/004): en tareas de **2
   operaciones efectivas**, un artefacto **verificado fuera del prompt** y presentado
   como **conocimiento aplicable** se usa: 10–11/12 frente a 3–5/12 del clon, 2–3/12
   del placebo y 0/12 de un placebo etiquetado como verificado.

No se somete una arquitectura nueva ni una teoría general de memoria. Se somete un
**instrumento de medición** y la evidencia que produce, incluida la evidencia de que
el resultado positivo **no** es expansión de competencia.

---

## 2. Las tres fases, en una tabla

| Fase | Experimentos | Qué establece |
|---|---|---|
| **Negativos** | 002, 003, 004, 005, 006-A′, 006-B, 007 | La memoria episódica/biblioteca no amplía cobertura en el régimen enumerable; reduce coste de forma condicional; la política de activación no paga; el agente real acierta 46,9 % |
| **Diagnóstico** | 007B, EXEC-001, LIRE-002 | El 007 estaba fuera de la ejecución (oráculo 2/12 en 5 pasos); en 2 operaciones el modelo aplica 86 %, en 3 el 44 %, en 5 el 0–33 %; LIRE-001b era redundante; con información independiente, el control sin tabla acierta 0/7 y el fallo está en la condición |
| **Positivo condicionado** | MEM-002, MEM-003, MEM-004, MEM-005 | En 2 operaciones, un procedimiento correcto presentado como verificado se usa (10–12/12); el encuadre de candidata lo hunde a 3–4/12; un placebo verificado acierta 0–1/12. **MEM-005 muestra que un programa escrito por un programador, sin aprendizaje previo, rinde igual (12/12): la ventaja es contenido + instrucción, no adquisición.** Las tareas ya son identificables desde los dos ejemplos |

---

## 3. Qué se afirma (claims principales)

| ID | Afirmación | Nivel | Dato |
|---|---|---|---|
| T1 | En espacio explorable, identificable y presupuestado, la memoria no amplía cobertura | E0 + 004/006 | 004-A: A1 64/64; A3 54/64 |
| V1 | Con continuidad total, 41,8 % menos pasos con igual cobertura | E2 local | 005 |
| V2 | Con continuidad cero, 22,1 pp menos de acierto | E2 local | 005 |
| P2 | La política aprendida no supera una regla simple (−1,0 pp) | E2 local | 006-A′ |
| L1 | `gpt-6-luna` low acierta 30/64 (46,9 %) sin historial | E2 local | 006-B |
| L5 | Sin la tabla, el modelo acierta 0/7 casos positivos | E2 local | LIRE-002 |
| L6 | Hay representaciones con 6–7/7 positivos y menos tokens que el español | E2 local | LIRE-002 |
| E1 | Con el programa completo, 2 operaciones aciertan ≥10/12 | E2 local | EXEC-001: 11/12 |
| E2 | La profundidad nominal no es monótona | **Refutada** como orden | EXEC-001: 3 ops 7/12; 4 ops 8/12 |
| E4 | La longitud mínima equivalente separa mejor que la nominal | E2 local, cualitativa | EXEC-001 |
| M1–M3 | En 3 operaciones, la memoria de 2 operaciones no supera clon, placebo ni historial | **Refutadas** | MEM-002: 3 vs 2/5/4 |
| M5 | El encuadre definitivo supera al de candidata en ≥3 pares | E2 local | MEM-003: 11 vs 4 (7 pares) |
| M8 | La memoria verificada supera al placebo en ≥3 pares | E2 local | MEM-003: 11 vs 3 (8 pares); MEM-004: 10 vs 2 (9 pares) |
| M10 | La memoria verificada supera al placebo verificado en ≥3 pares | E2 local | MEM-004: 10 vs 0 (10 pares, p=0,002) |
| M13 | Con contenido correcto, estado verificado e instrucción de aplicar, el contenido supera al placebo | E2 local | MEM-005: 12 vs 1 (11 pares, p=0,001) |
| M14 | Con contenido correcto e instrucción de aplicar, el estado verificado supera a la candidata | E2 local | MEM-005: 12 vs 9 (3/0, p=0,25; direccional) |
| M15 | Con contenido correcto y estado verificado, aplicar supera a verificar | E2 local | MEM-005: 12 vs 8 (4/0, p=0,125; direccional) |
| M16 | El programa escrito por un programador queda a ≤2 pares del aprendido | E2 local | MEM-005: 12/12 vs 12/12 (0 pares) |
| M11–M12 | Réplica de 24 tareas: verificada ≥20/24 y > candidata en ≥6 pares | **Abiertas** | No ejecutadas |

**Ninguna alcanza E3** (varias distribuciones), **E4** (tareas reales) ni **E5**
(longitudinal). El manuscrito lo dice.

---

## 4. Qué **no** se afirma

- Que la memoria no sirva a los agentes.
- Que las habilidades no funcionen.
- Que exista novedad algorítmica.
- Que haya transferencia entre modelos ni formación conceptual.
- **Que el resultado de MEM-003/004/005 sea expansión de competencia.** La tarea de 2
  operaciones es enumerable e identificable; la memoria ahorra el coste de
  identificarla, no amplía el espacio de lo que el agente puede expresar.
- **Que las tareas requieran información que el clon no tenga.** Las doce tareas ya
  están determinadas por los dos ejemplos de soporte; el artefacto entrega el programa
  explícito. El resultado mide **inferir frente a recibir**.
- **Que la adquisición previa aporte algo.** MEM-005: un programa escrito por un
  programador, sin aprendizaje previo, acierta 12/12, igual que el aprendido. La
  ventaja es contenido + instrucción, no memoria.
- **Que el modelo verifique por sí mismo.** El placebo verificado (0–1/12) muestra que
  aplica un programa falso si la etiqueta dice «verificado». La verificación es
  externa; el modelo no puede ser el verificador de su propia memoria.
- **Que haya recuperación autónoma.** El evaluador entrega el artefacto; no hay
  selección entre varias memorias.
- **Que haya transferencia a familias reservadas.** Las tareas empiezan por el motivo
  aprendido; es reutilización favorable, no generalización.
- **Que el resultado sea general.** n=12 por condición, una semilla, un modelo
  (`gpt-6-luna` low); la réplica de 24 tareas está pre-registrada y no ejecutada.
- **Que el modelo pueda verificar su propia memoria.** La etiqueta «verificado» debe
  provenir de una verificación externa; un programa falso etiquetado como verificado
  acierta 0/12 y se aplica con confianza.
- Que la revisión de literatura sea exhaustiva.
- Que los resultados de terceros estén replicados.

---

## 5. Cómo verificar

### 5.1 Tests y registro

```bash
python -m unittest discover -s tests -v          # 87 tests
python docs/verificar_afirmaciones.py            # 100 claims, totales citados
```

### 5.2 Reproducir los experimentos clave

```powershell
# LIRE-002: información independiente + control sin tabla
python -m ohmem.lire_002 --model gpt-6-luna --effort low --timeout 120 --out resources/investigation/lire-002/results/luna-low-12cases.json
python resources/investigation/lire-002/analyze.py

# EXEC-001: mapa de aplicación
foreach ($s in 0,1,2,3) { python -m ohmem.v7_transfer --n 12 --support 2 --suffix $s --session1-examples 12 --exact-ops --conditions oracle --model gpt-6-luna --effort low --timeout 120 --out "resources/investigation/exec-001/results/oracle-depth-$($s+2).json" }
python resources/investigation/exec-001/analyze.py

# MEM-003: encuadre
python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 --session1-examples 12 --exact-ops --conditions clone,memory,memory_verified,placebo,history,oracle --model gpt-6-luna --effort low --timeout 120 --out resources/investigation/mem-003/results/pilot-depth2-framing.json
python resources/investigation/mem-003/analyze.py

# MEM-004: placebo verificado
python -m ohmem.v7_transfer --n 12 --support 2 --suffix 0 --session1-examples 12 --exact-ops --conditions clone,memory,memory_verified,placebo,placebo_verified,history,oracle --model gpt-6-luna --effort low --timeout 120 --out resources/investigation/mem-004/results/pilot-depth2-verified-placebo.json
python resources/investigation/mem-004/analyze.py

# MEM-005: factorial + programa escrito
python -m ohmem.mem_005 --n 12 --seed 1 --support 2 --session1-examples 12 --exact-ops --model gpt-6-luna --effort low --timeout 120 --out resources/investigation/mem-005/results/factorial-seed1.json
python resources/investigation/mem-005/analyze.py
```

### 5.3 Trazabilidad

| Resultado | Datos crudos | Análisis |
|---|---|---|
| LIRE-001b (retractado) | `lire-001b/results/luna-low-12cases.json` | `docs/errata-lire-001b.md` |
| LIRE-002 | `lire-002/results/luna-low-12cases.json` | `lire-002/analyze.py` |
| EXEC-001 | `exec-001/results/oracle-depth-{2,3,4,5}.json` | `exec-001/analyze.py` |
| MEM-002 (3 y 2 ops) | `mem-002/results/pilot-depth{3,2}.json` | `mem-002/analyze.py` |
| MEM-003 | `mem-003/results/pilot-depth2-framing.json` | `mem-003/analyze.py` |
| MEM-004 | `mem-004/results/pilot-depth2-verified-placebo.json` | `mem-004/analyze.py` |
| MEM-005 | `mem-005/results/factorial-seed1.json` | `mem-005/analyze.py` |

Los JSON contienen las filas por condición, tarea y programa, con la respuesta, el
valor esperado, los tokens y los segundos. No se publican solo los resúmenes.

---

## 6. Limitaciones declaradas

1. **Un entorno sintético** de seis operaciones; no es un benchmark de LLM.
2. **Un modelo** (`gpt-6-luna`), un esfuerzo (`low`), una semilla; las corridas con
   `gpt-6.1-terra` son exploratorias y no se usan como evidencia.
3. **n=12 por condición** en LIRE-002, EXEC-001 y MEM; la réplica de 24 tareas está
   pre-registrada y pendiente.
4. **Las tareas empiezan por el motivo** aprendido: reutilización favorable, no
   transferencia.
5. **La etiqueta «verificado» es una frase del prompt** en el experimento. Un sistema
   real necesita verificación externa; el placebo verificado (0/12) muestra el riesgo.
6. **El historial tiene más tokens** que la memoria verificada; no se iguala longitud.
7. **LIRE-002**: idioma, longitud y estructura siguen confundidos; no es un factorial;
   LLMLingua-2 no se ejecutó.
8. **EXEC-001**: solo condición simbólica; `steps` y `nl` pendientes; la longitud
   mínima se calcula sobre 60 sondas, no es una prueba formal.
9. **Sin baseline externo reproducido**, sin `ACTUAL-RETRIEVAL` y sin ciclo
   longitudinal `E`/`K`/`P`.
10. **Los negativos del 006** conservan sus limitaciones: presupuesto que puede
    rebasarse hasta 6 pasos, IC con dos semillas, condición de herramienta inválida.
11. **Las doce tareas de MEM son identificables desde los dos ejemplos**: el clon
    tiene la información; el artefacto entrega el programa explícito. El resultado
    mide **inferir frente a recibir**, no un hecho que solo estuviera en la memoria.
12. **MEM-002/003/004 comparten las mismas 12 tareas y semilla**: no son réplicas
    independientes; la réplica de 24 tareas y varias semillas está pendiente.
13. **El contraste candidata/verificado cambia estado e instrucción**; MEM-005 los
    separa en un factorial 2×2×2 con control de programa escrito por un programador.
14. **No hay recuperación autónoma**: el evaluador entrega el artefacto. **MEM-004 vs
    clon no alcanza p < 0,05** (p = 0,0625); los p no corrigen por comparaciones
    múltiples y el orden era fijo en MEM-002/003/004.
15. **MEM-005**: un programa escrito por un programador rinde igual que el aprendido
    (12/12 vs 12/12); la adquisición no añade en esta tarea. Los efectos individuales
    de estado e instrucción son direccionales, no significativos; n=12, semilla 1.

---

## 7. Preguntas para el revisor

1. ¿La proposición de `teoria.md` §3 es correcta con las tres condiciones
   (explorabilidad, identificabilidad, presupuesto) o falta alguna?
2. ¿El resultado de MEM-003/004 mide **uso de memoria** o una ventaja informacional
   trivial? Nuestros controles: clon, placebo, historial y placebo verificado. El
   historial (9–10/12) casi iguala a la memoria verificada (10–11/12): ¿basta eso
   para hablar de memoria, o solo de información?
3. ¿El encuadre definitivo es una manipulación legítima o una forma de dar una
   instrucción privilegiada? El control de placebo verificado (0/12) separa contenido
   de etiqueta; el historial separa programa de experiencias crudas.
4. ¿La longitud mínima equivalente es una buena medida de dificultad? Se calcula
   sobre 60 sondas; no es una prueba formal.
5. ¿El control sin tabla de LIRE-002 es suficiente? El acierto total del control es
   5/12 por la estrategia `NONE`; el positivos 0/7 es la métrica principal.
6. ¿Qué aprendió el agente que no pudiera reconstruir a partir de los ejemplos
   presentes en la tarea?
7. ¿La ventaja depende de la experiencia previa o simplemente de recibir el programa
   correcto? MEM-005 incluye el control de programa escrito por un programador.
8. Si un procedimiento está verificado, ¿cómo se establece su ámbito de aplicabilidad,
   su procedencia y el momento en que deja de ser válido?
9. ¿Puede el agente seleccionar el conocimiento correcto entre cien memorias, sin que
   el evaluador le entregue la respuesta?
10. Después de mil experiencias, ¿aprende problemas nuevos con menos ejemplos, menos
    cómputo y mayor fiabilidad que un clon idéntico?
11. ¿Qué afirmación del registro no está respaldada por los datos?
12. ¿Qué haría falta para pasar de «revisión mayor» a «aceptable»? Nuestra apuesta:
    réplica de 24 tareas y varias semillas, segundo modelo, familia reservada,
    baseline externo y ciclo longitudinal.

---

## 8. Historia de las correcciones

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
| 16 nov | Revisión externa `gpt-6.1-terra` | `respuesta-a-revision-externa.md` |
| 16 nov | 007: retención + reinicio + placebo; sin ventaja sobre placebo | `prototipo-007-transferencia/` |
| 16 nov | **LIRE-001b retractado**: las 120 reglas eran una fórmula; `expected()` no comprobaba pertenencia; orden no aleatorizado | `docs/errata-lire-001b.md` |
| 16 nov | **LIRE-002**: información independiente, control sin tabla, tokens pareados | `lire-002/` |
| 16 nov | **007B**: «el cuello es la ejecución» suavizado a «la aplicación del programa»; mecanismo no identificado | `prototipo-007b-transferencia/` |
| 16 nov | **EXEC-001**: mapa de aplicación por profundidad y longitud mínima | `exec-001/` |
| 16 nov | **MEM-002/003/004**: el encuadre era el cuello; la etiqueta no basta | `mem-002/`, `mem-003/`, `mem-004/` |
| 16 nov | **MEM-005**: factorial contenido × estado × instrucción; el programa escrito rinde igual (12/12); la adquisición no añade | `mem-005/` |

El repositorio conserva los resultados antiguos y las erratas. No se reescribió la
historia.
