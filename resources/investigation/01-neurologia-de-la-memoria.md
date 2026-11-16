# 01 — Neurología de la memoria

## 1. La idea central

La memoria no es un disco. Es un conjunto de sistemas con **competencias
opuestas**: uno aprende rápido y pierde detalle; otro aprende lento y retiene
estructura. El cerebro no eligió entre velocidad y estabilidad: construyó dos
sistemas y los hizo hablar entre sí durante el sueño.

Esta es la teoría de **sistemas de aprendizaje complementarios (CLS)** —
McClelland, McNaughton y O'Reilly (1995), actualizada por Kumaran, Hassabis y
McClelland (2016) para agentes inteligentes. Es la piedra angular de todo lo
demás.

| Sistema | Aprende | Representa | Olvida | Análogo funcional |
|---|---|---|---|---|
| Hipocampo | One-shot, un evento | Disperso, específico, episódico | Rápido si no se consolida | Escritura inmediata + índice asociativo |
| Neocórtex | Gradual, muchas exposiciones | Distribuido, solapado, semántico | Muy lento | Esquemas y conocimiento estable |

El hipocampo **no guarda el recuerdo completo**: guarda un índice que liga las
piezas dispersas de la corteza (teoría del indexado hipocámpico, Teyler y
DiScenna, 1986). Recuperar es reensamblar, no leer una fila.

**Implicación de diseño:** dos almacenes con dinámicas distintas y un proceso de
transferencia. Un solo vector store no puede ser las dos cosas.

## 2. Piezas del sistema

### 2.1 Hipocampo: separación y completado de patrones

- **Separación de patrones** (giro dentado): eventos parecidos se codifican como
  distintos. Evita que "reunión del martes" y "reunión del jueves" colapsen.
- **Completado de patrones** (CA3): una pista parcial reactiva el episodio
  entero. Es recall asociativo, no búsqueda exacta.
- **Codificación dispersa**: pocas neuronas por recuerdo → alta capacidad y baja
  interferencia.

**Implicación:** separar *deduplicar* de *asociar*. Son operaciones opuestas:
una empuja recuerdos aparte, la otra los junta. Un sistema que solo hace
similitud coseno hace las dos mal.

### 2.2 Consolidación

- **Sináptica** (minutos–horas): estabilización local de la huella.
- **De sistemas** (días–años): reorganización hacia la corteza.
- **Modelo estándar** (Squire y Alvarez, 1995): el hipocampo es necesario al
  principio y prescindible después.
- **Teoría de trazas múltiples** (Nadel y Moscovitch, 1997): los episodios
  vívidos siguen dependiendo del hipocampo; lo que se semantiza es el esquema,
  no el recuerdo literal.

Matiz importante: no todo "sube" a la corteza. Lo episódico permanece
episódico. Lo que se consolida es la **regularidad**, no el evento.

- **Replay durante el sueño** (Wilson y McNaughton, 1994): el hipocampo reactiva
  secuencias y la corteza las integra. Replay de ondas lentas + integración REM
  (Rasch y Born, 2013).
- **Esquemas** (Tse et al., 2007): cuando ya existe un marco, lo nuevo
  congruente se asimila en días, no semanas. El esquema actúa como fast-track de
  consolidación.

**Implicación:** la consolidación no es "resumir". Es *replay intercalado* de
episodios para extraer estructura, y es más rápida cuando ya hay un esquema que
la recibe.

### 2.3 Reconsolidación

Un recuerdo recuperado se vuelve lábil y se reestabiliza, a veces con
modificaciones (Nader, Schafe y LeDoux, 2000). Recuperar es **escribir de
nuevo**, no solo leer. Tiene condiciones límite y no aplica a todo recuerdo
(B) — pero el principio es sólido: el uso actualiza la memoria.

**Implicación:** cada recuperación refuerza, actualiza contexto y puede corregir
el recuerdo. Un sistema que solo lee nunca mejora sus recuerdos.

### 2.4 Olvido

- Curva de Ebbinghaus (1885): decaimiento rápido al inicio, luego meseta.
- Interferencia: lo nuevo interfiere con lo viejo y viceversa.
- **Olvido adaptativo** (Richards y Frankland, 2017): olvidar no es un fallo; es
  una función que mejora generalización y reduce ruido.
- Poda sináptica y eliminación de conexiones débiles.

**Implicación:** el olvido debe ser una política explícita (decaimiento por
desuso, protegido por saliencia), no un efecto colateral de la compactación.

### 2.5 Engramas

Un recuerdo es un **conjunto** de neuronas activadas juntas, no una ubicación
(Josselyn, Köhler y Frankland, 2015). Se asignan (allocación), se reactivan y se
pueden activar artificialmente. La memoria es composicional y ligada a contexto.

