# 15 — Respuesta directa: ¿puede un agente acumular procedimientos durante meses y transferirlos entre modelos?

## La pregunta

> ¿Puede un agente desarrollar conocimiento procedimental acumulativo durante
> meses, transferible entre modelos distintos, de forma que su rendimiento
> mejore sin necesidad de volver a entrenar el LLM?

## La respuesta corta

**Sí, y en 2026 ya hay evidencia parcial — pero no de la duración ni de la
validez causal que la pregunta exige.**

- **Zep Agent Skills** (Chalef et al., 2026) compila trazas verificadas en skills
  versionadas y mejora a modelos más débiles con las skills de uno más fuerte.
- **MSCE** (Tang et al., 2026) convierte experiencia en políticas y skills con
  evidencia, límites y verificación; reporta transferencia cross-domain.
- **Trace2Skill** (Ni et al., 2026) destila trayectorias en skills que transfieren
  entre escalas y familias de modelos.
- **AFTER** (Belikova et al., 2026) mide transferencia de skills entre tareas,
  roles y backbones.

Lo que **no** está demostrado:

1. que la mejora dure **meses** con deriva real de modelos, APIs y requisitos;
2. que las habilidades promovidas sean **causales** y no correlaciones afortunadas;
3. que la selección funcione cuando la biblioteca crece (Jiang et al., 2026);
4. que la gobernanza social supere a un verificador único con igual presupuesto.

## Lo que la evidencia sostiene

- El aprendizaje sin actualizar pesos existe en formas parciales: memoria de
  casos (Memento), playbooks (ACE), bibliotecas de habilidades (Voyager,
  SkillWeaver, AWM, Zep Agent Skills, MSCE), reflexión (Reflexion).
- La neurología sostiene que consolidación y olvido son procesos selectivos
  (CLS, replay, olvido adaptativo), no simple almacenamiento.
- La biología social sostiene que la transmisión de alta fidelidad hace
  acumulativa la cultura (orcas, primates, córvidos).
- La sociología aporta el expediente y la gobernanza (Weber, memoria transactiva,
  Ostrom), pero **legitimidad no es verdad**.
- La comparación humano–máquina muestra un trade-off compartido entre
  transferencia e interferencia (Holton et al., 2026).

## La hipótesis revisada

**H1 (portabilidad acumulativa):** con pesos congelados, una capa de artefactos
procedimentales agnósticos al modelo, compilados desde trazas verificadas y
validados por ejecución ciega entre modelos, produce mejora acumulativa en
familias de tareas recurrentes y transferencia positiva a modelos no vistos,
**frente a un repositorio simple de Markdown + tests + recuperador y frente a los
sistemas de 2026, con presupuesto igualado**.

Subhipótesis: acumulación, transferencia, retención tras reinicio/cambio,
atribución artefactual, compilación vs. resumen, auditoría ciega vs.
auto-revisión, artefactos tipados vs. chat libre.

**H2 (JANUS):** sin contrafactuales, los sistemas confunden éxito con causalidad;
una memoria que registra alternativas y aplica una puerta causal reduce las
skills espurias.

## La arquitectura, corregida

**CUMULUS v0.2** (Traza → Forja → Canon → Pod → Puente):

1. **Traza**: log inmutable con procedencia y saliencia.
2. **Forja**: cribado causal —segmenta, abstrae, prueba necesidad local, detecta
   redundancias e interacciones— y **se abstiene** si la cobertura es baja.
3. **Canon**: biblioteca versionada con matriz de portabilidad, dueño, caducidad
   y contradicciones.
4. **Pod**: roles con artefactos tipados, auditoría ciega y disenso; el quórum es
   coordinación, no verdad.
5. **Puente**: renderizadores por modelo, adaptadores, conformidad y deriva.

**JANUS** añade el ledger de decisiones, los contrafactuales y la puerta de
promoción causal.

## Cómo se falsa

Protocolo `08-hipotesis-y-experimentos.md` v2.0:

- métrica primaria: éxito en instancias reservadas de familias recurrentes;
- presupuesto igualado; rival simple C3;
- competidores: Zep Agent Skills, MSCE, Trace2Skill;
- 8 ciclos con deriva programada; holdouts ocultos;
- potencia calculada con piloto; multiplicidad controlada; jueces
  independientes.

**Criterio de muerte:** si CUMULUS no supera al rival simple en la métrica
primaria con IC 95% que excluya cero, la arquitectura no aporta.

## Lo que no promete

- Conciencia, emoción o inteligencia general.
- Crear competencia que el modelo no tiene.
- Transferencia universal: algunas habilidades serán específicas del modelo.
- Eliminar la interferencia: solo gestionarla por dominio.
- Que la capa social mejore por sí sola: es una hipótesis con confusor de
  cómputo.

## Documentos

- Revisión y alcance corregido: [`papers/cumulus-revision-v0.2.md`](papers/cumulus-revision-v0.2.md)
- Respuesta a la revisión: [`22-respuesta-a-revision.md`](22-respuesta-a-revision.md)
- Marco de validez: [`23-marco-de-validez.md`](23-marco-de-validez.md)
- Competidores 2026: [`precedentes/06-competidores-directos-2026.md`](precedentes/06-competidores-directos-2026.md)
- Protocolo experimental: [`08-hipotesis-y-experimentos.md`](08-hipotesis-y-experimentos.md)
- JANUS: [`papers/janus-es.md`](papers/janus-es.md)
