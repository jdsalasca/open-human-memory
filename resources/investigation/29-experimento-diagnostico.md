# 29 - Experimento diagnóstico: memoria, selección, procedimiento o abstracción

> **Actualizado 2026-11-16.** Los resultados de este diagnóstico están corregidos
> por `docs/errata-006b.md` y `prototipo-004-validez/`. Lectura vigente: el 002 es
> un benchmark de solucionador; el 003 quedó retirado; el cuello de botella del
> agente real sigue abierto.

**Objetivo:** antes de construir otra arquitectura, identificar qué transformación
de la experiencia produce la mejora. No comparar cinco sistemas completos;
comparar cinco **tipos de información** con el mismo agente y presupuesto.

## 1. Condiciones

| Condición | Qué recibe el agente | Qué prueba |
|---|---|---|
| **A** | Sin memoria | Línea base |
| **B** | Recuperación automática por similitud | Valor del retrieval |
| **C** | Memoria correcta seleccionada por oráculo | Techo de la información |
| **D** | Procedimiento verificado derivado de experiencias | Valor de compilar |
| **E** | Abstracción conceptual derivada de varias experiencias | Valor de conceptualizar |

C es un **oráculo**: selecciona la experiencia que resuelve la tarea. No es
implementable; es un techo para saber si el problema es de selección.

## 2. Tres distribuciones de evaluación

| Distribución | Qué mide |
|---|---|
| **D1: nuevas instancias de familias conocidas** | Reutilización y robustez |
| **D2: familias nuevas con la misma estructura** | Transferencia composicional |
| **D3: familias estructuralmente nuevas** | Generalización amplia |

No son intercambiables. Un sistema puede ganar D1 y fallar D2/D3.

## 3. Métricas

### 3.1 Ganancia acumulativa

\[
G(n) = \mathbb{E}[S_{\text{memoria},n}] -
\mathbb{E}[S_{\text{control},n}]
\]

evaluada después de \(n = 100, 1{,}000, 5{,}000, 10{,}000\) experiencias, siempre
sobre tareas futuras no usadas en el aprendizaje.

Lo importante no es solo que \(G(n) > 0\), sino su **forma**: ¿crece, se estanca o
decae?

### 3.2 Costo descompuesto

\[
C = C_{\text{ejecución}} + C_{\text{recuperación}} + C_{\text{consolidación}} +
C_{\text{entrenamiento}} + C_{\text{verificación}} + C_{\text{mantenimiento}}
\]

Se reporta éxito por unidad de costo, no tokens por respuesta.

### 3.3 Métricas de daño

- errores persistentes;
- transferencia negativa;
- adopción de memoria envenenada;
- calibración de abstención;
- tiempo a abandono de una creencia refutada.

## 4. Hipótesis y lectura

| Resultado | Interpretación |
|---|---|
| C ≫ B | El cuello es la **selección**, no el almacenamiento |
| D ≫ C | Compilar procedimientos aporta más que recuperar casos |
| E ≫ D en D2/D3 | La abstracción conceptual es la fuente de transferencia |
| B ≈ A | La memoria no es el cuello en esa familia |
| G(n) decrece | El sistema acumula interferencia o errores |
| G(n) crece solo en D1 | Especialización, no expansión |

## 5. Controles

- Mismas tareas, mismo agente, mismo presupuesto.
- Oráculo C con acceso a la solución; B sin acceso.
- Semillas fijas y múltiples repeticiones.
- Particiones temporales: entrenamiento antes, evaluación después.
- Contaminación: D2/D3 no comparten vocabulario ni identificadores con D1.
- Costo del oráculo reportado aparte; no se compara como si fuera gratis.

## 6. Implementación mínima

### 6.1 Resultados del Prototipo 002 (sin filtración)

El Prototipo 001 se conserva como *smoke test*: tenía target leakage (el nombre de
la regla aparecía en la superficie). El 002 separa observación y solución, infiere
la regla desde tres ejemplos y añade composición.

Media de 3 semillas, 200 de entrenamiento, 50 de evaluación:

| Condición | D1 | D2 | D3 (composición) |
|---|---|---|---|
| MEM-A sin memoria | 0.240 | 0.507 | 0.000 |
| MEM-B retrieval | 0.553 | 0.513 | 0.027 |
| MEM-C oráculo | 1.000 | 1.000 | 1.000 |
| MEM-D primitiva | 1.000 | 1.000 | 0.000 |
| MEM-E composición | 1.000 | 1.000 | 1.000 |

Lectura: retrieval no basta cuando la regla está en los ejemplos y no en la
superficie; una primitiva inducida resuelve reglas simples; **la composición es
el discriminador**: MEM-D falla D3 porque su espacio de hipótesis no incluye
composiciones, MEM-E acierta porque las busca. Sigue siendo sintético: no prueba
un LLM ni descubrimiento abierto.
## 6.2 Prototipo 003: aprendizaje de macros (exploratorio, superado)

El 002 incluye `MEM-A0` (mismo solucionador composicional sin historial) y
`MEM-A0` empata con `MEM-E` en D1/D2/D3. Por tanto, **el 002 no demuestra
aprendizaje desde la memoria**: es un benchmark de solucionador.

El 003 encapsula programas de dos pasos repetidos como macros y las usa en
evaluación. Media de 3 semillas, con **tres programas D3 elegidos a mano**:

