# 12 — Aprendizaje humano vs. aprendizaje de máquinas

## 1. La comparación útil

Comparar "humanos vs. máquinas" suele producir dos errores: antropomorfizar la
máquina o reducir el humano a un algoritmo. La comparación útil es más estrecha:
**¿qué restricciones y qué estrategias de aprendizaje son propias de cada
sistema, y cuáles se pueden importar?**

La respuesta corta: los humanos ganan en eficiencia de muestra, causalidad,
transmisión social y olvido adaptativo; las máquinas ganan en escala,
persistencia, paralelismo y recall exacto. El proyecto no debe copiar el sustrato
humano, sino **la agenda** que a la máquina le falta: consolidación, olvido
selectivo y transmisión de alta fidelidad.

## 2. Las diferencias que la evidencia sostiene

### 2.1 Eficiencia de muestra e inducción

- Lake, Ullman, Tenenbaum y Gershman (2017) argumentan que las máquinas actuales
  aprenden "como palomas" (gradiente, gran data) y no "como humanos": falta
  construir modelos causales, apoyarse en teorías intuitivas y explotar la
  composicionalidad para aprender a aprender.
- Lake et al. (2015) mostraron aprendizaje de conceptos a partir de un solo
  ejemplo con inducción de programas bayesianos: un régimen de muestra que las
  redes profundas no igualan.
- Kühl (2022) comparó humanos y aprendizaje supervisado en la misma tarea:
  **los humanos aprenden patrones más rápido con pocos ejemplos**; las máquinas
  necesitan más instancias para alcanzar el mismo nivel (y en algunas tareas lo
  superan).

**Lectura:** la máquina no es "peor"; tiene otro sesgo inductivo. Su fuerza es la
escala; su debilidad es lo que no está en los datos.

### 2.2 Aprendizaje continuo e interferencia

- McCloskey y Cohen (1989) y French (1999): el aprendizaje secuencial en redes
  produce **interferencia catastrófica**; lo nuevo sobrescribe lo viejo.
- Kirkpatrick et al. (2017, EWC) y Rolnick et al. (2019, replay) son las
  soluciones estándar: proteger pesos importantes o repasar datos antiguos.
- Flesch et al. (2018, PNAS) compararon aprendizaje continuo en humanos y redes:
  los humanos estructuran y protegen mejor el conocimiento entre tareas.
- **Holton et al. (2025/2026, Nature Human Behaviour)** encontraron algo más
  incómodo: humanos y redes muestran **patrones similares** de transferencia e
  interferencia. Tareas parecidas producen más transferencia y más interferencia;
  tareas disímiles producen menos de ambas. Los "lumpers" humanos (generalizan)
  se parecen a redes en régimen *rich*; los "splitters" (individuación), a redes
  *lazy*.
- Pisupati y Niv (2022) y Kudithipudi et al. (2022) resumen el estado: la
  estabilidad–plasticidad es un problema compartido, y la biología aporta
  soluciones (replay, neuromodulación, neurogénesis, modularidad) que las
  máquinas aún no integran.

**Lectura:** la diferencia no es "humano no olvida"; es que el humano **regula**
el olvido y distribuye la representación. La interferencia es el precio de
generalizar, en ambos sistemas.

### 2.3 Composición, causalidad y teoría

Lake et al. (2017) proponen tres ingredientes para una inteligencia más humana:

1. **Modelos causales** que expliquen, no solo clasifiquen.
2. **Teorías intuitivas** (física, psicología) que estructuren el aprendizaje.
3. **Composición y aprendizaje-a-aprender** para generalizar con pocos datos.

Las máquinas actuales son fuertes en correlación y débiles en intervención y
contrafactual.

### 2.4 Aprendizaje social y cultura

Los humanos acumulan conocimiento por transmisión de alta fidelidad, enseñanza y
normas (Tomasello, 1999; Henrich, 2015). Las máquinas, hasta hace poco,
aprendían de datos, no de pares. Los agentes LLM ya muestran convenciones
emergentes (Ashery et al., 2025), pero no tienen un mecanismo probado de
transmisión acumulativa con fidelidad medida.

### 2.5 Sueño y consolidación

Los humanos consolidan offline (Rasch y Born, 2013; Stickgold y Walker, 2013).
Las máquinas entrenan y luego se congelan; su "memoria" en producción es contexto
y RAG. El cómputo offline (sleep-time compute, Lin et al., 2025) es un primer
paso, pero no es consolidación selectiva con olvido.

### 2.6 Olvido