**Implicación:** modelar el recuerdo como nodo con enlaces, no como texto suelto
con embedding. El enlace es parte del recuerdo.

### 2.6 Memoria de trabajo

- Actividad persistente en corteza prefrontal.
- Capacidad limitada: ~4 elementos (Cowan, 2001).
- *Gating* y actualización por ganglios basales (modelo PBWM de O'Reilly y
  Frank).

**Implicación:** la ventana de contexto es memoria de trabajo, no archivo. Necesita
compuerta de entrada, política de desalojo y presupuesto — no "meter todo".

### 2.7 Memoria procedural

Los ganglios basales aprenden secuencias y las **empaquetan en hábitos**
(Graybiel, 2008). Lo que empezó como acción controlada termina como chunk
automático. Aprendizaje por refuerzo: error de predicción de recompensa.

**Implicación:** las "habilidades" de un agente (playbooks, rutas de herramientas,
heurísticas de debugging) son un tipo de memoria distinto del conocimiento
declarativo, con su propia estructura: disparador, pasos, estadísticas de éxito
y versión.

### 2.8 Emoción y saliencia

La amígdala modula la consolidación de lo emocionalmente relevante (McGaugh,
2004). No guarda el recuerdo: le pone una etiqueta que decide cuánto se refuerza.

### 2.9 Taxonomía de los sistemas de memoria

Squire (2004) ordena la memoria en dos grandes ramas con circuitos distintos:

```
Memoria declarativa (explícita)
├── Episódica   → hipocampo + lóbulo temporal medial
└── Semántica   → corteza temporal y asociativa

Memoria no declarativa (implícita)
├── Procedimental (habilidades) → ganglios basales
├── Priming perceptual          → neocorteza
├── Condicionamiento clásico    → amígdala / cerebelo
└── No asociativo (habituación) → vías reflejas
```

No son "niveles" de la misma cosa: son sistemas con sustratos, dinámicas y
patologías propias. Un amnésico puede perder episodios y conservar habilidades.

**Implicación:** un solo índice vectorial mezcla tipos de memoria que el cerebro
mantiene separados. Conocimiento, episodios, procedimientos y miedos necesitan
estructuras y políticas distintas.

### 2.10 Plasticidad sináptica: la fuerza tiene historia

- **Potenciación a largo plazo (LTP)** (Bliss y Lømo, 1973): la coactivación
  repetida fortalece la sinapsis.
- **Depresión a largo plazo (LTD)**: el patrón opuesto la debilita.
- **Plasticidad dependiente del tiempo de espiga (STDP)** (Bi y Poo, 1998): el
  orden temporal importa; antes-después fortalece, después-antes debilita.
- **Metaplasticidad**: la historia previa cambia la facilidad para plasticidad
  futura.
- **Etiquetado sináptico** (Frey y Morris, 1997): una marca local permite que
  una señal global convierta un cambio débil en duradero.

**Implicación:** el peso de una asociación no es un booleano, es una función de
la historia (co-ocurrencias, orden, resultado). Y la plasticidad tiene techo:
sin metaplasticidad, el sistema oscila entre rigidez y caos.

### 2.11 Mapas cognitivos: generalizar es navegar estructura

