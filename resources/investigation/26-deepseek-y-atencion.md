# 26 — DeepSeek y la línea de atención: lo que cambia para la memoria

## 1. Por qué esta línea importa

La memoria de agentes no flota sobre el modelo: vive dentro de un presupuesto de
atención, caché KV, cómputo y latencia. Las decisiones arquitectónicas de
DeepSeek —MLA, DeepSeekMoE, atención nativa dispersa, GRPO, verificación con
código y Lean— cambian el costo y las posibilidades de la memoria.

Ignorarlas produce papers que razonan sobre "tokens" como si todos costaran lo
mismo y como si la ventana fuera el único límite.

## 2. La línea de atención

| Hito | Aporte | Implicación para memoria |
|---|---|---|
| Sutskever et al. (2014) | Seq2seq con estados fijos | La información comprimida se pierde; nace la necesidad de atención |
| Bahdanau et al. (2015) | Atención alineada | Acceso selectivo a la fuente, no un resumen fijo |
| Vaswani et al. (2017) | Self-attention | Contexto como conjunto de relaciones; costo cuadrático |
| Shazeer (2019), Ainslie et al. (2023) | MQA / GQA | El KV cache es el verdadero cuello de botella |
| Su et al. (2021) | RoPE | Posición relativa y extensión de contexto |
| Dao et al. (2022) | FlashAttention | El costo es de memoria/IO, no solo de FLOPs |
| Beltagy et al. (2020), Zaheer et al. (2020) | Atención dispersa | No todo token necesita atenderse |
| Katharopoulos et al. (2020) | Atención lineal | Alternativa al costo cuadrático |
| DeepSeek-V2 (2024) | MLA | Comprime K/V en un latente; −93,3% de KV cache, 5,76× throughput |
| DeepSeek NSA (2025) | Atención dispersa nativa y entrenable | Selección jerárquica de bloques; hasta 11,6× en decodificación a 64K |

**Lectura:** el contexto no es gratis ni homogéneo. La memoria externa compite
con una atención nativa cada vez más eficiente y selectiva. Su justificación no
es "caber", sino **elegir mejor que la atención**.

## 3. DeepSeek: arquitectura y aprendizaje

### 3.1 DeepSeekMoE

Dai et al. (2024) proponen segmentación fina de expertos y aislamiento de
expertos compartidos. El resultado: más capacidad total con menos cómputo activo
y mejor especialización.

**Analogía para memoria:** un Canon con "expertos compartidos" (conocimiento
común) y "expertos enrutados" (habilidades específicas) es más eficiente que un
almacén plano. El enrutamiento por dominio es el equivalente al router de
expertos.

### 3.2 DeepSeek-V2 y MLA

DeepSeek-V2 (2024) introduce Multi-head Latent Attention: comprime claves y
valores en un vector latente, reduce el KV cache 93,3% y aumenta el throughput
5,76× frente a DeepSeek 67B, manteniendo calidad.

**Implicación:** el costo de mantener contexto crece con la caché, no solo con
los tokens. Un sistema de memoria debe medir **costo por token × costo de KV ×
latencia**, no solo tokens.

### 3.3 DeepSeek-V3

DeepSeek-V3 (2024): 671B parámetros totales, 37B activos, MLA + DeepSeekMoE,
predicción multi-token (MTP), FP8 y balanceo sin pérdida auxiliar. Entrenado con
2,788M horas H800.

**Implicación:** la capacidad total no es la capacidad activa. La memoria
externa puede especializar sin activar todo el modelo; el enrutamiento importa.

### 3.4 DeepSeekMath y GRPO

Shao et al. (2024) introducen Group Relative Policy Optimization: elimina el
crítico y usa la recompensa media del grupo como baseline. Es la base de
DeepSeek-R1.

**Implicación para JANUS:** se puede entrenar una **política de uso de memoria**
(qué recuperar, qué saltar, cuándo consolidar) con GRPO y recompensas
verificables, sin tocar los pesos del LLM base.

