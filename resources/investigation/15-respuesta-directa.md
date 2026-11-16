# 15 — Respuesta directa: ¿puede un agente acumular procedimientos durante meses y transferirlos entre modelos?

## La pregunta

> ¿Puede un agente desarrollar conocimiento procedimental acumulativo durante
> meses, transferible entre modelos distintos, de forma que su rendimiento
> mejore sin necesidad de volver a entrenar el LLM?

## La respuesta corta

**Sí, en principio — pero no con los sistemas actuales.** La evidencia no
permite afirmar que ya ocurra; permite afirmar que es viable si se cumplen tres
condiciones que hoy no se cumplen:

1. **Representación portable.** El procedimiento debe ser un artefacto
   ejecutable agnóstico al modelo, no un prompt, un resumen o una transcripción.
2. **Compilación verificada.** Debe construirse desde trazas por ablación causal
   y con postcondiciones ejecutables, no por resumen.
3. **Gobernanza social.** Debe promoverse con verificación ciega entre modelos,
   quórum, procedencia, decaimiento y revisión.

## Por qué la respuesta no es un "no"

- El aprendizaje continuo sin actualizar pesos ya existe en formas parciales:
  memoria de casos (Memento), playbooks evolutivos (ACE), bibliotecas de
  habilidades (Voyager, SkillWeaver, AWM), reflexión verbal (Reflexion).
- La neurología muestra que la consolidación y el olvido son procesos
  seleccionables, no un simple almacenamiento (CLS, replay, olvido adaptativo).
- La biología social muestra que la transmisión de alta fidelidad es lo que hace
  acumulativa la cultura (orcas, primates, córvidos).
- La sociología muestra que la memoria necesita instituciones: expediente,
  jurisdicción, legitimidad y gobernanza (Weber; memoria transactiva; Ostrom).
- La comparación humano–máquina muestra que el trade-off
  transferencia/interferencia es compartido (Holton et al., 2026), así que la
  meta no es eliminarlo sino gestionarlo.

## Por qué la respuesta no es un "sí" trivial

- Sin actualizar pesos, el techo es la competencia latente del modelo. La memoria
  organiza y amplifica; no crea capacidad inexistente.
- La transferencia entre modelos no es automática: sintaxis, política y
  competencia cambian. Hay que medirla, no suponerla.
- Los benchmarks actuales miden recall, no acumulación procedural longitudinal.
- Sin verificación, el sistema acumula errores con la misma eficiencia con que
  acumula aciertos.

## La hipótesis

**Hipótesis de portabilidad acumulativa (H1):** con pesos congelados, una capa
de artefactos procedimentales agnósticos al modelo, compilados desde trazas
verificadas y validados por ejecución ciega entre modelos, produce mejora
acumulativa positiva en familias de tareas recurrentes y verificables, y
transferencia positiva a modelos no vistos.

Subhipótesis medibles: acumulación (H1a), transferencia (H1b), retención tras
reinicio/cambio (H1c), atribución artefactual (H1d), superioridad de la
compilación sobre el resumen (H1e), reducción de contaminación por auditoría
ciega (H1f) y superioridad de los artefactos tipados sobre el chat libre (H1g).

## La arquitectura en una página

**CUMULUS** (Trace → Forge → Canon → Pod → Bridge):

1. **Traza**: log inmutable de episodios con procedencia y saliencia.
2. **Forja**: compila trazas en habilidades SIR mediante segmentación,
   abstracción, ablación causal, inferencia de precondiciones/postcondiciones y
   pruebas.
3. **Canon**: biblioteca versionada de habilidades validadas, con matriz de
   portabilidad, dueño, caducidad y contradicciones preservadas.
4. **Pod**: roles (explorador, herrero, auditor, curador, historiador, crítico)
   que intercambian artefactos tipados; auditoría ciega, quórum y registro de
   disenso.
5. **Puente**: renderizadores por modelo, adaptadores de capacidades, suite de
   conformidad, score de portabilidad y detección de deriva.

La clave: **lo que la habilidad significa** (SIR) se separa de **cómo un modelo
lo dice** (renderizador). Así el procedimiento sobrevive al cambio de modelo.

## Cómo se falsa

El benchmark longitudinal CUMULUS-Bench (5 dominios, 10 familias por dominio, 3
familias de modelos, 6 ciclos, verificadores ejecutables, holdouts ocultos)
compara CUMULUS contra zero-shot, RAG, Reflexion, Voyager, ACE y Memento.

Criterio de muerte: si tras 6 ciclos CUMULUS no supera a la mejor línea base en
≥10% relativo en al menos 2 de 4 métricas primarias (éxito, retención,
transferencia, costo), o no alcanza un coeficiente de transferencia ≥0,5 para la
mitad de las canónicas, la hipótesis falla para este diseño.

## Lo que no promete

- Conciencia, emoción o inteligencia general.
- Crear competencia que el modelo no tiene.
- Transferencia universal: algunas habilidades serán específicas del modelo y
  deben reportarse como tales.
- Eliminar la interferencia: solo gestionarla por dominio.

## Documentos

- Paper en inglés: [`papers/cumulus-en.md`](papers/cumulus-en.md)
- Paper en español: [`papers/cumulus-es.md`](papers/cumulus-es.md)
- Síntesis de evidencia: [`07-sintesis-mecanismos-y-diseno.md`](07-sintesis-mecanismos-y-diseno.md)
- Hipótesis y experimentos: [`08-hipotesis-y-experimentos.md`](08-hipotesis-y-experimentos.md)
- Comparación humano–máquina: [`12-aprendizaje-humano-vs-maquinas.md`](12-aprendizaje-humano-vs-maquinas.md)
