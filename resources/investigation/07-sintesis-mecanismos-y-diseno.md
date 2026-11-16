# 07 — Síntesis: de la biología al sistema

## 1. Criterio de traducción

Un mecanismo entra al diseño solo si cumple las tres condiciones:

1. **Tiene evidencia del fenómeno** (etiqueta `[A]`, `[B]` o `[C]` según el
   README).
2. **Tiene una traducción computacional honesta** (no requiere simular biología).
3. **Puede ser ablacionado**: si quitarlo no empeora una métrica, se elimina.

La biología no es el objetivo. Es un catálogo de soluciones probadas a problemas
de información: qué guardar, cuánto, dónde, por cuánto tiempo y con quién
compartirlo.

**Advertencia de validez (revisión mayor):** la columna "Evidencia del fenómeno"
califica **solo el nivel L1** (¿el fenómeno existe?). No califica la traducción
computacional (L2) ni la ventaja comparativa (L3). Un `[A]` en la tabla significa
"el fenómeno está bien establecido", no "el componente funciona". El marco
completo está en `23-marco-de-validez.md`.

## 2. Tabla maestra de mecanismos

### 0. Estado de traducción

| Mecanismo | L1 fenómeno | L2 traducción | L3 ventaja | Qué falta |
|---|---|---|---|---|
| Dos velocidades (CLS) | Fuerte | Almacén rápido + lento | No probada | Comparar contra un solo almacén con buen retrieval |
| Consolidación offline | Fuerte | Job de consolidación | No probada | Aislar repetición, selección y abstracción |
| Olvido selectivo | Fuerte | Decaimiento + archivo | Parcial | Demostrar precisión sin perder crítico |
| Saliencia | Buena | Vector de pesos | No probada | Calibrar sin juez humano |
| Esquemas | Buena | Extracción de estructura | No probada | Medir generalización vs. resumen |
| Memoria transactiva | Fuerte | Directorio de expertise | No probada | Comparar con enrutamiento aleatorio |
| Quórum | Fuerte en hormigas | Promoción por corroboración | No probada | Modelar errores correlacionados |
| Estigmergia | Fuerte | Trazas con evaporación | No probada | Evitar amplificación de errores |
| Enseñanza | Buena en orcas/primates | `teach()` con verificación | No probada | Medir fidelidad de ejecución |
| Práctica de recuperación | Fuerte en humanos | Refuerzo por uso | **Débil** | Riesgo de monopolio; tratar como hipótesis |
| Legitimidad weberiana | Interpretativa | Regímenes de validez | **Débil** | Separar legitimidad de verdad |
| Sueño como compactación | Parcial | Fase offline | **Débil** | Distinguir mecanismos; no es identidad |

**Lectura:** casi ningún mecanismo tiene evidencia L3 en agentes LLM. Eso no los
invalida; obliga a probarlos, no a asumirlos.


### A. Codificación (hipocampo digital)

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Codificación one-shot con contexto | [A] | Guardar el evento completo la primera vez | `encode()` con contexto y procedencia | % de eventos recuperables | Ruido si todo se guarda |
| Separación de patrones | [B] | Distinguir lo parecido antes de asociar | Detección de duplicados + novedad | Tasa de duplicados; precisión de distinción | Sobre-separar y perder generalización |
| Indexado y enlaces | [A] | El recuerdo es un nodo con aristas | Grafo de asociaciones al escribir | Recall multi-hop | Grafo que se vuelve una maraña |
| Vector de saliencia | [B] | No todo se refuerza igual | `{novedad, recompensa, sorpresa, amenaza, social}` | Correlación con importancia humana | Saliencia mal calibrada = sesgo |
| Compuerta de memoria de trabajo | [A] | El contexto se administra | Presupuesto + política de desalojo | Tokens por tarea; aciertos | Desalojar lo que hacía falta |

### B. Consolidación (corteza digital)

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Replay offline | [A] | Repasar mezclado extrae estructura | Job de consolidación | Esquemas útiles por ciclo | Costo de cómputo |
| Extracción de esquemas | [B] | Regularidad, no anécdota | `induce()` sobre clústeres | Reutilización del esquema | Resumen que pierde el porqué |
| Vía rápida por esquema | [B] | Lo congruente se asimila antes | Puntuación de congruencia | Latencia de consolidación | Sesgo de confirmación |
| Quórum de corroboración | [B] | N fuentes independientes antes de promover | Umbral configurable | Precisión vs. cobertura | Estancamiento si N es alto |
| Intercalado | [A] | Mezclar dominios mejora transferencia | Replay entre dominios | Transferencia entre tareas | Contaminación entre dominios |
| Validez temporal | [A] | Un hecho puede dejar de ser cierto | Aristas con intervalo | Respuestas obsoletas | Complejidad del grafo |

