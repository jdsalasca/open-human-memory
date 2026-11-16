# Papers

Documentos de trabajo del proyecto. No arbitrados; no reportan resultados
empíricos.

| Archivo | Tema | Idioma |
|---|---|---|
| [cumulus-final-es.md](cumulus-final-es.md) | CUMULUS v1.0 final | Español |
| [cumulus-final-en.md](cumulus-final-en.md) | CUMULUS v1.0 final | English |
| [janus-final-es.md](janus-final-es.md) | JANUS v1.0 final | Español |
| [cumulus-en.md](cumulus-en.md) | CUMULUS v0.1 histórica | English |
| [cumulus-es.md](cumulus-es.md) | CUMULUS v0.1 histórica | Español |
| [cumulus-revision-v0.2.md](cumulus-revision-v0.2.md) | Alcance corregido tras la revisión mayor | Español |
| [janus-es.md](janus-es.md) | JANUS v0.1 histórica | Español |
| [janus-v0.2.md](janus-v0.2.md) | JANUS v0.2: identificabilidad declarada | Español |

**Autores:** Juan David Salas Camargo (MIT) y DeepSeek / DeepSeek 4.1 Flash.

## CUMULUS

**Pregunta:** ¿puede un agente acumular procedimientos durante meses,
transferirlos entre modelos y mejorar sin reentrenar el LLM?

**Idea:** habilidades como artefactos ejecutables agnósticos al modelo (SIR),
compiladas desde trazas verificadas por ablación causal, y gobernadas por
auditoría ciega, quórum y un ciclo de vida institucional.

## JANUS

**Pregunta:** ¿puede una memoria agéntica aprender la lección correcta si
registra lo que no pasó?

**Idea:** contrafactuales como objetos de primera clase; jerarquía de evidencia
(experimento aleatorio > natural > simulación > juicio del modelo); puerta de
promoción causal para procedimientos; sueño contrafactual; memoria de
casi-fallos y arrepentimiento.

## Relación

CUMULUS responde **¿funciona y es portable?** JANUS responde **¿funcionó por esta
razón?** JANUS usa CUMULUS como sustrato de promoción y portabilidad.
