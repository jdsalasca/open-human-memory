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
| [precedentes/](precedentes/) | Catálogo de lo ya intentado, incluidos competidores 2026 |
| [papers/](papers/) | CUMULUS final (EN/ES) y JANUS final (ES) |

## Estado

`v0.9` — plan de implementación. Los documentos 01–06 son la evidencia base; 07
es la síntesis; 08 es el protocolo v2.0; 09–12 amplían con Weber, psicología,
biología comparada y humano–máquina; 13 es el paper sobre el riesgo del olvido;
14 es la bibliografía; 15 responde la pregunta central; 16–20 desarrollan momento
cero, contexto, filosofía, compactación y sueño; 21 audita la evidencia en dos
ejes; 22 responde a la primera revisión; 23 fija el marco de validez; 24 es el
programa v2; 25 es el protocolo de fuentes; 26 integra DeepSeek y atención; 27 es
el plan de implementación de JANUS-C; `precedentes/` cataloga lo ya intentado;
`papers/` contiene las versiones finales de CUMULUS (EN/ES) y JANUS (ES).

## La tesis en una frase

La memoria de un agente no debe ser un almacén que crece, sino un **ciclo de
vida** —codificar rápido, asociar, consolidar despacio, recuperar
reconsolidando, olvidar, y transmitir a otros— y ese ciclo solo se vuelve
"mente" cuando existe dentro de una **sociedad** con especialización, reputación
y dialectos compartidos.
