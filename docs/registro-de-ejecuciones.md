# Registro de ejecuciones

**Fecha de compilación:** 16 de noviembre de 2026.
**Entorno:** Windows 11, PowerShell 7, Python 3.13.15, sin dependencias externas
para los experimentos sintéticos. `codex-cli 0.169.0` para los agentes.
**Coste monetario:** no registrado. Se reportan llamadas, tiempo y presupuesto de
pasos; no tarifas.

## Política de modelos

| Contexto | Modelo | Esfuerzo |
|---|---|---|
| OpenCode (agente de investigación) | `deepseek-v4.1-flash-1017` | máximo |
| Codex CLI — análisis, revisión, feedback | `gpt-6.1-terra` | `medium` |
| Codex CLI — **todos los experimentos** | `gpt-6-luna` | `low` |

**Los experimentos se ejecutan solo con `luna` low.** No se comparan modelos: terra
es más capaz por tecnología y cualquier diferencia estaría confundida. Las corridas
con terra de 007 y LIRE son **exploratorias** (calibración y piloto) y **no se usan
como evidencia** en el registro.

`gpt-6-terra` (sin punto) **no existe** para cuentas ChatGPT: se verificó y
responde «model is not supported». El identificador correcto es `gpt-6.1-terra`.

El baseline del 006-B, el 007, las LIRE, EXEC-001 y MEM usan el mismo modelo de
experimento: `gpt-6-luna` low. Eso hace comparables los resultados entre prototipos.

**Mapa de secciones:**

| Sección | Experimento | Modelo | Evidencia |
|---|---|---|---|
| 1–3 | 002–006 (sintéticos y LLM) | `luna` low | Sí (con las limitaciones del 006) |
| 4 | 007 (retención, reinicio, placebo) | `luna` low | Sí; 5 pasos fuera de régimen |
| 4b | 007B (historial, oráculo) | `luna` low | Sí; diagnóstico |
| 5 | LIRE-001b (representación) | `luna` low | **Retractado** |
| 5b | LIRE-002 (información independiente) | `luna` low | Sí |
| 5c | EXEC-001 (aplicación) | `luna` low | Sí; simbólico |
| 5d | MEM-002/003/004 (memoria verificada) | `luna` low | Sí; piloto de 12 tareas |


Este documento existe para que un revisor pueda repetir cada experimento sin
adivinar modelo, versión, semilla ni comando.

---

## 1. Experimentos sintéticos (sin LLM)

Todos usan el mismo solucionador de búsqueda y el mismo generador. No hay
aleatoriedad del modelo: las semillas controlan tareas y ejemplos.

| ID | Protocolo | Semillas | Tamaño | Presupuesto | Comando |
|---|---|---|---|---|---|
| 001 | Smoke test invalidado | 0–2 | 200/50 | — | `python -m ohmem.experiment` |
| 002 | `MEM-*` | 0–2 | 200 train / 50 eval | — | `python -m ohmem.v2_experiment --train 200 --eval 50` |
| 003 | `LEARN-*` | 0–2 | 60 train / 30 eval | profundidad 2 | `python -m ohmem.v3_experiment --train 60 --eval 30` |
| 004-A | `VALID-*` | 0–2 | 64 programas | 120 pasos | `python resources/investigation/prototipo-004-validez/reproduce.py` |
| 005-A | `BUDGET-*` | 0–2 | 96 tareas en 4 fases | 120 pasos | `python resources/investigation/prototipo-005-presupuesto/reproduce.py` |
| 006-A | `POLICY-*` | 0 (desarrollo), 1–2 (evaluación) | 48 tareas por conjunto | 120 pasos | `python resources/investigation/prototipo-006-politica/reproduce_corrected.py` |

**Protocolos congelados:**

- 004-A: `prototipo-004-validez/results/protocolo.sha256` (SHA-256 del protocolo).
  El código de evaluación está en el commit `3a1004f`.
- 006-A: `prototipo-006-politica/results/frozen.sha256` (protocolo + 5 archivos de
  código + datos de semillas 1 y 2). `reproduce.py` aborta si algo cambió.