### C. Olvido y estabilidad

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Decaimiento por desuso | [B] | Lo no usado pierde fuerza | Peso con función de decaimiento | Retención de lo importante | Perder lo raro pero crítico |
| Protección por saliencia | [B] | Lo importante no decae | Piso de peso por saliencia | % de críticos retenidos | Inflación de saliencia |
| Reconsolidación al recuperar | [B] | Recuperar actualiza | Actualización de contexto/fuerza | Corrección de recuerdos | Deriva por uso |
| Archivo, no borrado | [C] | El olvido debe ser auditable | Estado `archived` | Trazabilidad | Crecimiento del almacenamiento |
| Contradicciones preservadas | [C] | El disenso es información | Nodos contradictorios ligados | Tasa de contradicción detectada | Ruido si no se resuelve nunca |

### D. Procedimiento (ganglios basales digitales)

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Playbooks con estadísticas | [B] | La habilidad se mide por resultados | Procedimiento + éxito/fallo | Tasa de éxito por tarea | Sobreajuste a un contexto |
| Chunking | [B] | Comprimir secuencias en unidades | Compilación de rutinas | Tokens por tarea resuelta | Perder pasos necesarios |
| Etiqueta de error/amenaza | [A] | El fallo se recuerda distinto | `threat` en saliencia | Reincidencia de errores | Evitación excesiva |
| Feedback y práctica | [A] | Sin corrección no hay mejora | Registro de causa de fallo | Mejora por iteración | Feedback caro o tardío |

### E. Sociedad (orcas, hormigas, sociología)

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Directorio de expertise | [A] | "Quién sabe qué" | Registro agente–dominio–éxito | Aciertos de enrutamiento | Popularidad ≠ competencia |
| Pods y dialectos | [B] | Vocabulario compartido comprime y une | Glosario por pod | Tokens; recall del novato | Aislamiento entre pods |
| Transmisión vertical | [B] | Enseñar conserva fidelidad | `teach()` con verificación | Fidelidad de ejecución | Cuello de botella del maestro |
| Custodio/anciano | [B] | El conocimiento crítico necesita curador | Rol de curación y respuesta | Cobertura de preguntas críticas | Punto único de fallo |
| Campo estigmérgico | [B] | Trazas compartidas que decaen | Grafo de uso con evaporación | Coordinación sin mensajes | Amplificar un error temprano |
| Reputación/gossip | [B] | Confianza de bajo costo | Score + reportes | Predicción de calidad | Difamación/cascadas |
| Gobernanza | [C] | Reglas de escritura y procedencia | Políticas por pod | Contaminación | Burocracia |
| Vínculos débiles | [B] | La novedad viene de lejos | Enlaces entre pods | Descubrimientos cruzados | Ruido |

### F. Instituciones, psicología y biología comparada

| Mecanismo | Evidencia del fenómeno | Principio | Componente | Métrica | Riesgo |
|---|---|---|---|---|---|
| Expediente y procedencia (Weber) | [C] | Un recuerdo vale por su respaldo | Autor, fecha, norma, estado | Trazabilidad | Burocracia |
| Tres legitimidades | [C] | Cada conocimiento se valida distinto | Canon / prestigio / evidencia | Consistencia de validación | Rigidez |
| Rutinización del carisma | [B] | La intuición exitosa se vuelve procedimiento | Episodio → playbook → regla | Reutilización | Jaula de hierro |
| Reconstrucción y contaminación | [A] | Recuperar puede distorsionar | Fuente separada de interpretación | Tasa de confabulación | Parálisis por duda |
| Olvido inducido por recuperación | [A] | Recordar A debilita B | Cuotas de diversidad en recall | Cobertura | Ruido |
| Inhibición colaborativa | [A] | El grupo recuerda menos que la suma | Buffers individuales | Ítems únicos recuperados | Costo de coordinación |
| Seguridad psicológica | [B] | Sin reporte seguro no hay aprendizaje del error | Registro de fallos sin castigo | Tasa de errores reportados | Impunidad |
| Identidad narrativa | [B] | La identidad filtra relevancia | Diario de compromisos | Coherencia de decisiones | Rigidez identitaria |
| Memoria por selección (inmune) | [B] | Variantes → resultado → amplificación | Playbooks competitivos | Mejora por ciclo | Convergencia local |
| Período crítico / onboarding | [B] | El dialecto se aprende al entrar | Andamiaje temprano | Tiempo a paridad | Exclusión |
| Identidad por señal | [B] | El nombre y el dialecto reconocen pertenencia | ID estable + glosario | Reconocimiento entre pods | Colusión |

