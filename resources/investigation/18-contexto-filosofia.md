# 18 — ¿Qué es el contexto? Una cartografía filosófica

## 1. La palabra y la intuición

"Contexto" viene del latín *contexere*: tejer juntos. No es lo que está alrededor
como un marco pasivo, sino lo que se **trama** con el acto para que el acto
signifique algo. La intuición ingenua —contexto como contenedor de texto— es
técnicamente cómoda y filosóficamente pobre.

Este documento no busca una definición única. Busca un mapa de posiciones que
permita diseñar mejores sistemas: si el contexto es relacional, entonces
"meter más texto" es una solución equivocada al problema equivocado.

## 2. Contexto como horizonte (hermenéutica)

Heidegger (1927) describe el *ser-en-el-mundo*: nunca percibimos objetos aislados,
sino dentro de una totalidad de utensilios y prácticas. El martillo se entiende
como "para martillar" antes de ser un objeto con propiedades. El contexto es la
**totalidad remisiva** que hace que algo sea utilizable.

Gadamer (1960) habla de **horizonte**: el conjunto de prejuicios y expectativas
desde el que comprendemos. Comprender es una "fusión de horizontes"; no se sale
del propio para entrar en el otro, se produce un encuentro.

**Implicación:** el contexto de un agente no es solo el prompt; es el conjunto de
prácticas, herramientas y expectativas desde el que interpreta la tarea. Un
agente sin mundo (sin affordances ni normas) tiene tokens, no contexto.

## 3. Contexto como juego de lenguaje (Wittgenstein)

Wittgenstein (1953) sostiene que el significado de una palabra es su uso en un
**juego de lenguaje**, y que los juegos se apoyan en una **forma de vida**. No hay
significado privado independiente de la práctica.

**Implicación:** las instrucciones de un agente no significan por sí solas; su
sentido depende de la práctica compartida (el dialecto del pod, las convenciones
del proyecto). Un agente nuevo que no comparte la forma de vida interpreta mal
aunque reciba el texto correcto.

## 4. Contexto como terreno común (pragmática y semántica formal)

- **Stalnaker (1978)** introduce el **common ground**: el conjunto de
  presuposiciones que los interlocutores comparten y actualizan en la
  conversación.
- **Lewis (1979)** describe la conversación como un juego de puntuación: las
  afirmaciones ajustan el terreno común, y las presuposiciones pueden acomodarse.
- **Kaplan (1989)** distingue el **contexto de la enunciación** (quién, cuándo,
  dónde) de las circunstancias de evaluación; los indexicales ("yo", "aquí",
  "ahora") dependen del contexto.

**Implicación:** el contexto de un agente incluye lo que el usuario y el sistema
dan por sentado. Si el agente no comparte ese terreno, responde a una pregunta
distinta de la que se hizo. La memoria compartida es, en gran parte, terreno
común.

## 5. Contexto como relevancia (teoría de la relevancia)

Sperber y Wilson (1986) definen la comprensión como la búsqueda del máximo
**efecto cognitivo** con el mínimo **esfuerzo de procesamiento**. El contexto no
es todo lo disponible: es el subconjunto de supuestos que se selecciona para que
el enunciado sea relevante.

**Implicación:** el contexto óptimo no es el más completo, sino el que maximiza
efectos útiles por unidad de costo. Es una definición económica, no enciclopédica.

## 6. Contexto como marco y modelo de situación

- **Fillmore (1982)** propone la **semántica de marcos**: comprender una palabra
  activa un marco de roles y escenas (comprar activa comprador, vendedor, precio,
  mercancía).
- **van Dijk y Kintsch (1983)** distinguen el texto del **modelo de situación**:
  el lector construye una representación del mundo descrito, no solo de las
  palabras.
- **Goffman (1974)** analiza los **marcos** de la interacción: qué está pasando,
  qué rol tiene cada uno, qué es aceptable.

**Implicación:** un agente necesita un modelo de situación (qué entidades, qué
roles, qué está en juego), no solo una secuencia de oraciones.

## 7. Contexto como affordance y enacción

Gibson (1979) define las **affordances** como las posibilidades de acción que el
entorno ofrece a un organismo. Varela, Thompson y Rosch (1991) y Noë (2004)
sostienen que la cognición es **enactiva**: el significado surge del acoplamiento
sensorimotor, no de representaciones internas aisladas.

**Implicación:** el contexto de un agente incluye lo que puede hacer con sus
herramientas. Un entorno sin affordances claras es un contexto pobre, aunque
tenga mucho texto.

