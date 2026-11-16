# 08 — Protocolo experimental v2.0

**Estado:** reescrito tras la revisión mayor. Sustituye al protocolo anterior.
Este documento es la única versión vigente; cualquier otro conjunto de
condiciones en el repositorio es histórico.

## 1. Pregunta y niveles

La pregunta principal se descompone en seis:

1. ¿Qué información de una trayectoria predice su utilidad futura?
2. ¿Se pueden inducir procedimientos reutilizables mediante intervenciones
   causales?
3. ¿Qué hace portable una habilidad entre modelos?
4. ¿Cuándo ayuda o perjudica la consolidación selectiva?
5. ¿La validación colectiva supera a la individual con igual presupuesto?
6. ¿Las mejoras persisten cuando cambian entorno, modelo y distribución?

**Unidad de aprendizaje:** el sistema (modelo + memoria + herramientas +
artefactos). No se afirma aprendizaje paramétrico.

**Definición operacional:** hay aprendizaje acumulativo externo cuando la
experiencia previa produce una mejora reproducible en tareas futuras no
observadas, bajo condiciones controladas, y persiste tras reinicios de contexto y
cambios de modelo.

## 2. Hipótesis

### 2.1 Primaria

> **H1.** Un sistema con memoria procedural (CUMULUS o equivalente) supera a un
> repositorio simple de habilidades en Markdown con tests y recuperador, en éxito
> sobre instancias reservadas de familias recurrentes, con presupuesto de cómputo
> igualado y tras reinicios de contexto.

**Métrica primaria:** tasa de éxito en instancias reservadas de familias
recurrentes, medida como diferencia absoluta en puntos porcentuales.

**Por qué esta y no otra:** es la métrica que importa al usuario, la más fácil de
verificar y la que el rival simple también puede optimizar. Si no hay diferencia
aquí, la arquitectura no aporta.

### 2.2 Secundarias (jerarquizadas)

| # | Hipótesis | Métrica | Corrección |
|---|---|---|---|
| H2 | La consolidación selectiva mejora la retención | Retención tras reinicio | Holm |
| H3 | La portabilidad medida predice transferencia | AUC de portabilidad | Holm |
| H4 | La validación ciega reduce skills espurias | Tasa de promoción con efecto nulo | Holm |
| H5 | La memoria contrafactual mejora el crédito | Precisión de atribución causal | Holm |
| H6 | La capa social mejora con igual presupuesto | Éxito por 1k tokens | Holm |
| H7 | El olvido selectivo mejora precisión sin perder crítico | Precisión; retención crítica | Holm |

Las exploratorias se reportan como exploratorias, sin corrección, y no sostienen
la conclusión principal.

## 3. Condiciones

Todas las condiciones usan el mismo modelo base, las mismas herramientas y el
mismo límite de tokens, llamadas y tiempo por tarea. El costo se reporta.

| Condición | Descripción |
|---|---|
| C0 | Sin memoria: solo contexto de la tarea |
| C1 | Resumen rodante del historial |
| C2 | RAG sobre episodios y hechos |
| C3 | **Rival simple:** repositorio Markdown de procedimientos + tests + recuperador léxico/vectorial |
| C4 | Zep Agent Skills (adaptación o reimplementación) |
| C5 | MSCE-style: trazas → políticas → skills con gobernanza heurística |
| C6 | CUMULUS sin capa social |
| C7 | CUMULUS completo |
| C8 | JANUS (contrafactual + puerta causal) |

**Igualación de presupuesto:** cada condición recibe el mismo máximo de tokens de
entrada, tokens de salida, llamadas a herramientas y tiempo de pared. Si una
condición necesita más, se reporta como costo adicional y se compara también por
éxito por unidad de costo.

## 4. Datos y entornos

### 4.1 Benchmark longitudinal

- **5 dominios:** reparación de código, pipelines de datos, síntesis de
  documentos, respuesta a incidentes, orquestación de herramientas.
- **10 familias por dominio**, 20 instancias por familia (10 públicas, 10
  reservadas).
- **8 ciclos** con 100 tareas por ciclo.
- **Reinicio de contexto** al final de cada ciclo.
- **Eventos de deriva programados:** en los ciclos 3, 5 y 7 cambia algo relevante:
  versión de modelo, API de herramienta, requisito del usuario o distribución de
  tareas. No es solo "pasar tiempo": es cambiar el mundo.
- **Holdouts ocultos** por familia para detectar sobreajuste al verificador.

### 4.2 Verificadores

- **Ejecutables** cuando sea posible: tests, esquemas, validaciones de salida.
- **Jueces LLM** solo para lo abierto: al menos dos familias de modelos distintas,
  ciegos al autor y a la condición, con rúbrica.
- **Auditoría humana** de una muestra aleatoria del 10%; se reporta acuerdo
  inter-juez (kappa) y discrepancias.
