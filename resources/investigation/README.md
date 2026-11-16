# Investigación: mente artificial con memoria biológica y social

Este directorio responde una sola pregunta:

> ¿Qué mecanismos concretos de memoria y aprendizaje —de la neurología, la
> etología de mamíferos sociales, los insectos sociales y la sociología del
> conocimiento— se pueden implementar como algoritmos que resuelvan la amnesia
> de contexto, la interferencia entre dominios y la falta de progreso acumulado
> en agentes LLM?

No es un ensayo de divulgación. Es la base de evidencia para diseñar
`open-human-memory`: cada mecanismo que entre al diseño debe poder rastrearse
hasta un hallazgo de este directorio y sobrevivir a una ablación (si quitarlo no
empeora nada medible, no entra).

> **Aviso de estructura (2026-11-16).** Estos documentos son ahora **material de
> apoyo**, no la columna del proyecto. La columna es
> [`docs/teoria.md`](../../docs/teoria.md),
> [`docs/registro-de-afirmaciones.md`](../../docs/registro-de-afirmaciones.md) y
> [`precedentes/10-matriz-de-antecedentes.md`](precedentes/10-matriz-de-antecedentes.md).
> Si un documento de este directorio contradice el registro de afirmaciones, se
> corrige el documento. La razón está en
> [`docs/plan.md`](../../docs/plan.md): seis prototipos produjeron correcciones,
> no una teoría acumulativa.

## Método

1. **Fuentes primarias y reviews**, no blogs. Cuando un dato viene de una sola
   línea de investigación se marca como tal.
2. **Etiqueta de evidencia** en la síntesis:
   - `[A]` consenso científico o meta-análisis replicado.
   - `[B]` evidencia sólida pero con debate o límites de generalización.
   - `[C]` teoría o hipótesis prometedora, sin validación convergente.
3. **Traducción explícita**: mecanismo biológico → principio computacional →
   componente del sistema → cómo se mide.
4. **Anti-metáfora**: cada documento tiene una sección de "qué NO copiar". La
   biología inspira; no se idolatra.

## Mapa