## 8. Contexto como mente extendida y cognición distribuida

Clark y Chalmers (1998) argumentan que los artefactos externos pueden formar
parte del sistema cognitivo (la libreta, el teléfono, el archivo). Hutchins
(1995) muestra que la cognición se distribuye entre personas, artefactos y
prácticas (la navegación de un barco).

**Implicación:** la memoria y el contexto de un agente no terminan en su ventana.
El repositorio, los documentos, las convenciones y las herramientas son parte
del sistema. Diseñar contexto es diseñar el entorno cognitivo.

## 9. Contexto como campo, habitus y discurso

- **Bourdieu (1980)**: el **habitus** es un sistema de disposiciones que orienta
  la acción; el **campo** es el espacio de posiciones y capitales. El contexto no
  es neutral: está estructurado por poder y trayectoria.
- **Foucault (1969)**: el **discurso** define qué se puede decir, quién puede
  decirlo y desde qué posición. El contexto incluye las reglas de formación del
  saber.

**Implicación:** en un sistema multi-agente, el contexto incluye jerarquías,
permisos y reglas de quién puede escribir qué. Ignorarlas produce memoria
"objetiva" que en realidad reproduce el poder del que escribe más.

## 10. Contexto como situación social de aprendizaje

Lave y Wenger (1991) muestran que el aprendizaje es situado: ocurre en una
comunidad de práctica, con un repertorio compartido y una identidad. El contexto
no es un decorado; es la práctica en la que el aprendiz participa.

**Implicación:** un agente nuevo no aprende solo con documentos; aprende
participando periféricamente en tareas reales con el dialecto y las normas del
pod.

## 11. Síntesis: cuatro dimensiones del contexto

| Dimensión | Pregunta | Fuente filosófica |
|---|---|---|
| Informacional | ¿Qué reduce la incertidumbre sobre la tarea? | Shannon; Sims; Sperber y Wilson |
| Material | ¿Qué puedo hacer con esto? | Gibson; Heidegger; Noë |
| Social/normativa | ¿Qué se da por sentado y qué está permitido? | Stalnaker; Lewis; Bourdieu; Foucault |
| Histórica | ¿De dónde viene y qué ha pasado antes? | Gadamer; Hutchins; Clark y Chalmers |

El contexto es la intersección de las cuatro. Un prompt solo cubre una parte de
la primera.

## 12. Definición operativa para agentes

> Contexto es el conjunto de condiciones —información, affordances, normas y
> historia— que hacen diferencia en la interpretación y el éxito de una acción;
> computacionalmente, el conjunto mínimo de representaciones que maximiza el
> éxito esperado bajo un presupuesto de tokens y un costo de recuperación.

Esta definición es funcional y falible: no dice qué es el contexto "en sí", sino
qué debe incluir un sistema para actuar con sentido.

## 13. Implicaciones para el diseño

1. **El contexto no es el prompt.** Es el prompt más el mundo, las normas y la
   historia.
2. **El terreno común es memoria.** Lo que el agente comparte con el usuario y
   el pod debe explicitarse.
3. **Las affordances son contexto.** Un agente sin herramientas claras no tiene
   contexto de acción.
4. **La relevancia es económica.** Seleccionar supuestos, no acumular texto.
5. **El poder es contexto.** Quién escribe, quién valida y quién es citado
   afecta lo que el sistema "sabe".
6. **La historia es contexto.** La procedencia y la validez temporal son parte
   del significado.

## 14. Límites de este mapa

- La filosofía no produce un algoritmo; produce criterios para evaluar diseños.
- Hay tradiciones incompatibles (hermenéutica, analítica, crítica). No se
  sintetizan sin pérdida.
- El riesgo de sobre-teorizar es real: un agente no necesita a Gadamer para
  responder un ticket. Necesita, eso sí, un contexto que no confunda el mapa con
  el territorio.
- La analogía entre contexto humano y contexto de LLM es funcional, no
  ontológica.

## 15. Preguntas abiertas

- ¿Puede un agente tener "mundo" sin cuerpo ni práctica?
- ¿El terreno común se puede representar explícitamente o solo se infiere?
- ¿Cómo se detecta que el agente interpretó la tarea desde un marco equivocado?
- ¿La relevancia es una propiedad del contexto o de la tarea?
- ¿Qué parte del contexto es universal y qué parte es específica de una forma de
  vida?
