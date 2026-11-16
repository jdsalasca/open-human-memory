# 08 — Hipótesis y experimentos

## 1. La pregunta falsable

> Un agente con el ciclo de vida de memoria propuesto repite menos errores,
> gasta menos contexto, transfiere mejor procedimientos y se contradice menos que
> el mismo agente con las estrategias actuales (contexto completo, resumen
> rodante, RAG vectorial), medido a lo largo de N sesiones sobre un proyecto que
> evoluciona.

Si la respuesta es no, el proyecto no tiene tesis. La arquitectura puede ser
elegante y aun así no servir.

## 2. Hipótesis

| # | Hipótesis | Métrica primaria | Dirección esperada |
|---|---|---|---|
| H1 | La consolidación con evidencia preserva decisiones y sus porqués mejor que el resumen rodante | Tasa de decisiones recuperadas correctamente a los K turnos | ↑ |
| H2 | La saliencia multidominio retiene lo crítico mejor que recencia + similitud | Retención de hechos críticos raros | ↑ |
| H3 | Las políticas por dominio reducen la interferencia entre campos | Precisión en consultas cruzadas | ↑ |
| H4 | Los playbooks con estadísticas mejoran la ejecución de tareas recurrentes | Tasa de éxito en tareas repetidas | ↑ |
| H5 | La enseñanza explícita acelera el arranque de un agente nuevo | Sesiones hasta paridad de desempeño | ↓ |
| H6 | El olvido selectivo mejora la precisión sin perder lo crítico | Precisión de recall; retención crítica | ↑ / = |
| H7 | El campo estigmérgico mejora la coordinación multi-agente | Tareas duplicadas; tiempo de convergencia | ↓ |
| H8 | Un régimen de validez explícito (tipo Weber) reduce la contaminación por rumores | % de recuerdos sin procedencia aceptados | ↓ |
| H9 | Las políticas por dominio gestionan el trade-off transferencia/interferencia mejor que un índice único | Transferencia e interferencia medidas juntas | ↑ / ↓ |

Hipótesis secundarias: menor tasa de contradicción (H10), menor costo por tarea
exitosa (H11), mejor calibración de confianza (H12).

## 3. Métricas operacionales

### 3.1 Continuidad de decisiones

- **Registro canónico**: cada decisión tiene `id`, texto, motivo, fecha, estado
  (`vigente`, `revocada`, `reemplazada_por`).
- **Acierto**: el agente cita la decisión vigente y su motivo cuando la tarea la
  toca.
- **Contradicción**: el agente propone algo incompatible con una decisión vigente
  sin señalarlo. Se mide por sesión y por 100 turnos.

### 3.2 Progreso en tareas

- **Tasa de éxito**: tarea completada y validada por test o por juez con rúbrica.
- **Reincidencia**: mismo error en dos sesiones separadas por ≥ 1 consolidación.
- **Tiempo hasta solución**: turnos y tokens.

### 3.3 Transferencia

- **Tarea de transferencia**: procedimiento aprendido en el dominio A, aplicado
  en B con distinto vocabulario y misma estructura profunda.
- **Métrica**: éxito sin contexto del dominio A, solo con el playbook.

### 3.4 Fidelidad de transmisión

- Agente maestro ejecuta un procedimiento; se destila; agente alumno lo ejecuta.
- **Fidelidad** = pasos correctos / pasos totales, y resultado final comparable.
- Un `summary` libre es la línea base de baja fidelidad.

### 3.5 Economía de contexto

- Tokens de entrada por tarea exitosa.
- Tokens de consolidación por sesión.
- Costo total por punto de éxito.

### 3.6 Olvido

- **Retención crítica**: % de hechos raros y críticos (decisiones, restricciones,
  incidentes) recuperables tras K sesiones.
- **Precisión**: % de recuerdos devueltos que son pertinentes.
- **Basura**: % de tokens de contexto ocupados por recuerdos obsoletos.

## 4. Diseño experimental

### 4.1 Proyecto longitudinal sintético

Un proyecto ficticio con:

- 40–60 sesiones de trabajo.
- Requisitos que cambian (decisiones revocadas y reemplazadas).
- Tareas recurrentes (misma clase de bug, mismo tipo de migración).
- Hechos raros pero críticos sembrados (una restricción que solo aparece una vez).
- Ruido: conversaciones irrelevantes, intentos fallidos.
- Preguntas de control en cada sesión sobre decisiones y procedimientos previos.

Ventaja: control y repetibilidad. Desventaja: puede no capturar la complejidad
real. Por eso se complementa con dogfooding.

### 4.2 Dogfooding

El propio desarrollo de `open-human-memory` como proyecto longitudinal real: cada
sesión de agente usa el sistema y se registran las métricas. Es el experimento
ecológicamente válido, con la desventaja de que no hay grupo de control limpio.

### 4.3 Condiciones

| Condición | Descripción |
|---|---|
| C0 | Contexto completo hasta el límite (techo de información, costo alto) |
| C1 | Resumen rodante (compactación típica) |
| C2 | RAG vectorial + recencia |
| C3 | Sistema propuesto sin capa social (A–D) |
| C4 | Sistema propuesto completo (A–E) |

### 4.4 Ablaciones

Por cada módulo (saliencia, quórum, esquemas, playbooks, olvido, directorio,
estigmergia), una corrida sin él. Si la diferencia no es significativa, el módulo
no justifica su complejidad.

### 4.5 Unidad de análisis y estadística

- Unidad: tarea dentro de sesión, agrupada por sesión.
- Comparaciones pareadas por tarea (misma tarea, distintas condiciones).
- Intervalos de confianza por bootstrap; reportar tamaño de efecto, no solo
  p-valor.
- Pre-registrar las métricas primarias antes de correr; las secundarias son
  exploratorias.

## 5. Protocolo mínimo viable (1 semana)

1. **Día 1**: implementar el harness y las condiciones C0–C2 (sin sistema nuevo).
2. **Día 2**: correr línea base sobre el proyecto sintético (10 sesiones).
3. **Día 3–4**: implementar A–D mínimo (encode, recall, consolidación básica,
   playbooks).
4. **Día 5**: correr C3 y ablaciones.
5. **Día 6**: analizar; decidir qué módulos sobreviven.
6. **Día 7**: escribir resultados y ajustar el diseño.

Si el harness no está listo, no se escribe código de producción. La medición
manda.

## 6. Criterios de éxito y de muerte

**Éxito mínimo**: C3 supera a C1 en al menos 2 de 4 métricas primarias
(decisiones, éxito, transferencia, contradicción) con efecto ≥ 10% relativo.

**Éxito fuerte**: C4 supera a C3 en al menos 1 métrica social (fidelidad,
arranque, duplicación).

**Muerte**: tras 30 sesiones, C3 no supera a C1 en ninguna métrica primaria. En
ese caso, el ciclo de vida no aporta y hay que reducirlo o abandonarlo.

## 7. Amenazas a la validez

- **No determinismo del LLM**: misma entrada, distinta salida. Mitigación:
  semillas cuando sea posible, múltiples corridas, comparación pareada.
- **Sesgo del juez**: si un LLM evalúa, puede favorecer respuestas largas o
  familiares. Mitigación: rúbrica, doble juez, acuerdo inter-juez.
- **Contaminación**: el modelo pudo ver el benchmark. Mitigación: proyecto
  sintético propio y no publicado.
- **Confusión por costo**: C3 puede ganar porque gasta más cómputo. Mitigación:
  reportar costo por punto de éxito, no solo calidad.
- **Novedad**: el sistema nuevo puede ganar por atención del investigador.
  Mitigación: mismo esfuerzo de ingeniería en las líneas base.
- **Deriva de versión**: cambio de modelo entre corridas. Mitigación: fijar
  versión y registrar hash.

## 8. Lo que este experimento no responde

- Si el sistema es "consciente" o "humano". No es una pregunta empírica de
  ingeniería.
- Si escala a miles de agentes. El experimento es de un usuario y un pod.
- Si funciona en dominios muy técnicos sin datos suficientes. Se necesitan
  réplicas por dominio.

## 9. Próximo paso

Convertir H1–H7 en un harness ejecutable antes de escribir el núcleo. El orden
correcto es: medir → diseñar → implementar → medir. No al revés.