**Semillas:** 0, 1, 2 salvo donde se indica. La semilla 0 de 006-A se usó para
desarrollo y **no** cuenta como evaluación.

**Métricas:** `candidates`, `executed_steps` (aplicaciones primitivas ejecutadas
hasta el primer contraejemplo), `accuracy`, `library_size`. En 004-A se conserva
`primitive_ops` como cota superior por trazabilidad; el 005 y el 006 usan el
contador exacto.

---

## 2. Diagnóstico con agente real (006-B)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| `reasoning_effort` | `low` |
| CLI | `codex-cli 0.169.0` |
| Cuenta | ChatGPT |
| Sandbox | `read-only` (excepto `tool`, `workspace-write`) |
| Modo | `--ephemeral --skip-git-repo-check` |
| Salida | JSON Schema `{"query_output": [int]}` |
| Fecha | 16 de noviembre de 2026 |

**Llamadas:** 209 en total.

| Condición | Tareas | Llamadas | Archivo |
|---|---|---|---|
| `base` (3 ejemplos) | 64 | 64 | `gpt-6-luna-low-seed0.json` |
| `base` pareado | 24 | 24 | `base-24.json` |
| `more_examples` (6) | 24 | 24 | `more-examples-24.json` |
| `vocabulary` | 24 | 24 | `vocabulary-24.json` |
| `ORACLE-MEMORY` | 24 | 24 | `retrieved-24.json` |
| `tool` (disponible) | 24 | 24 | `tool-24.json` |
| `tool-forced` | 24 | 24 | `tool-forced-24.json` |
| Prueba de transcript | 1 | 1 | — |

**Tiempos:** ~8,8 s por llamada en `base`; ~29,4 s en `tool-forced` (3,3×).
**Código de salida:** 0 en todas las llamadas; el exit del proceso no equivale al
exit del script interno.
**Prompt:** `src/ohmem/llm_ceiling.py`, funciones `prompt_for` y `prompt_for_tool`.
**Reproducir:**

```powershell
$env:PYTHONPATH="src"
python -m ohmem.llm_ceiling --n 64 --model gpt-6-luna --effort low `
  --out resources/investigation/prototipo-006-agente-llm/results/gpt-6-luna-low-seed0.json
python -m ohmem.llm_ceiling --condition more_examples --n 24 --out ...\more-examples-24.json
python -m ohmem.llm_ceiling --condition vocabulary --n 24 --out ...\vocabulary-24.json
python -m ohmem.llm_ceiling --condition oracle_memory --n 24 --out ...\retrieved-24.json
python -m ohmem.llm_ceiling --condition tool --n 24 --out ...\tool-forced-24.json
python resources/investigation/prototipo-006-agente-llm/analyze.py
```

**Advertencias registradas:**

- `retrieved` se construía con `task.solution.program`: es `ORACLE-MEMORY`, no
  recuperación. Ver `docs/errata-006b.md`.
- La muestra `[:24]` son 16 tareas que empiezan por `sort_asc` y 8 por `sort_desc`.
- La condición `tool` no verificó ejecución, validación ni uso; 16/24 trazas
  contienen errores de entorno. No se usa para inferir nada.

---

## 3. Revisión externa

| Campo | Valor |
|---|---|
| Modelo | `gpt-6.1-terra` |
| `reasoning_effort` | `medium` |
| CLI | `codex-cli 0.169.0` |
| Sandbox | `read-only` |
| Fecha | 16 de noviembre de 2026 |
| Prompt | revisión científica del repositorio completo |
| Salida | `resources/investigation/revision-externa/codex-gpt-6.1-terra-medium.md` |

Se intentó primero `gpt-6-terra` (sin punto) y la cuenta ChatGPT lo rechazó. El
identificador correcto es `gpt-6.1-terra`. La salida de `gpt-6-luna` se descartó por
decisión del autor y no se usa.

---

## 4. Prototipo 007 (retención y transferencia)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` (evidencia) · `gpt-6.1-terra` (exploratorio) |
| Esfuerzo | `low` (evidencia) · `medium` (exploratorio) |
| CLI | `codex-cli 0.169.0` |
| Llamadas principales | 37 con luna, 6 ejemplos (abortó en sesión 1) · 74 con luna, 12 ejemplos y soporte 1–2 · 111 con terra (exploratorio) |
| Tareas | 12 por condición |
| Condiciones | `clone`, `memory`, `placebo` |
| Resultado | **luna: con 6 ejemplos la sesión 1 no verificó (abortado); con 12 ejemplos verificó. Soporte 1: 0/0/2. Soporte 2: 1/3/6 — el placebo supera a la memoria** · terra: subrutina 9/11/11; programa completo 10/2/11; 3 ejemplos 12/11/12 |
| Archivos | `prototipo-007-transferencia/results/luna-low-support1-12ex.json`, `luna-low-support2-12ex.json`, `terra-medium-*.json` |

