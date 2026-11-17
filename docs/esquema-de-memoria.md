# Esquema de memoria: conocimiento y evidencia sobre el conocimiento

**Fecha:** 17 de noviembre de 2026
**Estado:** propuesta de representación; **no implementada**.
**Uso:** MEM-006 y la línea LIRE.

La lección de MEM-003/004/005 es que **el conocimiento y la evidencia sobre el
conocimiento son cosas distintas**. Un procedimiento puede ser correcto y, aun así,
estar fuera de su ámbito, haber sido verificado solo en una distribución o haber
quedado obsoleto. El prompt debe llevar ambos, no solo la secuencia de operaciones.

## Registro propuesto

```yaml
skill_id: ordering_double_v1
procedure:
  - sort_asc
  - double
verification:
  status: passed            # passed | failed | unknown
  method: external_tests    # harness, 60 probes
  tested_scope: integer_lists
  probes: 60
applicability:
  requires:
    - input_is_integer_list
  invalid_when:
    - operation_semantics_changed
    - input_contains_non_integers
provenance:
  source: learned_from_examples
  evidence_count: 12
  acquired_at: 2026-11-17
decision:
  recommended: apply_if_preconditions_hold
  confidence: local
```

## Por qué estos campos

| Campo | Qué separa |
|---|---|
| `procedure` | El conocimiento: qué hacer |
| `verification.status` | Si el harness lo comprobó; no una frase del modelo |
| `verification.tested_scope` | Dónde se comprobó; no implica validez universal |
| `applicability.requires` | Cuándo se puede usar |
| `applicability.invalid_when` | Cuándo hay que rechazarlo o revisarlo |
| `provenance` | De dónde vino: aprendizaje, experto, síntesis |
| `decision` | Qué recomienda el sistema, con su confianza |

**Regla:** el modelo **no puede escribir** `verification.status: passed`. Lo escribe el
harness tras ejecutar las pruebas. Si el modelo o un generador pueden declararse
verificados, el placebo verificado de MEM-004/005 (0–1/12) se convierte en un fallo
de seguridad.

## Cómo se usa en MEM-006

- La biblioteca contiene 8 registros.
- El recuperador ve la tarea (2 ejemplos) y los metadatos; debe elegir un `skill_id`.
- La condición `expert_written` usa los mismos procedimientos con
  `provenance.source: expert`; así se separa contenido de adquisición.
- La condición de obsolescencia cambia `invalid_when`; el sistema debe rechazar la
  habilidad o marcarla para revisión.

## Conexión con las líneas

- **LIRE:** ¿qué representación del registro conserva `procedure`, `verification` y
  `applicability` con menos tokens y más fidelidad? El registro es el nuevo objeto de
  compresión, no una tabla de reglas.
- **CUMULUS:** cómo transportar el registro entre modelos sin perder procedencia ni
  ámbito.
- **JANUS:** cómo evaluar la evidencia que justifica `verification.status` y
  `decision`.

## Lo que no es

No es un certificado de seguridad, no es una prueba formal y no sustituye la
verificación externa. Es una estructura para que el agente pueda distinguir **qué
sabe, por qué lo sabe, dónde se aplica y cuándo debe desconfiar**.
