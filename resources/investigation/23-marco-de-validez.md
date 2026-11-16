# 23 — Marco de validez: fenómeno, traducción y ventaja comparativa

## 1. Por qué hace falta

La revisión externa señaló el problema central: la investigación reunía evidencia
de que un fenómeno existe (el sueño consolida, las hormigas usan quórum, los
humanos practican recuperación) y de ahí saltaba a un mecanismo computacional y a
una afirmación de mejora. Ese salto no es válido por sí mismo.

Este documento separa tres niveles y define qué evidencia exige cada uno.

## 2. Los tres niveles

### L1 — Fenómeno

**Pregunta:** ¿el fenómeno existe y está bien establecido en su disciplina?

**Evidencia:** estudios primarios, meta-análisis, revisiones sistemáticas.

**Lo que autoriza:** usar el fenómeno como inspiración y como restricción de
diseño. Nada más.

**Fallo típico:** citar un mecanismo biológico como si probara una arquitectura.

### L2 — Traducción funcional

**Pregunta:** ¿existe un mecanismo computacional que cumpla una función análoga,
sin requerir el sustrato biológico?

**Evidencia:** especificación formal, prototipo, prueba de concepto, ablación
interna.

**Lo que autoriza:** decir "esto es un análogo funcional de X", no "esto mejora
el rendimiento porque X".

**Fallo típico:** llamar "hipocampo" a un índice vectorial y creer que hereda sus
propiedades.

### L3 — Ventaja comparativa

**Pregunta:** ¿el mecanismo supera a alternativas más simples en agentes LLM, con
presupuesto y evaluación comparables?

**Evidencia:** experimento controlado, ablación, línea base fuerte, intervalos de
confianza, réplica.

**Lo que autoriza:** afirmar una contribución.

**Fallo típico:** comparar contra "sin memoria" en vez de contra un repositorio de
Markdown, tests y un recuperador.

### Tabla de niveles

| Nivel | Se prueba con | No se prueba con | Salida |
|---|---|---|---|
| L1 fenómeno | Neurociencia, etología, sociología, psicología | Analogía, intuición | Inspiración y restricción |
| L2 traducción | Especificación + prototipo + ablación interna | Éxito de un caso | Análogo funcional |
| L3 ventaja | Experimento comparativo con líneas base | Revisión bibliográfica | Contribución |

**Regla:** ninguna afirmación de CUMULUS o JANUS puede subir de nivel sin la
evidencia del nivel correspondiente.

## 3. Ontología de la evidencia

Una traza no es conocimiento. Para que el sistema no confunda registro con
verdad, cada objeto debe tener un tipo explícito:

| Tipo | Definición | Tratamiento |
|---|---|---|
| **Observación** | Evento registrado por una fuente | Conservar con procedencia; no es verdad |
| **Afirmación** | Lo que un agente sostiene | No asumir; requiere evidencia |
| **Evidencia** | Información que respalda o refuta una afirmación | Evaluar calidad, alcance e independencia |
| **Inferencia** | Conclusión derivada de evidencia | Registrar supuestos y método |
| **Hipótesis** | Explicación provisional | Someter a prueba; no promover |
| **Conocimiento validado** | Resultado corroborado bajo condiciones explícitas | Reutilización controlada |

### Esquema mínimo

```yaml
object:
  id: ...
  type: observation | claim | evidence | inference | hypothesis | validated
  content: ...
  source: {agent, model, tool, human}
  method: {how it was obtained}
  scope: {domain, conditions}
  confidence: ...
  supports: [ids]
  contradicts: [ids]
  status: active | archived | revoked
```

**Regla de oro:** una afirmación sin evidencia es una hipótesis; una inferencia
sin supuestos declarados es una opinión; una observación sin procedencia es un
rumor.

## 4. Teoría del error

Un sistema de memoria que aprende de trazas debe modelar cómo se equivoca.

### 4.1 Falsos positivos de verificación

Un test pasa y el requisito no se cumple. Causas: tests incompletos, criterios
mal especificados, comportamiento no determinista, entorno distinto.

**Mitigación:** múltiples verificadores, holdouts ocultos, tests adversariales,
revisión humana por muestreo.

### 4.2 Trazas incompletas

La traza no registra una condición externa, un cambio de estado o una decisión
implícita. La Forja infiere una causa que no está.

**Mitigación:** registrar estado del entorno, versiones, permisos y supuestos;
marcar campos faltantes; abstenerse si la cobertura es baja.

### 4.3 Verificadores defectuosos

El verificador tiene un bug o está sesgado. El sistema aprende a satisfacer el
verificador, no el objetivo.

**Mitigación:** verificación independiente, auditoría del verificador, tests de
mutación, comparación con jueces humanos.

### 4.4 Contaminación por interpretaciones previas