**Síntesis de las ampliaciones (09–12):**

- **Weber** aporta la capa institucional: sin expediente, jurisdicción y reglas de
  validez, la memoria compartida es un rumor. Su advertencia —la jaula de
  hierro— es el límite superior de la consolidación.
- **Psicología** aporta la higiene: la memoria reconstruye, se contamina, se
  inhibe en grupo y se sesga hacia la decisión vigente. Procedencia,
  contraevidencia y buffers individuales no son opcionales.
- **Biología comparada** aporta la prueba de que la memoria puede ser externa
  (moho), selectiva (inmune), química (bacteria) y cultural (cetáceos). También
  aporta el antiejemplo: el pulpo es inteligente y solitario, y su conocimiento
  muere con él.
- **Humano vs. máquina** aporta el realismo: el trade-off transferencia /
  interferencia es compartido (Holton et al., 2026), así que el sistema no puede
  prometer eliminar la interferencia; solo gestionarla por dominio.

## 3. Los cinco subsistemas

```
                    ┌──────────────────────────────┐
   evento ────────► │  A. Codificación (hipocampo) │
                    │  separar · indexar · saliencia│
                    └──────────────┬───────────────┘
                                   │ índice + prioridad
                    ┌──────────────▼───────────────┐
                    │  B. Consolidación (corteza)  │
                    │  replay · esquemas · quórum  │
                    └───────┬──────────────┬───────┘
                            │              │
              ┌─────────────▼───┐   ┌──────▼────────────┐
              │ C. Olvido       │   │ D. Procedimiento  │
              │ decaer · archivar│   │ playbooks · stats │
              └─────────────┬───┘   └──────┬────────────┘
                            │              │
                    ┌───────▼──────────────▼───────┐
                    │  E. Sociedad                 │
                    │ directorio · pods · teach    │
                    │ reputación · gobernanza      │
                    └──────────────────────────────┘
```

El núcleo (A–D) funciona para un solo agente. La capa E es aditiva: si se apaga,
el sistema sigue siendo una mente individual competente.

## 4. El bucle de la mente

```
encode(evento, agente, dominio):
    ctx   = memoria_de_trabajo.actual()
    x     = separar(evento, ctx)                 # ¿es nuevo o conocido?
    sal   = saliencia(evento, ctx)               # novedad, recompensa, sorpresa,
                                                 # amenaza, señal social
    e     = guardar(x, contexto=ctx, saliencia=sal,
                    procedencia={agente, dominio, tarea, hora})
    enlazar(e, asociaciones(x, k))               # grafo, no fila suelta
    si sal.alta: reforzar(e); difundir(e, pod)   # baile / gossip
    programar_consolidacion(e, prioridad=sal)

recall(consulta, agente, dominio):
    ruta  = directorio.expertos(consulta, dominio)     # memoria transactiva
    cands = busqueda_hibrida(consulta, politicas[dominio],
                             expandir_grafo=True)
    cands = rerank(cands, relevancia, recencia, saliencia,
                   confianza, error_de_prediccion)
    reforzar(cands)                                    # práctica de recuperación
    devolver(ensamblar(cands, presupuesto=memoria_de_trabajo))

consolidar():                                          # "sueño"
    para cluster en replay_intercalado(pendientes):
        si corroboracion(cluster) >= quorum:
            esquema = inducir(cluster)                 # LLM + validación
            si valida(esquema, evidencia):
                promover(esquema, corteza)
                enlazar(esquema, evidencia)
                decaer(evidencia)                      # el episodio se desvanece
    podar(peso_bajo y sin_uso y saliencia_baja)
    actualizar_procedimientos(resultados)
    reprogramar_repasos(curva_de_espaciado)

cerrar_tarea(tarea, resultado):
    actualizar_estadisticas(procedimiento, resultado)
    si fallo: etiquetar_amenaza(episodio)
    si éxito_novedoso: difundir + candidato_a_innovacion
    registrar_causa(resultado)                         # feedback, no solo métrica
```

## 5. Mapeo a los cuatro requisitos

