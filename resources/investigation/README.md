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

## Estado

`v0.2` — revisión ampliada. Los documentos 01–06 son la evidencia base; 07 es la
síntesis que alimenta el diseño; 08 define el benchmark longitudinal; 09–12
amplían con Weber, psicología, biología comparada y la comparación humano–máquina;
13 es el documento de trabajo que integra la tesis; 14 es la bibliografía.

## La tesis en una frase

La memoria de un agente no debe ser un almacén que crece, sino un **ciclo de
vida** —codificar rápido, asociar, consolidar despacio, recuperar
reconsolidando, olvidar, y transmitir a otros— y ese ciclo solo se vuelve
"mente" cuando existe dentro de una **sociedad** con especialización, reputación
y dialectos compartidos.
