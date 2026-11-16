# El riesgo del olvido

### Memoria, olvido y transmisión en agentes inteligentes

**Juan David Salas Camargo** — Massachusetts Institute of Technology (MIT)  
**DeepSeek** — Modelo de lenguaje

*Documento de trabajo · v0.1 · noviembre de 2026 · no arbitrado*

---

## Resumen

El cuello de botella de los agentes basados en modelos de lenguaje ya no es la
ventana de contexto. Es la ausencia de un **ciclo de vida de la memoria**. Cuando
el contexto se compacta, el agente conserva hechos y pierde métodos, motivos y
legitimidad; al cabo de un millón de tokens parece "estúpido otra vez". Este
trabajo sostiene que el olvido no es el enemigo: el riesgo es el **olvido
equivocado**, que elimina lo que hacía competente al agente mientras acumula
ruido. A partir de neurología (sistemas complementarios, consolidación,
reconsolidación, olvido adaptativo, neuromodulación), biología comparada (orcas,
córvidos, hormigas, sistema inmune), sociología (Weber, memoria transactiva,
comunidades de práctica) y aprendizaje de máquinas (aprendizaje continuo,
interferencia catastrófica, memoria de agentes), proponemos una arquitectura de
cinco subsistemas —codificación, consolidación, olvido, procedimiento y
sociedad— y una métrica longitudinal para falsarla. La tesis es simple:
**recordar no es almacenar; es saber qué perder, cuándo y con quién.**

**Palabras clave:** memoria de agentes, olvido adaptativo, consolidación,
transmisión cultural, memoria transactiva, aprendizaje continuo.

---

## 1. Introducción: el problema del millón de tokens

Un agente trabaja durante semanas en un proyecto. Toma decisiones, descubre
restricciones, corrige errores, aprende el vocabulario del equipo. Un día el
contexto se llena. El sistema compacta: resume, descarta, prioriza lo reciente.
El agente sigue respondiendo con fluidez. Pero ha perdido algo que no aparece en
el resumen: **por qué** se eligió una arquitectura, **cómo** se resolvió un bug
que ya se había resuelto, **quién** validó una decisión y **qué** se probó y
falló.

El fenómeno es conocido por cualquiera que use agentes a diario: después de
cierto punto, el agente vuelve a proponer lo que ya se descartó, repite errores
corregidos y contradice decisiones vigentes. No es un fallo de razonamiento. Es
un fallo de **continuidad**.

La respuesta habitual es "más contexto" o "mejor retrieval". Ambas cosas ayudan,
pero no tocan el problema. El contexto es memoria de trabajo, no memoria a largo
plazo. El retrieval devuelve fragmentos parecidos, no procedimientos
verificados. Y ningún sistema actual decide **qué debe olvidarse**.

Este trabajo argumenta que el problema es de ciclo de vida y de estructura
social, y que la biología ofrece un catálogo de soluciones probadas —no para
copiar neuronas, sino para copiar **políticas**.

## 2. El olvido no es el enemigo

### 2.1 Las seis pérdidas

Llamamos "riesgo del olvido" a seis pérdidas distintas que suelen confundirse en
una sola:

| # | Pérdida | Qué se pierde | Síntoma |
|---|---|---|---|
| F1 | De método | El procedimiento que funcionó | Se resuelve de nuevo, peor |
| F2 | De motivo | El porqué de una decisión | Se revierte sin saber qué se sacrificó |
| F3 | De dominio | La separación entre campos | Interferencia y respuestas híbridas |
| F4 | De legitimidad | Quién validó y con qué evidencia | Se acepta un rumor como decisión |
| F5 | De lo crítico | Lo raro pero esencial | Un detalle de una sola vez desaparece |
| F6 | De novedad | La capacidad de sorprenderse | Sobre-consolidación y jaula de hierro |

Las tres primeras producen la sensación de "agente estúpido". La cuarta produce
contradicciones. La quinta produce incidentes evitables. La sexta produce un
sistema que ya no aprende.

### 2.2 La regla de la triple fidelidad