### 3.5 DeepSeek-R1

DeepSeek-R1 (2025; Nature 645, 633–638) muestra que el razonamiento puede
incentivarse con RL puro y recompensas verificables, sin trayectorias humanas.
Emergen auto-verificación, reflexión y adaptación de estrategia. La clave:
**preguntas difíciles + verificador fiable + cómputo**.

**Implicación:** es la misma receta de JANUS: contrafactuales verificables,
preguntas difíciles y una política que aprende a usarlos.

### 3.6 DeepSeek-Coder y DeepSeek-Prover

DeepSeek-Coder (2024) entrena con repositorios completos y FIM; DeepSeek-Prover
(2024) usa Lean 4 para verificar pruebas y genera datos sintéticos a escala.

**Implicación:** los verificadores ejecutables (tests, proof checkers, SQL,
solvers) son los "modelos del mundo" más fiables para la memoria contrafactual.
COUNTERMEM ya lo explota; JANUS debe hacerlo con certificados de replay.

### 3.7 Native Sparse Attention

Yuan et al. (2025) proponen NSA: compresión gruesa + selección fina + ventana
local, entrenable de extremo a extremo. Reporta hasta 11,6× de speedup en
decodificación a 64K y mejoras en tareas de contexto largo.

**Implicación:** la atención nativa se vuelve selectiva. La memoria externa debe
aportar lo que la atención no puede: persistencia, procedencia, causalidad y
corrección.

## 4. Lo que DeepSeek no resuelve

- Memoria persistente entre sesiones.
- Transferencia procedural entre modelos.
- Asignación de crédito causal.
- Incertidumbre e ignorancia.
- Gobernanza de memoria compartida.

La eficiencia de atención mejora el **transporte**; no decide **qué merece
recordarse**.

## 5. Hipótesis derivadas

| # | Hipótesis | Métrica |
|---|---|---|
| HD1 | El valor de una memoria debe medirse por éxito por unidad de KV/cómputo, no por tokens | Costo por éxito con KV incluido |
| HD2 | MLA/NSA reducen costo pero no eliminan la necesidad de selección | Comparar atención nativa vs. atención + memoria |
| HD3 | GRPO puede entrenar una política de uso de memoria con recompensas verificables | Mejora de éxito/costo vs. política fija |
| HD4 | Los verificadores de código/Lean son los world models más fiables para contrafactuales | Tasa de verificación y daño |
| HD5 | El enrutamiento de memoria y el enrutamiento de expertos comparten estructura | Transferencia de políticas de routing |

## 6. Consecuencias para CUMULUS y JANUS

- **CUMULUS:** el Puente debe reportar costo por modelo incluyendo KV y latencia,
  no solo tokens. La portabilidad incluye eficiencia.
- **JANUS:** la política de uso puede entrenarse con GRPO sobre recompensas
  verificables; los verificadores de código/Lean son el sustrato natural.
- **Ambos:** la comparación contra atención nativa larga es obligatoria. Si el
  modelo puede atender 128K con NSA, la memoria externa debe demostrar que
  aporta más que "meter todo".

## 7. Lectura crítica

- MLA y NSA son avances de eficiencia, no de memoria. No confundir "contexto más
  barato" con "aprendizaje acumulativo".
- GRPO y R1 son entrenamiento con RL; nuestro uso es una analogía para una
  política externa, no una afirmación de que el modelo aprenda memoria.
- DeepSeek-Coder/Prover verifican código y pruebas, no decisiones arbitrarias.
  La cobertura de verificadores sigue siendo el cuello de botella.

## 8. Cierre

DeepSeek demuestra que la eficiencia se diseña en la arquitectura. La memoria de
agentes debería aprender la lección: no competir por tokens, sino por **valor por
unidad de cómputo**. La atención resuelve el acceso; la memoria debe resolver el
juicio.