- **Células de lugar** (O'Keefe y Dostrovsky, 1971) y **células de rejilla**
  (Moser y Moser): el hipocampo representa el espacio como un mapa.
- **Mapa cognitivo** (Tolman, 1948): no es una lista de rutas, es una
  representación relacional que permite atajos.
- **Mapas de conocimiento** (Behrens et al., 2018): el mismo mecanismo soporta
  generalización entre tareas con estructura compartida; el hipocampo construye
  mapas de relaciones, no solo de lugares.
- **Replay y planificación** (Pfeiffer y Foster, 2013): el hipocampo simula
  trayectorias futuras reutilizando secuencias.

**Implicación:** un grafo de recuerdos debe capturar **relaciones** (causa,
antes/después, parte/todo), no solo cercanía semántica. La transferencia entre
dominios ocurre cuando dos problemas comparten estructura y el sistema puede
navegar de uno a otro.

### 2.12 Sueño: seleccionar, no copiar

- **Ondas lentas + husos + ripples**: coordinación hipocampo–corteza durante el
  sueño de ondas lentas (Buzsáki, 2015).
- **Bucle cortico-hipocampal-cortical** (Rothschild, Eban y Frank, 2017):
  reactivación y transferencia de información.
- **Triaje de memoria** (Stickgold y Walker, 2013): el sueño no copia todo;
  **selecciona**, integra y generaliza. Decide qué se queda, qué se transforma y
  qué se descarta.
- **REM**: integración asociativa y reconfiguración; no solo "descanso".

**Implicación:** la consolidación ideal no es un resumen del día. Es un proceso
de selección con criterios (saliencia, novedad, utilidad futura), que además
prueba generalizaciones y descarta lo que no encaja.

### 2.13 Dinámica de engramas: el olvido como accesibilidad

- **Asignación de engramas** (Han et al., 2007): no todas las neuronas compiten
  igual; la excitabilidad y CREB deciden quién entra en la huella.
- **Olvido como plasticidad adaptativa** (Ryan y Frankland, 2022): olvidar no es
  borrar la huella, es cambiar su **accesibilidad**. La memoria puede seguir ahí
  y no poder recuperarse.
- **Neurogénesis adulta y olvido** (Akers et al., 2014): integrar neuronas nuevas
  degrada recuerdos viejos; el olvido es el precio de la plasticidad.
- **Decaimiento vs. interferencia** (Hardt, Nader y Nadel, 2013): ambas cosas
  ocurren; la pregunta es cuándo domina cada una.

**Implicación:** el olvido debe implementarse como **cambio de estado de
recuperación** (peso, claves, contexto), no como `DELETE`. Eso permite archivar,
auditar y, a veces, recuperar lo "olvidado" con la clave correcta.

### 2.14 Memoria, yo y futuro

- **Memoria constructiva** (Schacter y Addis, 2007): recordar y imaginar el
  futuro usan la misma maquinaria; la memoria sirve para simular, no solo para
  archivar.
- **Sistema de memoria del yo** (Conway, 2005): la identidad es una narrativa
  jerárquica que filtra qué se recuerda y cómo.
- **Pensamiento episódico futuro**: proyectar escenarios pasados a situaciones
  nuevas es la base de la planificación.

**Implicación:** un agente sin narrativa de sí mismo no puede decidir qué es
relevante. Un "diario de identidad" (decisiones, valores, compromisos) es tan
parte de la memoria como el índice técnico.

### 2.15 Neurobiología de lo social

- **Hipótesis del cerebro social** (Dunbar, 1998): el tamaño del neocórtex
  correlaciona con el tamaño del grupo en primates; gran parte del cerebro se
  dedica a gestionar relaciones.
- **Memoria social**: rostros, voces, reputaciones e historias se almacenan con
  carga afectiva y se recuperan por pistas sociales.
- **Oxitocina y vasopresina**: modulan confianza, reconocimiento y sesgo
  endogrupal (Kosfeld et al., 2005; De Dreu et al., 2010).

**Implicación:** la memoria de personas/agentes (quién es confiable, quién falló,
quién sabe qué) es un sistema propio, no un atributo de los hechos técnicos.

### 2.16 Decisión: modelo vs. hábito

- **Model-based vs. model-free** (Daw et al., 2011): el cerebro combina un
  control deliberativo (simula consecuencias) con un control habitual (responde
  a estímulos). El estrés y la práctica inclinan la balanza hacia el hábito.
- **Control prefrontal** (Miller y Cohen, 2001): la corteza prefrontal mantiene
  metas y sesga la competición entre representaciones.
- **Hábitos** (Balleine y Dickinson; Graybiel, 2008): secuencias que se
  automatizan y dejan de ser sensibles a la recompensa inmediata.

**Implicación:** un agente necesita ambos modos: deliberación para lo nuevo y
procedimientos automáticos para lo repetido. El riesgo es que el hábito se
ejecute cuando la situación cambió; de ahí la importancia de la validez temporal.

## 3. Neuromoduladores como canales de control

No hacen falta neuronas simuladas para usar su lógica. Cada neuromodulador es una
señal global que cambia *qué se codifica, cuánto se consolida y qué se recupera*.

| Sistema | Señal biológica | Efecto en memoria | Canal de diseño |
|---|---|---|---|
| Dopamina | Error de predicción de recompensa (Schultz, Dayan y Montague, 1997); novedad; tagging sináptico (Frey y Morris, 1997; Redondo y Morris, 2011) | Refuerza lo que predice mejor de lo esperado; habilita LTP tardía | `reward` + `novelty`: prioridad de consolidación |
| Noradrenalina | Arousal, sorpresa; locus coeruleus | Potencia recuerdos emocionales | `surprise`: boost de codificación |
| Acetilcolina | Modo codificar vs. modo recuperar (Hasselmo, 1999) | Cambia la dinámica del hipocampo según la tarea | `mode`: encode vs recall |
| Serotonina | Inhibición conductual, paciencia; modulación difusa | Papel modulador, no interruptor (C) | `patience`: umbral para actuar/consolidar |
| Oxitocina | Vínculo social, confianza (Kosfeld et al., 2005); sesgo endogrupal (De Dreu et al., 2010) | Prioriza lo socialmente relevante | `social`: peso de recuerdos de otros agentes |
| Cortisona | Estrés agudo moderado facilita; crónico daña (Joëls et al., 2006) | Curva en U invertida | `threat`: proteger y priorizar lo peligroso |

**Implicación:** un vector de saliencia de 5–6 dimensiones, calculado al
codificar, que module consolidación, decaimiento y ranking de recuperación. Es
la pieza que convierte "guardar todo" en "guardar lo que importa".

La noradrenalina merece un matiz: la **teoría de ganancia adaptativa** (Aston-Jones
y Cohen, 2005) propone que el locus coeruleus regula el equilibrio entre
exploración y explotación. No es solo "arousal": es una señal de control que
decide si el sistema se abre a información nueva o se concentra en la tarea
actual. En un agente, ese canal puede modular la tasa de exploración del
retrieval y la probabilidad de aceptar un esquema nuevo.

## 4. Principios computacionales derivables

1. **Dos velocidades.** Rápido y específico arriba; lento y general abajo.
2. **Índice, no copia.** El recuerdo episódico apunta a piezas; recuperar
   reensambla.
3. **Separar antes de asociar.** Deduplicación y asociación son operaciones
   distintas.
4. **Replay intercalado.** La consolidación offline extrae estructura de
   episodios mezclados, no de un solo tema.
5. **El esquema acelera.** Lo que encaja con un marco previo se consolida antes.
6. **Recuperar modifica.** Reconsolidación y práctica de recuperación.
7. **Olvidar es funcional.** Decaimiento selectivo, no basura acumulada.
8. **Saliencia global.** Pocos canales moduladores bien elegidos valen más que
   cien reglas locales.
9. **La emoción etiqueta.** El fallo y la amenaza se recuerdan distinto.
10. **Límite de memoria de trabajo.** El contexto se administra, no se llena.
11. **La fuerza tiene historia.** Los pesos reflejan co-ocurrencia, orden y
    resultado; no son etiquetas.
12. **Generalizar es navegar estructura.** La transferencia ocurre entre
    problemas que comparten forma, no entre textos parecidos.
13. **Consolidar es seleccionar y abstraer.** No es copiar; es decidir qué
    merece pasar y en qué forma.
14. **Olvidar es cambiar accesibilidad.** Archivar, no borrar; regular claves,
    no destruir.
15. **La memoria sirve para simular el futuro.** Recordar es ensayar escenarios,
    no reproducir películas.
16. **Lo social es memoria de primer orden.** Personas, roles y confianza no son
    metadatos: son contenido.

### Límite de la analogía (revisión mayor)

La teoría CLS es evidencia de que el cerebro usa dos velocidades; **no** es
evidencia de que un almacén episódico externo + un job de consolidación mejoren a
un LLM. En el cerebro, consolidar cambia circuitos y representaciones; en un
agente con pesos congelados, cambia artefactos. Son fenómenos distintos.

Además, la consolidación no es solo lenta: la congruencia con esquemas previos
permite una vía rápida (Tse et al., 2007; van Kesteren et al., 2012). La analogía
de "dos velocidades" es una hipótesis de diseño, no una ley.

Para afirmar que la traducción funciona haría falta un experimento L3: comparar
la arquitectura contra un almacén único con buen retrieval, con presupuesto
igualado. Eso no se ha hecho.

## 5. Qué NO copiar

- **Simulación de spiking como sustrato de memoria.** El cerebro usa spikes; un
  LLM no los lee. Simular neuronas de verdad es un proyecto de neurociencia
  computacional, no una capa de memoria para agentes. (La neuromórfica tiene su
  lugar en hardware de bajo consumo, no aquí.)
- **Un homúnculo que decide.** Nada de "el módulo central elige". Las políticas
  deben ser locales y composables.
- **Consolidarlo todo.** La consolidación es cara y selectiva; si todo se
  promueve, el sistema se vuelve ruido.
- **Plasticidad sin estabilidad.** Aprender sin proteger lo aprendido produce
  interferencia catastrófica (ver doc 06).
- **"El cerebro recuerda, entonces el agente debe recordar como humano".** La
  analogía es de *función*, no de implementación. Cada mecanismo paga su costo
  con una ablación.

## 6. Preguntas abiertas

- ¿Cuánta consolidación es óptima para un agente que opera en sesiones de horas,
  no en días? El ciclo circadiano humano no aplica; hay que inventar el "sueño".
- ¿La separación de patrones se resuelve con umbral de similitud o hace falta un
  índice estructural?
- ¿El olvido debe ser lógico (borrar) o probabilístico (peso que decae)? La
  evidencia biológica apoya lo segundo; la ingeniería prefiere lo primero por
  auditabilidad.
- ¿Se puede medir "saliencia" sin un LLM juez? Si depende de un LLM, el costo por
  escritura se dispara.