- **Verificación del verificador:** tests de mutación y casos adversariales para
  detectar verificadores defectuosos.

## 5. Potencia y análisis

### 5.1 Piloto obligatorio

Antes de la corrida principal se ejecuta un piloto con 30 tareas por condición
para estimar varianza y costo. Con esa varianza se calcula N por celda para
detectar un efecto mínimo de 10 puntos porcentuales con 80% de potencia y
\(\alpha = 0.05\) bilateral. El cálculo se publica antes de la corrida.

### 5.2 Unidad y modelo estadístico

- Unidad: tarea dentro de familia, agrupada por ciclo.
- Modelo: efectos mixtos con dificultad de tarea como covariable y familia como
  efecto aleatorio.
- Comparaciones pareadas por tarea.
- Intervalos de confianza por bootstrap (10.000 remuestreos).
- Se reporta tamaño de efecto, no solo p-valor.

### 5.3 Multiplicidad

- Una métrica primaria (H1).
- Secundarias con Holm–Bonferroni.
- Exploratorias etiquetadas; no se usan para afirmar la conclusión.

### 5.4 Transferencia

Se reportan:

- **delta absoluto:** \(S(m', C+s) - S(m', C)\);
- **delta relativo:** respecto a la línea base del modelo receptor;
- **AUC de portabilidad:** capacidad del score de predecir éxito;
- **tasa de transferencia negativa.**

No se usa el cociente \(T\) con denominador inestable. Si se reporta, se hace
solo cuando el denominador está acotado lejos de cero y con intervalo de
confianza.

## 6. Ablaciones

| Ablación | Qué prueba |
|---|---|
| Sin Forja (solo trazas) | Valor de la compilación |
| Sin Canon (sin promoción) | Valor de la curaduría |
| Sin auditoría ciega | Valor de la independencia |
| Sin Puente (un solo modelo) | Valor de la portabilidad |
| Sin decaimiento | Valor del olvido |
| Sin capa social | Valor de la sociedad |
| Sin contrafactuales | Valor de JANUS |
| Sin verificación | Valor de los verificadores |

Cada ablación se compara con C6/C7/C8 y se reporta con el mismo presupuesto.

## 7. Errores correlacionados y capa social

En los Pods, los agentes pueden compartir modelo, prompt, datos y sesgos. El
quórum no es independencia.

- Se simula una correlación \(\rho\) entre evaluadores (0, 0.3, 0.6, 0.9) y se
  mide cómo cambia la tasa de falsas promociones.
- Se mide diversidad de evidencia (modelos, herramientas, fuentes) por promoción.
- Se compara Pod con presupuesto igualado contra un verificador único con el mismo
  presupuesto.
- Si el Pod no supera al verificador único, la capa social no se justifica.

## 8. Criterios de éxito y de muerte

### Éxito mínimo

- H1: diferencia absoluta ≥10 pp a favor de C6/C8 sobre C3, con IC 95% que excluya
  0.
- Costo por éxito no más de 50% superior al de C3.
- Retención tras reinicio ≥80% de la ganancia pico.

### Éxito fuerte

- C8 (JANUS) reduce la tasa de skills espurias ≥30% frente a C6.
- La portabilidad predice transferencia con AUC ≥0.7.
- La capa social supera al verificador único con igual presupuesto.

### Muerte

- Si C6/C8 no supera a C3 en H1 con el IC excluyendo 0, la hipótesis falla.
- Si el costo por éxito se duplica sin mejora, la arquitectura no es viable.
- Si la capa social no supera al verificador único, se elimina.

## 9. Amenazas a la validez

- **No determinismo:** semillas cuando sea posible; múltiples corridas;
  comparación pareada.
- **Sesgo del juez:** familias distintas, ciego, auditoría humana, kappa.
- **Contaminación:** benchmark propio no publicado; holdouts ocultos.
- **Confusión por costo:** presupuesto igualado y éxito por costo.
- **Novedad:** mismo esfuerzo de ingeniería en C3/C4/C5.
- **Deriva de versión:** fijar versiones, registrar hashes, introducir deriva
  programada.
- **Sobreajuste al verificador:** tests de mutación y casos adversariales.

## 10. Qué falsaría la tesis

Si el rival simple (Markdown + tests + recuperador) iguala o supera a CUMULUS en
H1 con el mismo presupuesto, la arquitectura no aporta y debe reducirse a ese
rival. Si JANUS no reduce las skills espurias frente a C6, la memoria
contrafactual no se justifica.

## 11. Reproducibilidad

- Protocolo versionado (`v2.0`).
- Semillas, prompts, versiones de modelo y hashes de datos.
- Scripts de análisis y resultados crudos.
- Informe de potencia previo.
- Un solo protocolo vigente; los anteriores se archivan como históricos.