Una memoria es útil si conserva tres cosas:

1. **Fidelidad de método**: el procedimiento se puede ejecutar igual.
2. **Fidelidad de motivo**: se puede explicar por qué se eligió.
3. **Fidelidad de legitimidad**: se puede rastrear quién lo validó y con qué
   evidencia.

Un resumen típico conserva el "qué" y pierde las tres. Por eso un agente con
memoria aparentemente buena vuelve a ser incompetente: tiene datos, no tiene
criterio.

### 2.3 El principio de la abuela

En las orcas residentes, las hembras post-reproductivas lideran los movimientos
colectivos, sobre todo en años de escasez (Brent et al., 2015). No producen
crías, pero custodian el conocimiento ecológico que el grupo necesita cuando la
situación es difícil. En términos de sistema: hace falta un **custodio** que no
genere trabajo nuevo pero cure, valide y enseñe lo crítico.

## 3. Lo que enseña la neurología

### 3.1 Dos sistemas, no uno

La teoría de sistemas complementarios (McClelland, McNaughton y O'Reilly, 1995;
Kumaran, Hassabis y McClelland, 2016) propone que el hipocampo aprende rápido,
de forma dispersa y episódica, mientras la corteza aprende lento, de forma
distribuida y semántica. El hipocampo indexa; la corteza generaliza; el sueño
los conecta (Wilson y McNaughton, 1994; Rasch y Born, 2013).

Un solo índice vectorial no puede ser las dos cosas. La memoria de un agente
necesita **dos velocidades**.

### 3.2 Consolidar es seleccionar y abstraer

El sueño no copia el día: hace **triaje** (Stickgold y Walker, 2013), selecciona,
integra y generaliza. Los esquemas previos aceleran la consolidación de lo
congruente (Tse et al., 2007). La consolidación es, por tanto, un proceso de
selección con criterios, no un resumen.

### 3.3 Recuperar es reescribir

La reconsolidación (Nader, Schafe y LeDoux, 2000) muestra que recordar vuelve
lábil la huella y permite actualizarla. Recuperar no es leer: es escribir de
nuevo. Un sistema que solo lee nunca corrige sus recuerdos.

### 3.4 Olvidar es adaptativo

El olvido no es un fallo: es una función (Richards y Frankland, 2017; Ryan y
Frankland, 2022). Lo que se olvida no se borra necesariamente: cambia su
**accesibilidad**. La neurogénesis adulta, la interferencia y la supresión
motivada compiten por la misma huella.

La implicación de diseño es fuerte: el olvido debe ser un cambio de estado
(peso, claves, contexto), no un `DELETE`. Archivar permite auditar y, a veces,
recuperar.

### 3.5 La saliencia gobierna

Dopamina (error de predicción de recompensa; Schultz, Dayan y Montague, 1997),
noradrenalina (ganancia adaptativa; Aston-Jones y Cohen, 2005), acetilcolina
(codificar vs. recuperar; Hasselmo, 1999), oxitocina (señal social; Kosfeld et
al., 2005) y cortisol (curva en U; Joëls et al., 2006) no son "emociones": son
canales que deciden qué se consolida, cuánto decae y qué se recupera.

Un vector de saliencia de pocas dimensiones —novedad, recompensa, sorpresa,
amenaza, señal social— es suficiente para convertir "guardar todo" en "guardar
lo que importa".

## 4. Lo que enseña la biología social

### 4.1 Orcas: especialización, dialecto y custodia

Los ecotipos de orca tienen dieta, comportamiento y repertorio vocal propios. Los
dialectos se transmiten por matrilina y cambian lentamente (Ford, 1991; Deecke,
Ford y Spong, 2000). Las matriarcas lideran cuando el conocimiento escasea
(Brent et al., 2015). La enseñanza de técnicas complejas es intencional y
costosa (Guinet y Bouvier, 1995).

Lección: **especialización ecológica + dialecto + custodia + enseñanza** son un
paquete. No se puede tener transmisión de alta fidelidad sin custodia, ni
custodia sin especialización.

