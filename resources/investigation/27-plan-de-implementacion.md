# 27 — Plan de implementación: qué construimos, qué no, y por qué

> **Actualizado por `29-experimento-diagnostico.md` y `src/ohmem/`.** El primer
> paso ya no es JANUS-C completo, sino el diagnóstico A–E. JANUS-C se implementa
> solo si el diagnóstico muestra que la selección/verificación es el cuello.

## 1. Respuesta corta

**No vamos a implementar COUNTERMEM como producto.** Vamos a implementar un
**controlador de decisiones epistémicas** sobre memoria contrafactual, con tres
certificados y abstención. COUNTERMEM será una **línea base replicada**, no el
sistema.

Nombre de trabajo: **JANUS-C** (Certificate-gated Counterfactual Memory).

## 2. Por qué no clonar COUNTERMEM

COUNTERMEM (Pu, Tang y Zhang, 2026) ya hace:

- alternativas locales desde un estado reseteado;
- verificación con world models ejecutables (tests, proof checkers, SQL, solvers);
- condiciones de aplicabilidad;
- selector DQN para usar o saltar;
- 12 benchmarks, +12,6 pp promedio.

Clonarlo sería replicación, no contribución. Además tiene tres supuestos
verificables que fallan en entornos reales:

1. **El estado se puede resetear fielmente.**
   Pakhomov y Nijkamp (2026) muestran snapshots con el mismo hash que difieren de
   la continuación viva en 9 y 20 de 24 estados. Peimani (2026) muestra replay
   visible que coincide en 20/20 ramas pero recupera el efecto equivocado en 3.
2. **La corrección verificada es aplicable fuera de la tarea fuente.**
   El propio COUNTERMEM reporta 11,8% de daño en tareas parecidas; sin condición
   de aplicabilidad, 34,2%.
3. **El presupuesto de verificación se puede gastar en todos los fallos.**
   En entornos abiertos, verificar cada fallo es caro; no todos los fallos
   merecen un contrafactual.

## 3. El problema verificable

> **Los sistemas de memoria contrafactual tratan "verificado en un reset" como
> "válido y aplicable", sin certificar la restauración, sin calibrar la
> aplicabilidad y sin asignar el presupuesto de verificación por valor de
> información.**

Consecuencias medibles:

- **Efecto equivocado:** una corrección parece funcionar por una restauración
  incompleta.
- **Reutilización dañina:** la corrección se aplica en un contexto parecido pero
  no equivalente.
- **Gasto inútil:** se verifican fallos de bajo impacto y se dejan sin verificar
  los de alto impacto.

## 4. La propuesta: JANUS-C

Tres puertas antes de promover una corrección contrafactual:

### 4.1 Certificado de restauración

Antes de aceptar un contrafactual, medir:

- acuerdo entre la rama restaurada y una continuación de referencia;
- estado del proceso (flujo aleatorio, cachés, handles);
- condiciones del estimando: replay exacto o igualdad distribucional;
- umbral pre-registrado.

Si no pasa, el contrafactual se guarda como **hipótesis**, no como corrección.

### 4.2 Certificado de aplicabilidad

En lugar de una condición generada por el LLM y verificada solo
estructuralmente:

- estimar utilidad marginal con pares WITH/WITHOUT en estados comparables
  (inspirado en SkillApt);
- calibrar a nivel de **trayectoria**, no de paso: la calibración por paso no
  transfiere (Li et al., 2026);
- emitir `load`, `abstain` o `conditional`;
- modelar costo y riesgo.

Si la calibración no alcanza el umbral, el sistema se abstiene.

### 4.3 Programador por valor de la información

No verificar todos los fallos. Elegir el siguiente contrafactual por:

\[
\text{VOI} = P(\text{cambiar decisi\'on}) \times \text{impacto} - \text{costo}
\]

con restricciones de reversibilidad y seguridad. Los fallos de alto impacto y
baja confianza se verifican primero; los triviales se archivan.

### 4.4 Abstención

El sistema puede responder:

> "No hay evidencia suficiente para determinar qué acción causó el resultado."

y guardar una **pregunta abierta** con experimento pendiente.

## 5. Qué innovamos (y qué no)

**No es nuevo:**

- memoria contrafactual verificada (COUNTERMEM);
- admisión contrafactual (ConMem);
- control de memoria (MemCon);
- load vs abstain por utilidad marginal (SkillApt);
- límites de aplicabilidad (BASM);
- calibración de uso de memoria (MemCalib);
- confianza en memoria por pruebas diseñadas (MemTrial);
- selección causal de memoria (CMI);
- certificados de replay (Pakhomov y Nijkamp; Peimani);
- familias de reparación mínima (GCJR);
- anti-persistencia (More Memory, Worse Agents);
- retención vs consolidación por presupuesto (OAS).

**Posible contribución (a probar):**

1. **Integrar las tres puertas** —restauración, aplicabilidad, VOI— en un solo
   controlador que decide entre `retain`, `reconstruct`, `promote`,
   `investigate` y `abstain`.
2. **Certificado por objeto de memoria**, no solo por pipeline: cada corrección
   declara qué se estimó, con qué restauración y qué aplicabilidad.
3. **Calibración a nivel de trayectoria** para decidir promoción, no solo
   precisión por paso.
4. **Presupuesto de verificación por VOI**, en lugar de verificación uniforme.
5. **Evaluación longitudinal con deriva** y tres regímenes de restauración
   (completa, parcial, solo visible), que ningún benchmark actual combina.

Es una contribución de **integración y política**, no de almacenamiento. Si no
supera a las piezas por separado, no existe.

## 6. MVP: qué se construye exactamente

### 6.1 Módulos

| Módulo | Función | Salida |
|---|---|---|
| `ledger` | Registra decisiones, propensiones, estado, resultado | JSONL inmutable |
| `restore` | Snapshot/reset y certificado de replay | `restore_certificate` |
| `counterfactual` | Genera alternativas locales y las evalúa | `cf_record` |
| `applicability` | Calibra utilidad marginal y abstención | `load/abstain/conditional` |
| `voi` | Prioriza qué verificar | ranking de fallos |
| `promote` | Decide Canon vs hipótesis vs archivo | `promotion_decision` |
| `sandbox` | Entornos con verdad causal y 3 regímenes de restauración | episodios |

### 6.2 Esquema mínimo

```yaml
decision:
  id: dr_...
  state_hash: ...
  observable: [...]
  hidden_assumptions: [...]
  propensity: {a: 0.7, a1: 0.2, a2: 0.1}
  chosen: a
  alternatives: [a1, a2]
  outcome: {y, verifier}

counterfactual:
  id: cf_...
  decision: dr_...
  alternative: a1
  estimate: y1
  evidence_type: randomized | natural | simulation | model
  restore_certificate: {agreement: 0.98, regime: full, passed: true}
  applicability: {p_help: 0.72, p_harm: 0.08, calibrator: trajectory}
  status: verified | hypothesis | rejected

promotion:
  skill: sk_...
  decision: promote | abstain | reconstruct
  reasons: [...]
```

### 6.3 Sandbox

Tres entornos con verdad causal conocida:

- **Reset completo:** el estado se restaura y el certificado pasa.
- **Reset parcial:** se restaura lo visible, pero el proceso/aleatorio no.
- **Sin reset:** solo se pueden usar experimentos naturales y logs.

Tres distribuciones de aplicación:

- **En distribución:** la corrección aplica.
- **Look-alike:** superficie parecida, condición distinta.
- **Deriva:** cambia el modelo, la API o el requisito.

### 6.4 Baselines

- Sin memoria.
- Trazas + recuperación.
- COUNTERMEM-style (reset + alternativas + selector).
- SkillApt-style (load/abstain por utilidad marginal).
- MemTrial-style (trust test).
- OAS-style (retain vs consolidate por presupuesto).
- Markdown + tests + recuperador (rival simple).

### 6.5 Métricas

Primarias:

- **tasa de efecto equivocado** (corrección promovida que no reproduce el efecto);
- **reutilización dañina** en look-alike;
- **éxito ajustado por costo**;
- **calibración** (ECE/Brier de aplicabilidad).

Secundarias:

- costo por éxito; llamadas de verificación; abstención correcta; tiempo a
  corrección; transferencia entre modelos.

### 6.6 Criterio de muerte

Si JANUS-C no reduce la tasa de efecto equivocado o la reutilización dañina
frente a COUNTERMEM-style con el mismo presupuesto, no se justifica. Si
SkillApt-style o MemTrial-style igualan el resultado, se adopta la pieza más
simple.

## 7. Fases

### Fase 0 — Replicación (1 semana)

- Sandbox de juguete con verdad causal.
- COUNTERMEM-style mínimo.
- Certificado de restauración.
- **Producto:** línea base reproducible.

### Fase 1 — Certificados (1–2 semanas)

- `restore_certificate` con régimen completo/parcial/visible.
- Medir efecto equivocado.
- **Producto:** evidencia de que la restauración importa.

### Fase 2 — Aplicabilidad calibrada (1–2 semanas)

- Pares WITH/WITHOUT.
- Calibración por trayectoria.
- `load/abstain/conditional`.
- **Producto:** reducción de daño en look-alike.

### Fase 3 — VOI (1 semana)

- Priorización por impacto × incertidumbre / costo.
- **Producto:** mismo éxito con menos verificaciones.

### Fase 4 — Longitudinal (2 semanas)

- Deriva de modelo/API/requisito.
- Anti-persistencia.
- **Producto:** curva de errores persistentes.

## 8. Lo que no se implementa todavía

- La arquitectura CUMULUS completa (Pod, Canon, Puente).
- La política GRPO de uso de memoria.
- El ledger de ignorancia completo.
- Multiagente real.
- Un servidor MCP.

Primero se demuestra la política; después se empaqueta.

## 9. Riesgos

- **La restauración perfecta puede ser imposible** en entornos hosted; el
  certificado distribucional puede ser costoso.
- **La calibración por trayectoria** requiere muchas muestras.
- **El VOI** puede ser tan caro de estimar como verificar.
- **El sandbox** puede no representar entornos reales.
- **La integración** puede no superar a las piezas por separado.

## 10. La innovación, en una frase

> No construir otra memoria, sino un **controlador que decide qué hacer con la
> evidencia contrafactual**: certificarla, calibrarla, priorizarla o abstenerse.

Eso es lo que vamos a implementar. Si funciona, se conecta a CUMULUS para la
portabilidad y a ESCM para la incertidumbre. Si no, se descarta sin haber
construido un castillo.
