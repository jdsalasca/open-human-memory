# 03 — Contexto y aprendizaje continuo sin reentrenar

## Los límites del contexto

- **Lost in the Middle** (Liu et al., 2023): el rendimiento depende de la posición;
  la información en el medio se usa peor.
- **RULER** (Hsieh et al., 2024): la longitud efectiva es menor que la nominal;
  solo la mitad de los modelos evaluados mantiene rendimiento a 32K.
- **LongICLBench** (Li et al., 2024): el beneficio del contexto largo se estanca
  cerca de 20K tokens y la mayoría de los modelos cae después.

**Conclusión:** el problema del contexto no es de tamaño, es de **gestión**.

## Aprendizaje en contexto

- **Induction heads** (Olsson et al., 2022): circuitos que copian patrones y
  explican buena parte del ICL.
- **ICL como inferencia bayesiana** (Xie et al., 2022): el prompt identifica un
  concepto latente.
- **ICL como descenso de gradiente** (von Oswald et al., 2023): equivalencia en
  regímenes lineales; no es una teoría general.

**Conclusión:** el contexto es un mecanismo de aprendizaje temporal que se borra
al cerrar la ventana.

## Aprendizaje continuo sin tocar pesos

- **EWC** (Kirkpatrick et al., 2017): protege pesos importantes con la información
  de Fisher.
- **Replay** (Rolnick et al., 2019): mezcla datos viejos con nuevos.
- **Redes progresivas**: módulos nuevos por tarea.
- **Sleep-time compute** (Lin et al., 2025): cómputo offline para reorganizar
  memoria.

**Conclusión:** el aprendizaje continuo en pesos es caro y requiere datos; la
alternativa para agentes es externalizar el aprendizaje en artefactos.

## Context engineering y compactación

- **ACE** (Zhang, Q., et al., 2025): playbook que evoluciona.
- **MemGPT**: paginación.
- **Compaction**: resumen cuando el contexto se llena.

**Problema:** la compactación típica optimiza longitud, no utilidad. Puede
conservar la prosa y perder el procedimiento, el motivo y la procedencia. No hay
verificación de que lo compactado siga siendo ejecutable.

## Lo que falta

1. Una teoría de **qué información merece el presupuesto** (tasa–distorsión
   aplicada a la tarea).
2. Una **compactación verificable** que preserve procedimientos y excepciones.
3. Una **memoria externa** que no dependa de la ventana.
4. Una **evaluación longitudinal** que mida retención y transferencia, no solo
   recall.

## Precedentes que sí miden algo parecido

- **LoCoMo** (Maharana et al., 2024): conversaciones largas.
- **LongMemEval** (Wu et al., 2025): memoria a largo plazo en asistencia.
- **DMR**: recuperación profunda.
- **Holton et al. (2026)**: transferencia e interferencia en aprendizaje continuo,
  humanos vs. redes.

Ninguno mide meses de trabajo procedural con cambio de modelo. Ese es el hueco del
benchmark CUMULUS-Bench.
