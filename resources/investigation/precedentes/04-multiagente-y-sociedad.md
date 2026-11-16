# 04 — Memoria en sistemas multiagente y sociales

## De la mente social a la sociedad de agentes

Minsky (1986) propuso la mente como una **sociedad de agentes** especializados
que compiten y cooperan. La metáfora inspiró arquitecturas multiagente, pero la
mayoría de los sistemas actuales traduce "sociedad" a **varios LLM conversando**,
no a una división del trabajo de memoria.

## Memoria compartida en productos

- **Mem0 / Zep**: permiten namespace por usuario o sesión; la "memoria
  compartida" es un espacio de nombres, no una institución.
- **Generative Agents** (Park et al., 2023): los agentes recuerdan e interactúan;
  la memoria social emerge de la simulación, no de un protocolo.
- **Multi-agent debate** (Du et al., 2023): varios agentes proponen y critican;
  mejora la factualidad en algunas tareas, pero no persiste conocimiento.

## Lo que la sociología aporta y casi nadie implementa

- **Memoria transactiva** (Wegner, 1987): el grupo no recuerda en conjunto;
  divide la memoria y mantiene un directorio de "quién sabe qué". Los equipos con
  buena memoria transactiva rinden mejor (Lewis, 2003; Ren y Argote, 2011).
- **Comunidades de práctica** (Lave y Wenger, 1991): el novato aprende
  participando periféricamente, con un repertorio compartido.
- **Cultura acumulativa** (Tomasello, 1999; Henrich, 2015): la fidelidad de
  transmisión es lo que permite que el conocimiento no se pierda en cada salto.
- **Gobernanza de comunes** (Ostrom, 1990): reglas de acceso, monitoreo y
  sanción para un recurso compartido.

## Lo que la biología social aporta

- **Orcas**: matrilinas, dialectos, custodias post-reproductivas, enseñanza
  intencional (Brent et al., 2015; Guinet y Bouvier, 1995).
- **Hormigas**: estigmergia con evaporación, quórum, umbrales de tarea (Grassé,
  1959; Pratt et al., 2002).
- **Abejas**: baile como broadcast de descubrimientos (von Frisch, 1967).

## El estado real de la coordinación multiagente

La mayoría de los frameworks (AutoGen, CrewAI, LangGraph, Colmena) orquestan
**turnos y herramientas**, no memoria. Lo que se comparte es el contexto o un
archivo; no hay:

- directorio de expertise con calibración,
- protocolo de enseñanza con verificación de fidelidad,
- reputación basada en resultados,
- auditoría ciega entre agentes,
- gobernanza de escritura y contradicciones,
- preservación del disenso.

## El riesgo documentado

Ashery, Aiello y Baronchelli (2025) muestran que poblaciones de agentes LLM
desarrollan convenciones espontáneas y **sesgos colectivos** aunque cada
individuo parezca neutral. La memoria compartida puede amplificar errores.

**Conclusión:** la capa social no es un adorno. Sin gobernanza, compartir memoria
es compartir sesgo con alta eficiencia.

## El hueco

La memoria multiagente se trata como **almacenamiento compartido**, no como
**sociedad del conocimiento**. Faltan:

1. **Directorio transactivo** operativo (quién sabe qué, con qué evidencia).
2. **Enseñanza verificada** (el aprendiz ejecuta; se mide fidelidad).
3. **Auditoría ciega** (el verificador no ve al autor).
4. **Reputación calibrada** (éxito por dominio, no volumen).
5. **Gobernanza** (procedencia, permisos, contradicciones, caducidad).

CUMULUS propone estas piezas. La pregunta abierta es si una sociedad de agentes
puede **acumular conocimiento sin acumular sesgo**. Esa es una hipótesis
empírica, no un eslogan.
