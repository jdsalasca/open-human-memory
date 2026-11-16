# 05 — Aprendizaje humano: qué hace que algo se quede

## 1. El hallazgo incómodo

La sensación de aprender no coincide con aprender. Releer y subrayar se sienten
productivos y producen poco; recuperar y espaciar se sienten difíciles y
producen retención. Casi todas las técnicas eficaces comparten una propiedad:
**introducen dificultad útil**.

Para un agente, la traducción es directa: si el sistema solo "relee" (resume,
recupera por similitud y mete al contexto), parecerá que aprende y no retendrá
nada. Si obliga a recuperar y a aplicar en condiciones distintas, retendrá.

## 2. Repetición espaciada

- Ebbinghaus (1885): la curva del olvido cae rápido y luego se aplana.
- Cepeda et al. (2006), meta-análisis de 254 estudios: distribuir la práctica en
  el tiempo produce retención muy superior a la práctica masiva.
- El intervalo óptimo crece con el horizonte de retención deseado.

**Implicación:** cada esquema o procedimiento necesita un **programador de
repasos** cuya distancia crece si el recuerdo se recupera con éxito y se acorta
si falla. No es un cron job genérico: es una cola de repaso por ítem.

## 3. Práctica de recuperación

Roediger y Karpicke (2006): recuperar información fortalece la huella más que
volver a estudiarla (efecto del test). El intento de recuperación, incluso
fallido, mejora el aprendizaje posterior.

**Implicación:** el sistema debe **preguntar antes de mostrar**. En la práctica:
al iniciar una tarea, recuperar candidatos y pedir confirmación/corrección; al
cerrar, generar preguntas de control. La recuperación es un evento de escritura
(reconsolidación), no solo de lectura.

## 4. Intercalado y variabilidad

Rohrer y Taylor (2007): mezclar tipos de problemas mejora la transferencia frente
a bloques del mismo tipo. Kornell y Bjork (2008) muestran que el intercalado se
siente peor y rinde mejor.

**Implicación:** la consolidación no debe procesar un solo dominio por lote.
Replay intercalado entre dominios produce esquemas más transferibles y reduce la
interferencia. (Esto también es lo que hace el hipocampo: reactiva secuencias
mezcladas.)

## 5. Dificultades deseables

Bjork y Bjork (2011): ciertas dificultades —espaciar, intercalar, recuperar,
variar el contexto, reducir pistas— mejoran la retención a largo plazo aunque
empeoren el desempeño inmediato.

**Implicación:** el sistema debe **degradar la ayuda gradualmente**. Primero
recuerda con pistas; luego sin ellas. Un agente que siempre recibe el contexto
completo nunca desarrolla memoria propia.

## 6. Práctica deliberada (con matices)

Ericsson, Krampe y Tesch-Römer (1993): la pericia se construye con práctica
focalizada en la debilidad, con feedback inmediato y repetición. La crítica de
Macnamara, Hambrick y Oswald (2014): la práctica deliberada explica una parte
significativa pero no toda la varianza; importan también la edad de inicio, la
calidad del entrenamiento y factores individuales.

**Implicación:** el agente debe recibir feedback sobre sus errores, no solo sobre
sus éxitos. Un sistema de memoria que registra "esto salió bien" sin registrar
"aquí fallé y por qué" no entrena nada.

## 7. Zona de desarrollo próximo y andamiaje

Vygotsky (1978): se aprende lo que está justo por encima del nivel actual, con
ayuda. Wood, Bruner y Ross (1976): el andamiaje es apoyo temporal que se retira.

**Implicación:** los agentes novatos necesitan un **andamiaje que se desvanece**:
plantillas, ejemplos resueltos y verificación, que se retiran a medida que el
agente demuestra dominio. Esto se puede implementar como nivel de ayuda por
dominio y por agente.

## 8. Carga cognitiva y chunking

- Sweller (1988): la memoria de trabajo es limitada; sobrecargarla impide
  aprender.
- Chase y Simon (1973): los expertos no tienen más memoria, tienen **chunks**
  más grandes. Ven patrones, no piezas.
- Ericsson y Kintsch (1995): la memoria de trabajo a largo plazo permite retener
  estructuras complejas con claves de recuperación.

**Implicación:** el presupuesto de contexto debe ser explícito y adaptativo. Y la
consolidación debe producir **chunks**: procedimientos comprimidos que ocupan
poco y activan mucho.

## 9. Codificación dependiente del contexto

Tulving y Thomson (1973): la recuperación depende de la coincidencia entre la
clave y el contexto de codificación. Craik y Lockhart (1972): el procesamiento
profundo (significado, conexiones) retiene más que el superficial.

**Implicación:** guardar el contexto de uso (tarea, dominio, agente, resultado)
junto al recuerdo, y recuperar con claves contextuales, no solo semánticas. Un
embedding sin contexto recupera lo parecido, no lo pertinente.

## 10. Sueño y consolidación

Rasch y Born (2013): el sueño consolidada memoria declarativa y procedural, con
replay e integración. La privación de sueño degrada la codificación.

**Implicación:** el "sueño" del sistema es una ventana de cómputo offline: sin
interrupciones, con replay, sin la presión de responder. No es un lujo; es donde
ocurre la consolidación.

## 11. Síntesis: el calendario del aprendizaje

| Técnica | Qué cambia | Cómo se implementa |
|---|---|---|
| Espaciado | Cuándo se repasa | Cola de repaso por ítem con intervalos crecientes |
| Recuperación | Cómo se repasa | Preguntar antes de mostrar; registrar aciertos/fallos |
| Intercalado | Qué se mezcla | Replay entre dominios, no por lotes |
| Dificultad deseable | Cuánta ayuda | Pistas decrecientes; contexto parcial |
| Feedback | Qué se corrige | Registrar error y causa, no solo éxito |
| Andamiaje | Cuánto se apoya | Nivel de ayuda por agente/dominio, con retiro |
| Chunking | Cómo se comprime | Playbooks y esquemas, no resúmenes |

## 12. Qué NO copiar

- **"Aprender estilos" (visual/auditivo).** No hay evidencia sólida de que
  adaptar el formato al estilo mejore el aprendizaje. No entra.
- **Gamificación superficial.** Puntos y rachas no son consolidación.
- **Practice makes perfect.** La repetición sin feedback ni variación consolida
  errores.
- **Curva de olvido como ley exacta.** Es un modelo; los parámetros se calibran
  por dominio.
- **Asumir que un LLM "aprende" al leer.** Leer es codificar; sin recuperación y
  consolidación, no hay retención.

## 13. Preguntas abiertas

- ¿Cómo se define "repaso exitoso" para un agente: recuperó el dato, lo aplicó
  bien, o ambos?
- ¿El espaciado debe medirse en tiempo real o en número de tareas?
- ¿Cómo se evita que el andamiaje se retire demasiado pronto y produzca fallos
  costosos?
- ¿La dificultad deseable tiene un límite de seguridad en tareas destructivas?