| Documento | Pregunta que responde |
|---|---|
| [01-neurologia-de-la-memoria.md](01-neurologia-de-la-memoria.md) | ¿Cómo codifica, consolida, recupera y olvida el cerebro? |
| [02-aprendizaje-en-mamiferos.md](02-aprendizaje-en-mamiferos.md) | ¿Cómo aprenden y transmiten cultura primates, orcas y elefantes? |
| [03-organismos-sociales.md](03-organismos-sociales.md) | ¿Cómo coordina una colonia sin jefe? (hormigas, abejas) |
| [04-sociologia-y-memoria-colectiva.md](04-sociologia-y-memoria-colectiva.md) | ¿Cómo recuerda un grupo y quién sabe qué? |
| [05-aprendizaje-humano.md](05-aprendizaje-humano.md) | ¿Qué hace que el estudio se convierta en dominio duradero? |
| [06-estado-del-arte-computacional.md](06-estado-del-arte-computacional.md) | ¿Qué existe ya y dónde está el hueco real? |
| [07-sintesis-mecanismos-y-diseno.md](07-sintesis-mecanismos-y-diseno.md) | ¿Qué construimos y por qué? |
| [08-hipotesis-y-experimentos.md](08-hipotesis-y-experimentos.md) | ¿Cómo sabremos si funciona? |
| [09-weber-y-la-memoria-burocratica.md](09-weber-y-la-memoria-burocratica.md) | ¿Cómo se institucionaliza la memoria? (Weber) |
| [10-psicologia-de-la-memoria.md](10-psicologia-de-la-memoria.md) | ¿Cómo se distorsiona, interfiere y contagia la memoria? |
| [11-biologia-comparada-y-sociobiologia.md](11-biologia-comparada-y-sociobiologia.md) | ¿Cómo recuerdan y transmiten otros seres vivos? |
| [12-aprendizaje-humano-vs-maquinas.md](12-aprendizaje-humano-vs-maquinas.md) | ¿En qué se diferencian y qué se puede importar? |
| [13-paper-el-riesgo-del-olvido.md](13-paper-el-riesgo-del-olvido.md) | Documento de trabajo: la tesis completa |
| [14-referencias.md](14-referencias.md) | Bibliografía completa |
| [15-respuesta-directa.md](15-respuesta-directa.md) | Respuesta a la pregunta central + CUMULUS |
| [16-momento-cero-aprendizaje-humano.md](16-momento-cero-aprendizaje-humano.md) | ¿Cómo emular el aprendizaje humano para mejorar el primer intento? |
| [17-el-problema-del-contexto.md](17-el-problema-del-contexto.md) | Límites, causas y estrategias del contexto |
| [18-contexto-filosofia.md](18-contexto-filosofia.md) | ¿Qué es el contexto, filosóficamente? |
| [19-compactacion-aprendizaje-humano.md](19-compactacion-aprendizaje-humano.md) | ¿Existe la compactación en el aprendizaje humano? |
| [20-compactacion-y-sueno.md](20-compactacion-y-sueno.md) | ¿Es la compactación como el sueño? |
| [21-revision-critica-fuentes.md](21-revision-critica-fuentes.md) | Qué sostiene el diseño y qué es metáfora |
| [22-respuesta-a-revision.md](22-respuesta-a-revision.md) | Respuesta punto por punto a la revisión mayor |
| [23-marco-de-validez.md](23-marco-de-validez.md) | Fenómeno, traducción y ventaja comparativa |
| [24-programa-de-investigacion-v2.md](24-programa-de-investigacion-v2.md) | Horizontes, hipótesis y experimento diferencial A–E |
| [25-protocolo-fuentes-primarias.md](25-protocolo-fuentes-primarias.md) | Búsqueda reproducible y evaluación en dos ejes |
| [26-deepseek-y-atencion.md](26-deepseek-y-atencion.md) | Línea DeepSeek/atención y su impacto en memoria |
| [27-plan-de-implementacion.md](27-plan-de-implementacion.md) | Qué implementamos, qué no, y el MVP JANUS-C |
| [28-programa-de-competencia.md](28-programa-de-competencia.md) | Programa v3: continuidad, competencia y expansión |
| [29-experimento-diagnostico.md](29-experimento-diagnostico.md) | Experimento A–E y harness ejecutable |
| [prototipo-001-diagnostico/](prototipo-001-diagnostico/) | Smoke test histórico; invalidado por target leakage |
| [prototipo-002-diagnostico/](prototipo-002-diagnostico/) | Benchmark de solucionador; A0 == E sin historial |
| [prototipo-003-aprendizaje/](prototipo-003-aprendizaje/) | Registro exploratorio; su conclusión fue retirada por el 004 |
| [prototipo-004-validez/](prototipo-004-validez/) | Protocolo congelado; las macros no amplían capacidad |
| [prototipo-005-presupuesto/](prototipo-005-presupuesto/) | Continuidad, orden de búsqueda y acumulación en línea |
| [prototipo-006-politica/](prototipo-006-politica/) | Política de activación congelada: acierta, no paga el probe |
| [prototipo-006-agente-llm/](prototipo-006-agente-llm/) | Techo de un agente real: 46,9 % |
| [../../docs/revision-de-rumbo.md](../../docs/revision-de-rumbo.md) | Revisión de dirección y decisión del 007 |
| [revision-sistematica/](revision-sistematica/README.md) | Revisión ejecutada: 31 trabajos, búsquedas y extracción |
| [manuscrito.md](../../docs/manuscrito.md) | **Artículo completo para revisión por pares** |
| [registro-de-ejecuciones.md](../../docs/registro-de-ejecuciones.md) | Modelo, esfuerzo, semillas y comandos por experimento |
| [para-revisores.md](../../docs/para-revisores.md) | Mapa y preguntas para el revisor |
| [../../docs/problema-central.md](../../docs/problema-central.md) | Análisis previo: capacidades, confundidores y escalera |
| [../../docs/errata-006b.md](../../docs/errata-006b.md) | Errata del diagnóstico con LLM |
| [precedentes/](precedentes/) | Catálogo de lo ya intentado, incluidos competidores 2026 |
| [papers/](papers/) | CUMULUS (EN/ES) y JANUS (ES) v1.1; históricas en `archive/` |

## Estado

`v1.13` — corpus unificado. La columna del proyecto está fuera de este directorio:
`docs/teoria.md` (marco y predicciones), `docs/registro-de-afirmaciones.md`
(estado de cada afirmación) y `docs/plan.md` (rondas F0–F5). Aquí vive el material
de apoyo: 01–06 evidencia base; 07 síntesis; 08 protocolo v2.0; 09–12 amplían con
Weber, psicología, biología comparada y humano–máquina; 13 paper sobre el riesgo del
olvido; 14 bibliografía; 15 respuesta central; 16–20 momento cero, contexto,
filosofía, compactación y sueño; 21 auditoría de evidencia; 22 respuesta a la
primera revisión; 23 marco de validez; 24 programa v2 (histórico); 25 protocolo de
fuentes; 26 DeepSeek y atención; 27 plan JANUS-C; 28 programa de competencia v3; 29
experimento diagnóstico; `revision-sistematica/` es la revisión ejecutada (31
trabajos); `prototipo-001` smoke test invalidado; `prototipo-002` benchmark de
solucionador; `prototipo-003` registro exploratorio retirado; `prototipo-004`
validación con protocolo congelado; `prototipo-005` cuándo paga la memoria;
`prototipo-006-politica` política de activación; `prototipo-006-agente-llm` línea
base del agente; `src/ohmem/` implementa los seis; `precedentes/` cataloga lo
intentado; `papers/` contiene CUMULUS (EN/ES) y JANUS (ES) v1.1, con históricas en
`archive/`.

## La tesis en una frase

La memoria de un agente no debe ser un almacén que crece, sino un **ciclo de
vida** —codificar rápido, asociar, consolidar despacio, recuperar
reconsolidando, olvidar, y transmitir a otros— y ese ciclo solo se vuelve
"mente" cuando existe dentro de una **sociedad** con especialización, reputación
y dialectos compartidos.
