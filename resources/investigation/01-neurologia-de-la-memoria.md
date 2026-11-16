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