Los smokes de calibración (n=1, n=3, profundidades 7 y 9, n=4) usaron 53 llamadas
adicionales y no se reportan como evidencia. El de n=3 se ejecutó con los probes de
verificación defectuosos; corregidos antes de las corridas principales.

## 4b. 007B (diagnóstico de información, instrucción y ejecución)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| Esfuerzo | `low` |
| Llamadas | 54: 4 de adquisición fallida + 25 de la corrida perdida (reconstruida) + 25 de la corrida limpia |
| Tareas | 12, soporte 2, profundidad 5 |
| Condiciones | `history` y `oracle`; se combinan con `clone`, `memory` y `placebo` del 007 |
| Resultado | clon 1/12, memoria 3/12, placebo 6/12, historial 4/12, **oráculo 2/12**; réplica: historial 3/12, oráculo 3/12 |
| Lectura | con el programa completo el modelo apenas resuelve; el cuello está en la aplicación del programa, no en la memoria |
| Archivos | `prototipo-007b-transferencia/results/luna-low-support2-history-oracle.json`, `...-attempt1.json`, `prototipo-007-transferencia/results/luna-low-support2-12ex.json` |

La adquisición de motivos de 3–4 operaciones se intentó con 12 y 24 ejemplos y
«exactamente N operaciones»; las cuatro llamadas fueron rechazadas por la
verificación. La corrida perdida no escribió el JSON por un fallo de ruta; sus filas
se reconstruyeron de los directorios temporales y se guardan como réplica.

## 5. LIRE-001b (representación con skill larga)

