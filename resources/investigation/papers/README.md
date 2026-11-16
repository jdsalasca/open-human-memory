# Papers

Documentos de trabajo del proyecto. **No arbitrados.** No reportan resultados
empíricos propios más allá de los prototipos sintéticos, y sus notas empíricas
están alineadas con la revisión de antecedentes de noviembre de 2026.

| Archivo | Tema | Idioma |
|---|---|---|
| [cumulus-final-es.md](cumulus-final-es.md) | CUMULUS v1.1 | Español |
| [cumulus-final-en.md](cumulus-final-en.md) | CUMULUS v1.1 | English |
| [janus-final-es.md](janus-final-es.md) | JANUS v1.1 | Español |
| [archive/](archive/) | Versiones históricas (v0.1, v0.2) | ES/EN |

**Autores:** Juan David Salas Camargo (MIT) y DeepSeek / DeepSeek 4.1 Flash.

## Qué afirman y qué no

**CUMULUS** — *¿puede un agente acumular procedimientos y transferirlos entre
modelos sin reentrenar?* Propone artefactos ejecutables agnósticos al modelo,
compilados desde trazas verificadas y gobernados por auditoría.

- **No afirma** que el formato sea nuevo: las skills con aplicabilidad y
  terminación ya existen (SoK, 2026).
- **No afirma** que la verificación por ejecución sea suya: Proof-Gated la
  implementa y muestra 52/538 aserciones confirmadas.
- **Lo que puede reclamar:** si una representación estructurada conserva la
  utilidad al cambiar de modelo y de dominio. Sigue abierto y sin evidencia propia.

**JANUS** — *¿puede una memoria aprender la lección correcta registrando lo que no
pasó?* Propone declarar la identificabilidad de cada afirmación y usar esa
declaración para decidir.

- **No afirma** ser la primera memoria contrafactual.
- **No afirma** que su gate de promoción sea nuevo: Proof-Gated lo implementa.
- **Lo que puede reclamar:** los **niveles de evidencia** que acompañan a cada
  creencia. Sin validación experimental propia.

## Estado

Ambos son marcos exploratorios. La revisión de antecedentes
([`../revision-sistematica/`](../revision-sistematica/README.md)) y el registro de
afirmaciones ([`../../../docs/registro-de-afirmaciones.md`](../../../docs/registro-de-afirmaciones.md))
mandan sobre estos textos si hay conflicto.