| Condición | D1 | D2 | D3 (profundidad 3) |
|---|---|---|---|
| NOLEARN | 1.000 | 1.000 | 0.000 |
| RANDOM (macros `reverse`/`negate`) | 1.000 | 1.000 | 0.000 |
| LEARNED | 1.000 | 1.000 | 1.000 |
| ABLATED (macros borradas) | 1.000 | 1.000 | 0.000 |

Ese 0 % frente a 100 % **no sobrevive a los controles**. El apartado 6.3 lo
documenta y lo retira.

## 6.3 Prototipo 004-A: los controles que faltaban

Protocolo congelado antes de medir (`prototipo-004-validez/protocolo-congelado.md`,
SHA-256 verificado por `reproduce.py`). Rejilla completa de **64 programas** de tres
primitivas, 3 semillas.

| Condición | Aciertos /64 | Candidatos | Candidatos por acierto |
|---|---|---|---|
| A0 sin memoria, prof. 2 | 33 (51,6 %) | 876 | 26,6 |
| **A1 sin memoria, prof. 3** | **64 (100 %)** | 1.761 | 27,5 |
| A2 azar, mismo lenguaje, prof. 2 | 50,7 (79,3 %) | 1.543 | 30,5 |
| **A3 macros aprendidas, prof. 2** | **54 (84,4 %)** | 1.448 | 26,8 |
| A4 macros aprendidas, prof. 3 | 64 (100 %) | 2.247 | 35,1 |

Conclusiones que se siguen de la tabla:

- **No hay capacidad nueva.** Sin historial y con profundidad 3 se resuelve el
  100 %. El límite de dos pasos lo impusimos nosotros.
- **La biblioteca es una compilación con pérdida:** 54/64. Gana 17,8 % de
  candidatos y pierde 15,6 pp de cobertura; por acierto el ahorro es 2,6 %.
- **Si se permite profundidad 3, la biblioteca encarece la búsqueda un 27,6 %.**
- **El control `RANDOM` del 003 estaba amañado.** Barrido de las 560 bibliotecas
  de 3 macros sobre los 16 pares del generador: 250/560 son perfectas en el D3 del
  003 (reproduce el 70,5 % de la auditoría) y **124/560 igualan o superan** a la
  aprendida en la rejilla.
- **Saturación en 6 experiencias.** Las 54 restantes no aportan nada.
- **Única ganancia defendible:** con presupuesto ≤ 40 candidatos por tarea, la
  biblioteca acierta más (78,1 % vs 70,3 %); desde 60, la búsqueda profunda la
  supera y termina en 100 %.

Lectura de conjunto: el 003 midió **un prior barato**, no una ampliación de
competencia. La hipótesis que sobrevive para el 005 es que las abstracciones
compiladas sirven cuando el cómputo por decisión está acotado, no como sustituto
del razonamiento.

## 6.4 Implementación mínima

El repositorio incluye un **diagnóstico sintético** en `src/ohmem/`:

- tareas con regla oculta y familia;
- memoria episódica;
- retrieval por similitud;
- oráculo;
- procedimiento y abstracción simulados;
- métricas por distribución y costo;
- CLI reproducible.

No es un benchmark de LLM. Es un **banco de pruebas del instrumento**: verifica
que el experimento distingue las condiciones antes de invertir en modelos.

## 6.5 Prototipo 005-A: el valor de la memoria es condicional

Documento: `prototipo-005-presupuesto/`. Exploratorio, no pre-registrado.

Tres mediciones que cambian la lectura del 004-A:

1. **La rejilla no tiene 64 problemas: tiene 14.** Firmando cada programa por su
   salida sobre 40 entradas, 64 sintaxis colapsan a 14 comportamientos. La
   biblioteca aprendida cubre 9/14; la búsqueda profunda, 14/14.
2. **La continuidad decide.** Con continuidad 1,0 (todo lo evaluado reutiliza
   motivos del entrenamiento), la biblioteca iguala el 100 % de cobertura con
   **41,8 % menos pasos ejecutados**. Con continuidad 0,0, el mismo trabajo rinde
   **22,1 pp menos**.
3. **Acumular no es aprender.** En un flujo de 96 tareas con deriva, congelar tras
   la primera fase da **76,0 % con 26,2 % menos trabajo** que no tener memoria;
   seguir aprendiendo baja a **67,0 %** y un tope con desalojo por uso a **64,6 %**.

Traducción para el problema del contexto: un artefacto de ocho macros sustituye a
96 episodios sin pérdida de precisión en este entorno, pero solo mientras el futuro
se parezca al pasado. La política que decide *cuándo* confiar en el artefacto sigue
sin existir: el primer intento la empeoró.

## 7. Qué decisión toma cada resultado

- Si **C ≫ B**: invertir en selección/activación, no en más almacenamiento.
- Si **D ≫ C**: invertir en compilación verificada (CUMULUS/JANUS).
- Si **E ≫ D en D2/D3**: invertir en descubrimiento conceptual (la frontera).
- Si **B ≈ A**: la memoria no es el cuello; buscar representación, herramientas o
  capacidad base.
- Si **G(n) decae**: invertir en anti-persistencia y corrección.

## 8. Límites

- El diagnóstico sintético no prueba nada sobre LLM; prueba que el diseño
  experimental separa las condiciones.
- El oráculo C no es implementable.
- La abstracción E simulada es una aproximación; la real requiere un motor
  conceptual.
- Los resultados negativos son útiles: evitan construir la capa equivocada.

## 9. Relación con el resto

- `28-programa-de-competencia.md`: marco.
- `08-hipotesis-y-experimentos.md`: protocolo principal.
- `27-plan-de-implementacion.md`: JANUS-C.
- `src/ohmem/`: harness mínimo.
