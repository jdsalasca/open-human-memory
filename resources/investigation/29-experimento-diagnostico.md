# 29 — Experimento diagnóstico: memoria, selección, procedimiento o abstracción

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

## 6.1 Resultados del Prototipo 002 (sin filtración)

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
## 6. Implementación mínima

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