### 4.2 Córvidos: qué, dónde, cuándo

Los arrendajos recuerdan qué escondieron, dónde y cuándo (Clayton y Dickinson,
1998); los cuervos de Nueva Caledonia fabrican herramientas con variación
cultural (Hunt y Gray, 2003) y usan metatool (Taylor et al., 2007). La memoria
episódica-like es un índice temporal y contextual, no un texto.

### 4.3 Hormigas: estigmergia y quórum

La estigmergia (Grassé, 1959) coordina por trazas que se refuerzan y evaporan
(Goss et al., 1989; Deneubourg et al., 1990). El quórum decide cuándo hay
suficiente corroboración (Pratt et al., 2002; Seeley y Visscher, 2004). La
división del trabajo emerge de umbrales (Bonabeau, Theraulaz y Deneubourg, 1996).

Lección: **memoria compartida = trazas que decaen + umbral de confirmación**. El
decaimiento no es un defecto; es lo que evita que un error temprano se convierta
en ley.

### 4.4 Sistema inmune: memoria por selección

La inmunidad adaptativa no "guarda" patógenos: selecciona clones que reconocen,
los amplifica y conserva células de memoria (Ahmed y Gray, 1996). Es un modelo
de memoria **generativa**: variantes → resultado → amplificación.

Lección: los procedimientos deben competir y ser seleccionados por resultado, no
solo por autoridad.

## 5. Lo que enseña la sociología

### 5.1 Weber: el expediente y la jaula

La burocracia es una tecnología de memoria: jurisdicción, jerarquía, expediente
(*Akten*), reglas e impersonalidad (Weber, 1922). Cada recuerdo debería tener
autor, fecha, norma y estado. Pero la racionalización excesiva produce la "jaula
de hierro": la estructura que protegía se vuelve contención.

Weber también distingue tres legitimidades —tradicional, carismática y
racional-legal— que en memoria se traducen en tres regímenes: canon, prestigio y
evidencia. Un sistema sano usa los tres y declara cuál aplica a cada tipo de
conocimiento.

### 5.2 Memoria transactiva: quién sabe qué

Wegner (1987) mostró que los grupos no recuerdan en conjunto: **dividen** la
memoria y mantienen un directorio de expertise. Los equipos con buena memoria
transactiva rinden mejor (Lewis, 2003; Ren y Argote, 2011).

Sin directorio, cada agente intenta recordarlo todo y termina recordando mal.

### 5.3 Comunidades de práctica y cultura acumulativa

Lave y Wenger (1991) describen el aprendizaje como participación periférica
legítima: el novato entra haciendo tareas reales periféricas, con un repertorio
compartido. Tomasello (1999) y Henrich (2015) muestran que la cultura acumulativa
depende de la **fidelidad de transmisión**: sin ella, cada generación reinventa.

### 5.4 Los riesgos sociales

Ashery, Aiello y Baronchelli (2025) demostraron que poblaciones de agentes LLM
desarrollan convenciones espontáneas y sesgos colectivos. La memoria compartida
puede amplificar errores. Por eso la consolidación no puede ser una votación:
debe preservar minorías, procedencia y contradicciones.

## 6. Lo que enseña la psicología

La memoria es reconstructiva (Bartlett, 1932) y maleable (Loftus y Palmer, 1974;
Roediger y McDermott, 1995). Recuperar un ítem debilita a sus competidores
(Anderson, Bjork y Bjork, 1994). Los grupos inhiben el recuerdo individual
(Weldon y Bellinger, 1997) y se contagian errores (Roediger, Meade y Bergman,
2001). La disonancia y el sesgo de confirmación empujan a interpretar la
evidencia a favor de la decisión vigente (Festinger, 1957; Kunda, 1990;
Nickerson, 1998).

Lección: cada recuperación y cada consolidación son una oportunidad de
contaminación. La procedencia y la contraevidencia no son lujos: son higiene
cognitiva.

## 7. El estado del arte y su hueco

Los sistemas actuales resuelven piezas:

- **MemGPT/Letta** (Packer et al., 2023): paginación y autogestión del contexto.
- **Generative Agents** (Park et al., 2023): memoria episódica con recuperación
  por recencia, importancia y relevancia; reflexión.
- **Mem0** (Chhikara et al., 2025): extracción, consolidación y actualización de
  hechos.
- **Zep/Graphiti** (Rasmussen et al., 2025): grafo temporal con validez de
  relaciones.
- **HippoRAG** (Gutiérrez et al., 2024, 2025): indexado hipocámpico y propagación
  asociativa.
- **MemoryBank** (Zhong et al., 2024): decaimiento tipo Ebbinghaus.
- **Sleep-time compute** (Lin et al., 2025): cómputo offline para reorganizar
  memoria.
- **Aprendizaje continuo**: EWC (Kirkpatrick et al., 2017), replay (Rolnick et
  al., 2019), y la comparación humano–máquina de Holton et al. (2026).

El hueco se estrechó en 2026: Zep Agent Skills y MSCE ya integran trazas,
compilación de habilidades y gobernanza; Trace2Skill mide transferencia entre
modelos; AFTER evalúa transferencia entre tareas, roles y backbones. Lo que
ninguno añade es **validación causal y memoria contrafactual**. Los benchmarks
(LoCoMo, LongMemEval) miden recall puntual; los nuevos miden transferencia, pero
no meses de deriva real.

## 8. Arquitectura propuesta

### 8.1 Cinco subsistemas

1. **Codificación (hipocampo digital)**: escritura one-shot, separación de
   patrones, índice asociativo, vector de saliencia.
2. **Consolidación (corteza digital)**: replay intercalado, extracción de
   esquemas, promoción por quórum, validez temporal.
3. **Olvido**: decaimiento por desuso, protección por saliencia, archivo,
   reconsolidación al recuperar.
4. **Procedimiento**: playbooks con estadísticas de éxito, chunking, etiqueta de
   error.
5. **Sociedad**: directorio de expertise, pods y dialectos, enseñanza verificada,
   reputación, gobernanza, vínculos débiles.

### 8.2 El bucle

```
codificar(evento) → separar → saliencia → guardar + enlazar → difundir si es crítico
recuperar(consulta) → enrutar por expertise → búsqueda híbrida → rerank
                    → reforzar (reconsolidación) → ensamblar con presupuesto
consolidar() → replay intercalado → esquema si hay quórum → promover
             → decaer evidencia → podar → reprogramar repasos
cerrar_tarea() → actualizar playbook → etiquetar error → registrar causa
```

### 8.3 Principios

1. Cada mecanismo paga con una ablación.
2. Determinista por defecto; LLM solo donde aporta.
3. Procedencia total.
4. Nada se borra sin archivo.
5. El contexto es presupuesto.
6. La sociedad es una capa, no un requisito.
7. La contradicción se preserva.

## 9. El riesgo del olvido, formalizado

| Fallo | Mecanismo | Mitigación | Métrica |
|---|---|---|---|
| F1 método | Compactación lossy | Playbooks + enseñanza verificada | Fidelidad de ejecución |
| F2 motivo | Resumen sin contexto | Campo obligatorio de motivo | Decisiones recuperadas con porqué |
| F3 dominio | Índice único | Políticas por dominio | Precisión cruzada |
| F4 legitimidad | Sin procedencia | Expediente weberiano | Trazabilidad |
| F5 crítico | Decaimiento uniforme | Piso de saliencia | Retención de lo raro |
| F6 novedad | Sobre-consolidación | Exploración + revisión | Tasa de esquemas revisados |

## 10. Evaluación

La tesis se falsa con un benchmark longitudinal: 40–60 sesiones, requisitos que
cambian, tareas recurrentes, hechos raros críticos y ruido. Condiciones: contexto
completo, resumen rodante, RAG, sistema sin capa social y sistema completo.
Métricas primarias: decisiones correctas, éxito de tareas, transferencia,
contradicciones. Métricas secundarias: tokens por éxito, fidelidad de
transmisión, retención crítica, reincidencia.