El agente resume su propia interpretación y luego la trata como observación. Es
el equivalente artificial de la reconsolidación distorsionada.

**Mitigación:** separar fuente de interpretación; no reescribir observaciones;
versionar.

### 4.5 Evaluadores correlacionados

Cinco agentes con el mismo modelo, el mismo prompt y los mismos datos no son
cinco fuentes independientes. El quórum mide acuerdo, no verdad.

**Mitigación:** modelar la correlación; usar modelos y herramientas distintas;
medir diversidad de evidencia; preferir verificación ejecutable.

### 4.6 Sesgo de supervivencia

Solo se guardan los éxitos; los fracasos no dejan traza. El sistema aprende una
distribución sesgada.

**Mitigación:** registrar fracasos y casi-fallos; muestrear intentos fallidos;
usar trayectorias de error como señal (Trace2Skill).

### 4.7 Goodhart

La métrica se convierte en objetivo. El agente optimiza el test, no la tarea.

**Mitigación:** métricas múltiples, holdouts, evaluación diferida, auditoría
humana.

## 5. Identificación causal: por qué la ablación simple no basta

### 5.1 El problema

La Forja de CUMULUS eliminaba un paso y volvía a ejecutar la postcondición para
encontrar el "núcleo causal". Eso es un test de necesidad local, no una
estimación del efecto causal.

### 5.2 Redundancia

Si A y B producen el mismo resultado de forma independiente:

- quitar A: el sistema funciona por B;
- quitar B: funciona por A;
- concluir "ninguno es necesario" es falso para el resultado, pero correcto para
  la necesidad individual. La conclusión depende de la pregunta.

### 5.3 Interacción

Si A y B solo funcionan juntos:

- quitar A rompe el resultado;
- quitar B lo rompe;
- ninguno es suficiente por separado; la causa es la conjunción.

### 5.4 Estado no restaurado

Repetir una ejecución no garantiza el mismo entorno. Archivos, cachés, permisos,
dependencias y no determinismo cambian. Sin aislamiento y restauración, la
ablación mide otra cosa.

### 5.5 Confusión

El éxito puede deberse a una variable no registrada (hora, carga, versión de una
dependencia). Sin diseño, la correlación se confunde con causa.

### 5.6 Lo que se necesita

- **Resultados potenciales:** \(Y(a)\) para cada acción \(a\).
- **Intervención:** \(do(a)\), no observación condicional.
- **Supuestos de identificación:** ignorabilidad, positividad, consistencia.
- **Diseño:** aleatorización cuando sea posible; experimentos naturales con
  matching; simulación con supuestos explícitos.
- **Transporte:** probar el efecto en otro dominio/modelo (Bareinboim y Pearl).
- **Abstención:** si no se puede identificar, no promover; guardar como
  correlación.

### 5.7 Jerarquía de evidencia

1. Experimento aleatorio.
2. Experimento natural con covariates comparables.
3. Simulación con modelo validado.
4. Juicio del modelo.

Una habilidad no se promueve con nivel 4 si hay niveles 1–2 disponibles. Si solo
hay nivel 4, se guarda como hipótesis, no como conocimiento validado.

## 6. Consecuencias para la arquitectura

### CUMULUS

- La Forja deja de llamarse "causal". Es **cribado causal**: identifica
  candidatos y pruebas de necesidad, no efectos.
- La puerta de promoción exige evidencia de nivel L3; sin ella, no hay Canon.
- El Canon distingue "procedimiento verificado" de "procedimiento causalmente
  validado".
- El Pod necesita un auditor de validez, no solo un auditor de ejecución.

### JANUS

- El ledger de decisiones es la materia prima de la identificación.
- La jerarquía de evidencia es la regla de promoción.
- Los contrafactuales de nivel 4 son hipótesis, nunca prueba.
- El "sueño contrafactual" debe declarar qué métodos usó y qué supuestos.

## 7. Checklist para cualquier mecanismo

Antes de entrar al diseño, un mecanismo debe responder:

1. ¿Cuál es el fenómeno L1 y con qué evidencia?
2. ¿Cuál es el análogo L2 y en qué se diferencia del original?
3. ¿Cuál es la alternativa simple L3 contra la que compite?
4. ¿Qué predicción falsable hace?
5. ¿Qué error produciría si la analogía es falsa?
6. ¿Cómo se mide su contribución marginal?
7. ¿Qué pasa si se elimina?

Si no responde 3–7, no es un mecanismo: es una metáfora.

## 8. Conclusión

La biología y la sociología no son evidencia de una arquitectura. Son fuentes de
hipótesis y restricciones. La ciencia de un sistema de memoria empieza cuando se
puede decir: **esto mejora aquello, frente a esta alternativa, con este costo y
bajo estas condiciones**. Todo lo demás es preparación.