- Humano: olvido adaptativo, interferencia, olvido inducido por recuperación
  (Anderson, Bjork y Bjork, 1994), olvido motivado (Anderson y Hanslmayr, 2014).
- Máquina: olvido catastrófico o ausencia total de olvido; el "unlearning" es un
  campo emergente.

### 2.7 Meta-cognición y calibración

Los humanos estiman su confianza y ajustan la búsqueda. Los LLM son
notoriamente mal calibrados. Un sistema de memoria que no distingue "lo sé" de
"lo vi una vez" no puede decidir cuándo consolidar.

## 3. Dónde convergen

- **Representaciones predictivas**: el cerebro y las redes profundas aprenden
  representaciones jerárquicas que predicen la entrada (Hassabis et al., 2017).
- **Refuerzo**: la dopamina como error de predicción (Schultz et al., 1997) y el
  RL comparten la misma matemática; el cerebro combina modelo y hábito (Daw et
  al., 2011; Gershman y Daw, 2017).
- **Replay**: hipocampo y *experience replay* cumplen una función análoga:
  reutilizar experiencias para estabilizar el aprendizaje.
- **Trade-off transferencia/interferencia**: Holton et al. (2026) muestran que
  no es una diferencia de sustrato, sino un compromiso computacional.
- **Modularidad**: la especialización por dominio reduce interferencia en ambos.

## 4. Tabla comparativa

| Dimensión | Humano | Máquina (LLM/red) | Sistema propuesto |
|---|---|---|---|
| Datos necesarios | Pocos, estructurados | Muchos, correlacionales | Híbrido: pocos + recuperación |
| Inducción | Causal, composicional | Estadística, asociativa | Grafo causal + embeddings |
| Continuo | Regulado, con olvido | Catastrófico o nulo | Ciclo de vida con consolidación |
| Interferencia | Alta entre tareas similares | Alta entre tareas similares | Políticas por dominio |
| Transmisión | Enseñanza, cultura | Datos, prompts, logs | `teach()` con fidelidad medida |
| Olvido | Adaptativo, reconstructivo | Ausente o destructivo | Decaimiento + archivo |
| Consolidación | Sueño, replay | Offline compute incipiente | Job de consolidación |
| Confianza | Calibrada (a veces) | Mal calibrada | Score por evidencia |
| Escala | Limitada | Masiva | Masiva + memoria curada |
| Identidad | Narrativa | Inexistente o de prompt | Diario de compromisos |

## 5. Qué significa para el diseño

1. **No competir con la escala.** La ventaja del sistema no es saber más, sino
   **recordar mejor lo que ya pasó**.
2. **Añadir el sesgo que falta.** Si la máquina es correlacional, el sistema debe
   imponer causalidad, procedencia y contraevidencia.
3. **Institucionalizar el olvido.** Donde la máquina no olvida o borra, el
   sistema decae y archiva.
4. **Enseñar, no volcar.** La transmisión de alta fidelidad es la diferencia
   entre cultura acumulativa y reinvención.
5. **Separa dominios.** La interferencia es el precio de compartir
   representaciones; aislar por dominio lo reduce.
6. **Calibrar la confianza.** Sin eso, la consolidación promueve ruido.
7. **Medir transferencia e interferencia juntas.** Como Holton et al.: mejorar
   una a costa de la otra no es progreso.

## 6. Lo que la comparación no resuelve

- No dice si un LLM "entiende". Esa pregunta es filosófica y no decide el
  diseño.
- No garantiza que los mecanismos humanos escalen a agentes; la analogía es
  funcional.
- No reemplaza la evaluación empírica: cada importación debe medirse contra una
  línea base simple.
- No implica que la arquitectura humana sea óptima; la evolución optimiza
  supervivencia, no rendimiento de tareas.

## 7. Agenda de investigación

- Benchmark de aprendizaje continuo con transferencia e interferencia medidas
  conjuntamente (inspirado en Holton et al.).
- Comparación de fidelidad de transmisión: resumen vs. playbook vs. enseñanza
  verificada.
- Calibración de confianza por dominio en agentes con memoria.
- Olvido selectivo con auditoría: ¿mejora precisión sin perder lo crítico?
- Consolidación offline con presupuesto fijo: ¿qué se elige y con qué criterio?

## 8. Preguntas abiertas

- ¿La eficiencia de muestra humana es alcanzable con recuperación estructurada,
  o requiere un sesgo inductivo distinto?
- ¿El trade-off transferencia/interferencia se puede romper con políticas por
  dominio, o solo se desplaza?
- ¿Un agente puede tener "teorías intuitivas" sin encarnación?
- ¿La cultura de agentes converge a normas útiles o a sesgos colectivos?