| Requisito | Cómo se cumple |
|---|---|
| 1. Aprendizaje continuo y progresivo de tareas distintas | D (playbooks con estadísticas) + B (replay intercalado) + feedback de resultado. El progreso se mide por mejora en la tasa de éxito entre sesiones, no por tokens acumulados. |
| 2. Memoria selectiva por campo | Políticas por dominio: qué se guarda, qué decae, cómo se recupera, qué vocabulario se usa. Aislamiento por defecto; enlace débil explícito. |
| 3. Hipocampo: memoria rápida y asociación | A: escritura one-shot, separación de patrones, índice y grafo de asociaciones. |
| 4. Corteza: aprendizaje gradual | B: consolidación offline, extracción de esquemas, promoción por quórum, validez temporal. |

Nótese que 3 y 4 son **el mismo sistema en dos fases**. Sin la fase lenta, el
hipocampo se llena de ruido; sin la rápida, la corteza nunca ve un caso
concreto.

## 6. La capa societal

No es "varios agentes hablando". Es infraestructura:

- **Directorio de expertise** (memoria transactiva): rutea preguntas.
- **Pods**: agrupaciones con dialecto, políticas y memoria compartida.
- **Transmisión**: vertical (custodio → novato), horizontal (par → par) y
  oblicua (experto → agente de otro pod).
- **Reputación**: confianza calibrada por resultados, no por volumen.
- **Gobernanza**: procedencia obligatoria, permisos de escritura, contradicciones
  preservadas, archivo en vez de borrado.
- **Vínculos débiles**: un agente que participa en dos pods es la fuente de
  asociaciones nuevas.

El riesgo sociológico está documentado: conformidad, cascadas, groupthink y
sesgo colectivo emergente (Ashery et al., 2025). Por eso la consolidación no
puede ser votación: debe conservar minorías y evidencia en contra.

## 7. ¿Esto sirve? Utilidad real y promesas falsas

**Lo que promete:**

1. **Continuidad de decisiones**: el "por qué" sobrevive a la compactación.
2. **Transferencia de procedimientos**: lo aprendido en un proyecto se reutiliza
   en otro con condiciones explícitas.
3. **Menos costo de contexto**: recuperar lo pertinente en vez de arrastrar todo.
4. **Menos contradicciones**: validez temporal y procedencia evitan que el agente
   repita una decisión revocada.
5. **Arranque más rápido de agentes nuevos**: dialecto + directorio + andamiaje.
6. **Progreso medible**: tasa de éxito y reincidencia de errores entre sesiones.

**Lo que no promete:**

- Conciencia, emoción sentida o "mente" en sentido filosófico.
- Simulación neuronal fiel.
- AGI.
- Que la metáfora biológica, por sí sola, mejore nada. Si un módulo no supera
  una ablación, se elimina aunque sea muy bonito.

**El criterio de utilidad:** un agente con este sistema, tras N sesiones, debe
(a) repetir menos errores, (b) necesitar menos contexto para la misma tarea,
(c) transferir mejor un procedimiento y (d) contradecir menos sus decisiones
previas que el mismo agente con RAG + resumen. Si no, la tesis falla.

## 8. Decisiones de diseño que quedan abiertas

1. **Almacenamiento**: SQLite + extensión vectorial (simple, local) vs. Postgres
   + pgvector (multi-usuario, servidor). Para "instalar en un computador", SQLite
   gana; para pods, Postgres.
2. **Embeddings**: modelo local (offline, costo cero, menor calidad) vs. API
   (mejor calidad, costo por escritura). Probablemente configurable.
3. **Consolidación**: ¿la hace el LLM del cliente (gratis para el servidor, pero
   depende de que el cliente colabore) o un LLM propio configurado (autónomo,
   con costo)? El diseño debe permitir ambas.
4. **Interfaz**: MCP es el estándar para agentes; una API HTTP para todo lo demás.
5. **Alcance inicial**: un usuario, un proyecto, varios dominios. La capa social
   se diseña desde el inicio pero se activa después.
6. **Evaluación**: harness longitudinal propio (doc 08) antes de optimizar.

## 9. Principios de diseño

1. **Parsimonia biológica**: cada mecanismo paga con una ablación.
2. **Determinista por defecto**: el LLM solo donde aporta (inducir esquemas,
   juzgar saliencia); lo demás es aritmética barata.
3. **Procedencia total**: todo recuerdo sabe de dónde vino, cuándo y con qué
   confianza.
4. **Nada se borra sin archivo**: el olvido es degradación de acceso, no
   desaparición.
5. **El contexto es presupuesto**: se administra, no se llena.
6. **La sociedad es una capa**: el núcleo funciona solo; la capa social multiplica.
7. **Contradicción preservada**: el sistema muestra el desacuerdo, no lo promedia.