Criterio de muerte: si en 30 sesiones el sistema no supera al resumen rodante en
al menos dos métricas primarias con efecto ≥10%, la tesis falla y el alcance se
reduce.

## 11. Limitaciones y ética

- No se reclama conciencia ni emoción sentida. La analogía es funcional.
- La memoria compartida plantea privacidad y gobernanza: qué se comparte, con
  quién y por cuánto tiempo.
- El sesgo colectivo es un riesgo documentado (Ashery et al., 2025); el sistema
  debe preservar disenso y procedencia.
- La evaluación con LLM juez introduce sesgos; se requieren rúbricas y doble
  juez.
- La biología inspira, no autoriza: cada módulo debe justificarse por su efecto.

## 12. Conclusión

El riesgo no es que un agente olvide. Es que olvide **lo que lo hacía
competente** y recuerde **lo que lo hace ruidoso**. La neurología muestra que el
olvido es una función; la biología social, que la transmisión es tan importante
como el almacenamiento; la sociología, que la memoria necesita legitimidad y
gobernanza; la psicología, que toda recuperación es una reconstrucción expuesta a
contaminación.

La propuesta es un ciclo de vida con dos velocidades, saliencia, consolidación
selectiva, olvido auditable y una capa social de custodia y enseñanza. No es un
cerebro simulado. Es una **institución de memoria** para agentes: un sistema que
sabe qué guardar, qué perder, por qué y con quién.

---

## Referencias seleccionadas

Ahmed, R., & Gray, D. (1996). Immunological memory and protective immunity.
*Science, 272*(5258), 54–60.

Anderson, M. C., Bjork, R. A., & Bjork, E. L. (1994). Remembering can cause
forgetting. *Journal of Experimental Psychology: Learning, Memory, and Cognition,
20*(5), 1063–1087.

Ashery, A. F., Aiello, L. M., & Baronchelli, A. (2025). Emergent social
conventions and collective bias in LLM populations. *Science Advances, 11*(20),
eadu9368.

Brent, L. J. N., et al. (2015). Ecological knowledge, leadership, and the
evolution of menopause in killer whales. *Current Biology, 25*(6), 746–750.

Chhikara, P., et al. (2025). *Mem0: Building production-ready AI agents with
scalable long-term memory*. arXiv:2504.19413.

Flesch, T., Balaguer, J., Dekker, R., Nili, H., & Summerfield, C. (2018).
Comparing continual task learning in minds and machines. *PNAS, 115*(44),
E10313–E10322.

Gutiérrez, B. J., et al. (2024). HippoRAG: Neurobiologically inspired long-term
memory for large language models. *NeurIPS, 37*.

Holton, E., Braun, L., Thompson, J. A. F., Grohn, J., & Summerfield, C. (2026).
Humans and neural networks show similar patterns of transfer and interference
during continual learning. *Nature Human Behaviour, 10*, 111–125.

Kumaran, D., Hassabis, D., & McClelland, J. L. (2016). What learning systems do
intelligent agents need? *Trends in Cognitive Sciences, 20*(7), 512–534.

Lin, K., et al. (2025). *Sleep-time compute: Beyond inference scaling at
test-time*. arXiv:2504.13171.

McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are
complementary learning systems in the hippocampus and neocortex. *Psychological
Review, 102*(3), 419–457.

Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human
behavior. *UIST 2023*.

Rasmussen, P., et al. (2025). *Zep: A temporal knowledge graph architecture for
agent memory*. arXiv:2501.13956.

Ryan, T. J., & Frankland, P. W. (2022). Forgetting as a form of adaptive engram
cell plasticity. *Nature Reviews Neuroscience, 23*(3), 173–186.

Stickgold, R., & Walker, M. P. (2013). Sleep-dependent memory triage. *Nature
Neuroscience, 16*(2), 139–145.

Weber, M. (1922). *Economía y sociedad*.

Wegner, D. M. (1987). Transactive memory: A contemporary analysis of the group
mind. En *Theories of Group Behavior* (pp. 185–208). Springer.

La bibliografía completa está en `14-referencias.md`.
