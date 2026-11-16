# 03 — Organismos sociales: hormigas, abejas, termitas

## 1. Por qué una colonia es un buen modelo

Una colonia logra cognición colectiva sin ningún individuo inteligente. No hay
un jefe que sepa dónde está la comida: hay **reglas locales, señales que se
degradan y umbrales**. Es exactamente el tipo de arquitectura que un sistema de
agentes necesita: nadie tiene el contexto completo, pero el sistema recuerda.

La colonia es un computador hecho de cuerpos (Seeley, 2010). La pregunta de
diseño es qué parte de ese computador es memoria.

## 2. Estigmergia: memoria en el entorno

Grassé (1959) acuñó **estigmergia**: coordinación indirecta mediante trazas que
un individuo deja en el entorno y otro lee. La hormiga no le dice "ve por la
izquierda": deja feromona; la siguiente la sigue y refuerza.

Propiedades clave:

- **No hay destinatario.** La señal es pública y anónima.
- **Se refuerza con el uso.** Más tráfico → más feromona → más tráfico.
- **Evapora.** Sin refuerzo, la traza desaparece. Esto evita bucles muertos y
  permite corregir.

El experimento del doble puente (Goss et al., 1989; Deneubourg et al., 1990):
dos caminos a la comida, uno corto y uno largo. Al inicio ambos reciben tráfico;
el corto se completa antes, recibe más feromona por unidad de tiempo y termina
dominando. **Emergencia por feedback positivo + evaporación**, sin comparar
distancias.

**Implicación:** un "campo de feromonas" digital —trazas compartidas con fuerza
que decae y se refuerza con el uso— es un mecanismo de memoria colectiva barato
y robusto. Es el mismo principio que PageRank y que el cacheo por frecuencia.

## 3. División del trabajo por umbrales

Las obreras no tienen un rol fijo: tienen **umbrales de respuesta** distintos
(Bonabeau, Theraulaz y Deneubourg, 1996). Si la demanda de una tarea sube, más
individuos cruzan su umbral y se reasignan. La colonia regula la asignación sin
planificador.

**Implicación:** enrutar tareas por umbral (carga actual + especialización +
costo de cambio) en vez de por rol estático. Los agentes se reasignan solos
cuando la demanda cambia.

## 4. Quórum: decidir cuando hay suficiente

- **Hormigas del género *Temnothorax***: una exploradora que encuentra un nido
  aceptable lo "anuncia" llevando compañeras. Cuando el número de encuentros en
  el sitio supera un quórum, la colonia se muda (Pratt et al., 2002; Pratt,
  2005). No esperan unanimidad ni deciden por mayoría central.
- **Abejas**: los exploradores bailan la ubicación de sitios; la decisión de
  enjambrar ocurre cuando suficientes abejas visitan el mismo sitio (Seeley y
  Visscher, 2004). El quórum es un **mecanismo de confirmación distribuida**.

**Implicación:** una memoria no debería promoverse a "verdad del sistema" por un
solo episodio. El quórum de corroboración (N fuentes independientes, N usos
exitosos, N agentes) es un criterio de consolidación más robusto que un umbral de
similitud. Y es ajustable: más quórum = más precisión y más lentitud.

## 5. Enseñanza en insectos: el tandem running

Franks y Richardson (2006) mostraron que la hormiga *Temnothorax albipennis*
enseña: una experimentada guía a una novata paso a paso, esperando y corrigiendo.
La novata aprende la ruta más rápido que sola. Es uno de los pocos casos de
enseñanza en invertebrados.

**Implicación:** la enseñanza uno-a-uno con pausas y verificación es un
protocolo, no un chat. El que enseña espera confirmación; el que aprende ejecuta.

## 6. Abejas: el baile como broadcast

La danza de la abeja (von Frisch, 1967) codifica dirección y distancia; es una
señal simbólica que se transmite en un "sala de baile" donde otras la leen. No
es un mensaje punto a punto: es un **canal de difusión** con información
codificada.

**Implicación:** un canal de "descubrimientos" de alta saliencia (lo que
funcionó, lo que falló, lo que cambió) que se difunde al pod. Sin él, cada agente
redescubre lo mismo.

## 7. Termitas: construcción sin plano

Las termitas construyen montículos con reglas locales de depósito y respuesta a
gradientes. La estructura global no está representada en ningún individuo.

**Implicación:** la estructura del conocimiento puede emerger de reglas de
escritura locales (dónde enlazar, cuándo promover, cuándo archivar) sin un
esquema global predefinido. Útil para no diseñar una ontología rígida.

## 8. Lo que la colonia realmente computa

| Fenómeno | Regla local | Propiedad global |
|---|---|---|
| Doble puente | Depositar y seguir feromona | Selección del camino corto |
| División del trabajo | Umbral individual | Asignación óptima bajo demanda |
| Quórum | Contar encuentros | Decisión robusta y rápida |
| Baile | Codificar y difundir | Diseminación de información |
| Construcción | Reglas de depósito | Arquitectura sin plano |

Ninguna propiedad global está representada en un individuo. **La memoria del
sistema no está en un nodo: está en el protocolo.**

### Límite: el quórum no es verdad (revisión mayor)

El quórum de las hormigas selecciona un nido, no una proposición verdadera. En
agentes, cinco evaluadores con el mismo modelo, prompt, datos y verificador no
son cinco fuentes independientes: son una fuente con cinco etiquetas.

Antes de usar quórum como validación hay que:

- modelar la correlación entre evaluadores;
- exigir diversidad de modelo, herramienta o evidencia;
- separar consenso de exactitud;
- preferir verificación ejecutable cuando exista.

El quórum se mantiene como **hipótesis de coordinación**, no como criterio
epistémico.

## 9. Qué NO copiar

- **Feromona infinita.** Sin evaporación, el sistema se congela en la primera
  solución. El decaimiento es la mitad del mecanismo.
- **Quórum como unanimidad.** La colonia decide con suficientes, no con todos;
  exigir consenso total paraliza.
- **"Inteligencia de enjambre" como marca.** El término suele esconder
  optimización de parámetros. La parte útil aquí es la memoria distribuida, no
  el marketing.
- **Roles rígidos.** La división del trabajo es adaptativa; copiar castas fijas
  crea cuellos de botella.
- **Ignorar el costo de la señal.** Toda traza cuesta escritura y lectura; si el
  campo de feromonas es global, se convierte en un hotspot.

## 10. Preguntas abiertas

- ¿El campo de feromonas debe ser un grafo de recuerdos o un espacio de
  embeddings con densidad?
- ¿La evaporación se mide en tiempo, en número de lecturas o en ciclos de
  consolidación?
- ¿Cómo se evita que el feedback positivo amplifique un error temprano?
  (Respuesta biológica: exploración aleatoria y ruido. En agentes: inyección de
  diversidad.)
- ¿Cuántos agentes hacen falta para que el quórum sea informativo y no un
  simple contador?