> **Retractado como medida de información.** Las 120 reglas son una fórmula
> (`S{código}` si importe < código); el verificador no comprueba pertenencia y el
> orden no está aleatorizado. Ver `docs/errata-lire-001b.md`. El reemplazo es
> LIRE-002.

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` (evidencia) · `gpt-6.1-terra` (exploratorio) |
| Esfuerzo | `low` (evidencia) · `medium` (exploratorio) |
| Llamadas | 60 con luna · 30 con terra (exploratorio) |
| Métrica | acierto + `input_tokens` mínimo por representación |
| Resultado | **luna (12 casos): chino 11/12; inglés 10/12; español 8/12; conciso 8/12; DSL 7/12; ahorro 0,5–6,1 %** |
| Archivo | `lire-001b/results/luna-low-12cases.json` (evidencia), `luna-low.json` (6 casos), `terra-medium.json` (exploratorio) |

LIRE-001 (regla corta) se ejecutó solo con terra y queda como exploratorio: el arnés
dominaba la medición. No se usa como evidencia.

## 5b. LIRE-002 (información independiente)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| Esfuerzo | `low` |
| Llamadas | 225: 16 de smoke + 17 de una corrida perdida + 96 del piloto + 96 de la corrida corregida |
| Tabla | 120 reglas aleatorias; ~3.759 bits; 12 excepciones |
| Casos | 12: 7 positivos, 5 negativos/inexistentes |
| Condiciones | español, inglés, chino, conciso, DSL, JSON, tabla TSV, sin tabla |
| Métrica | acierto estratificado + tokens incrementales pareados vs sin tabla |
| Resultado | sin tabla 0/7 positivos; inglés y DSL 12/12; español 10/12; chino 11/12; conciso 10/12; JSON y tabla 8/12 |
| Lectura | la recuperación funciona; el fallo está en la condición; el chino no ahorra tokens ni acierta más |
| Archivos | `lire-002/results/luna-low-12cases.json`, `...-pilot-instruction.json` |

## 5c. EXEC-001 (mapa de aplicación)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| Esfuerzo | `low` |
| Llamadas | 52: 4 profundidades × (1 adquisición + 12 oráculo) |
| Tareas | 12 por profundidad (2–5 operaciones) |
| Condición | `oracle`: programa completo simbólico |
| Resultado | 2 ops 11/12; 3 ops 7/12; 4 ops 8/12; 5 ops 4/12 |
| Longitud mínima | 2 ops 18/21; 3 ops 8/18; 4 ops 4/8; 5 ops 0/1 |
| Lectura | el régimen aplicable son 2 operaciones efectivas; la nominal no es monótona |
| Archivos | `exec-001/results/oracle-depth-{2,3,4,5}.json` |

## 5d. MEM-002/MEM-003/MEM-004 (memoria en el régimen aplicable)

| Campo | Valor |
|---|---|
| Modelo | `gpt-6-luna` |
| Esfuerzo | `low` |
| Llamadas | MEM-002: 122 (61 de 3 ops + 61 de 2 ops) · MEM-003: 73 · MEM-004: 85 · MEM-005: 121 · MEM-006: 58 (8 adquisiciones + 50 de evaluación) |
| Tareas | 12 por condición, 2 ejemplos de soporte; MEM-006: 10 tareas, 5 habilidades |
| Condiciones | clon, memoria candidata, memoria verificada, placebo, placebo verificado, historial, oráculo; MEM-005 añade factorial 2×2×2 y programa escrito; MEM-006 añade retrieval, aleatoria, experto y simbólico |
| Resultado MEM-002 (3 ops) | clon 2, memoria 3, placebo 5, historial 4, oráculo 8 |
| Resultado MEM-002 (2 ops) | clon 5, memoria 7, placebo 4, historial 9, oráculo 11 |
| Resultado MEM-003 | clon 3, candidata 4, verificada 11, placebo 3, historial 10, oráculo 12 |
| Resultado MEM-004 | clon 5, candidata 3, verificada 10, placebo 2, placebo verificado 0, historial 9, oráculo 12 |
| Resultado MEM-005 | clon 6; correcto candidato verificar 8, aplicar 9; verificado verificar 8, aplicar 12; placebo verificado aplicar 1; escrito 12 |
| Resultado MEM-006 | clon 8/10; oráculo 8/10; retrieval 7/10 (selección 5/10); aleatoria 1/10; experto 5/10; simbólico 10/10 |
| Lectura | el efecto grande es contenido+verificado+aplicar; el programa escrito rinde igual; en 2 ops con biblioteca, la búsqueda simbólica gana |
| Archivos | `mem-002/results/*.json`, `mem-003/results/*.json`, `mem-004/results/*.json` |

## 6. Revisión de literatura

| Campo | Valor |
|---|---|
| Base | OpenAlex API |
| Fecha de consulta | 16 de noviembre de 2026 |
| Cadenas | 8 por título (2023–2026) |
| Registros | 7.100 identificados, 177 cribados, 43 resúmenes, 31 incluidos |
| Bola de nieve | 6 semillas, 139 referencias, 23 citas directas |
| Límites | una base, un revisor, resúmenes, sin replicación |

Reproducir: `resources/investigation/revision-sistematica/busquedas.md`.

---

## 7. Versiones y artefactos

| Artefacto | Versión / commit |
|---|---|
| Repositorio | `main` (ver `git log`) |
| Etiqueta de revisión | `v1.27-review` |
| Python | 3.13.15 |
| `codex-cli` | 0.169.0 |
| Tests | `python -m unittest discover -s tests -v` (60) |

**Regla:** toda cifra publicada debe poder rastrearse hasta un archivo de
`results/` y hasta este registro. Si falta el modelo, la semilla o el comando, no
está lista para revisión.
