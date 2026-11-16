# 02 — Aprendizaje en mamíferos sociales

## 1. Por qué mirar aquí

Un agente LLM no tiene infancia ni manada, pero el problema que enfrenta —cómo
acumular conocimiento entre individuos y generaciones sin que se degrade— es
exactamente el que resolvieron los mamíferos sociales. La pregunta útil no es
"¿cómo aprende una orca?" sino "¿qué mecanismo de transmisión mantiene la
fidelidad de una técnica durante décadas?".

## 2. Aprendizaje social: el vocabulario mínimo

Whiten y van Schaik (2007) ordenan los mecanismos por fidelidad:

| Mecanismo | Qué copia | Fidelidad | Ejemplo |
|---|---|---|---|
| Realce de estímulo | Nada; solo se fija la atención en un objeto | Muy baja | Un mono ve a otro comer una fruta |
| Emulación | El resultado, no el método | Media | Abrir una caja por prueba y error tras verla abierta |
| Imitación | La secuencia de acciones | Alta | Copiar el gesto de pescar termitas |
| Enseñanza | El método, con costo para el que enseña | Muy alta | Orca varada intencionalmente; hormiga que guía |

La lección: **la fidelidad es el recurso escaso**. Un resumen con pérdida (la
compactación típica de contexto) es emulación de baja fidelidad: conserva el
resultado y pierde el método. Por eso los agentes "vuelven a ser estúpidos":
no perdieron los hechos, perdieron el procedimiento.

## 3. Primates: cultura sin escuela

- **Chimpancés**: Whiten et al. (1999) documentaron 39 patrones de conducta
  variables entre comunidades (pesca de termitas, cascado de nueces, hojas para
  beber) que no se explican por ecología ni genética. Son tradiciones.
- **Capuchinos**: tradiciones de uso de piedras y plantas medicinales; transmisión
  vertical y horizontal.
- **Sesgos sociales**: copiamos más a individuos de prestigio (Henrich y
  Gil-White, 2001), a la mayoría (conformismo) y a los exitosos. No copiamos al
  azar: el grupo filtra.
- **Enseñanza**: rara y costosa. La mayor parte del aprendizaje primate es
  observación, no instrucción.
- **Efecto trinquete** (Tomasello, 1999): la cultura humana acumula porque la
  transmisión es de alta fidelidad y cada generación modifica lo recibido. Sin
  fidelidad no hay acumulación, solo deriva.

**Implicación:** para que un agente mejore entre sesiones, la transmisión del
procedimiento debe ser de alta fidelidad y con capacidad de enmienda. Un
`summary` de la sesión anterior es emulación; un playbook versionado con
condiciones de uso es imitación.

## 4. Orcas: el caso más cercano a una "sociedad de especialistas"

### 4.1 Ecotipos: especialización ecológica con memoria propia

Las orcas del Pacífico Norte se dividen en ecotipos con dieta, comportamiento y
**repertorio vocal** distintos:

- **Residentes**: salmón; matrilineales; muy vocales; dialectos por matrilina
  (Ford, 1991).
- **Transitorias (Bigg's)**: mamíferos marinos; silenciosas al cazar; grupos
  pequeños.
- **Offshore**: peces y tiburones; ámbitos profundos.

Los ecotipos no son razas: son **culturas ecológicas** que se mantienen por
transmisión, no por aislamiento genético.

**Implicación:** un dominio no es una carpeta. Es un conjunto de políticas
(qué se guarda, cómo se recupera, qué vocabulario se usa) que se especializa con
el uso. Varios dominios pueden convivir sin contaminarse si tienen políticas
propias.

### 4.2 Dialectos

Los dialectos de las residentes son estables por matrilina y cambian
lentamente; Deecke, Ford y Spong (2000) documentaron cambios compatibles con
aprendizaje vocal y transmisión horizontal, no solo vertical.

**Implicación:** un "dialecto" computacional es un vocabulario compartido por
pod (nombres de proyectos, abreviaturas, decisiones canónicas). Sirve para dos
cosas: comprimir contexto y reconocer pertenencia. Un agente nuevo que no habla
el dialecto pierde recall aunque tenga los datos.

### 4.3 Menopausia y custodia del conocimiento

Brent et al. (2015): en las residentes, las hembras post-reproductivas lideran
los movimientos colectivos, **especialmente en años de escasez de salmón**. La
ventaja no es reproductiva: es conocimiento ecológico acumulado que el grupo
necesita cuando la situación es difícil.

**Implicación:** hace falta un rol de **custodio** —un agente (o perfil) que ya
no produce trabajo nuevo pero cura, valida y enseña el conocimiento crítico. En
términos de sistema: un índice curado y una función de "abuela" que responde
"¿qué hicimos la última vez que pasó esto?".

### 4.4 Enseñanza real

Guinet y Bouvier (1995) describieron en las orcas de Crozet la enseñanza
intencional de la técnica de varamiento para capturar pinnípedos: la madre
empuja a la cría a la playa y la recupera, graduando la dificultad. No es
observación pasiva; hay costo y ajuste al aprendiz.

**Implicación:** "enseñar" debe ser una operación explícita del sistema
(destilar un procedimiento para otro agente, con verificación de que el aprendiz
lo ejecuta), no un efecto secundario de compartir un log.

### 4.5 Fisión-fusión

Los grupos se separan y se reencuentran; la información viaja cuando se juntan.
No hay un registro central único.

**Implicación:** los pods no son estáticos. La memoria compartida necesita
mecanismos de sincronización al reencuentro (qué aprendiste mientras no
estábamos juntos).

## 5. Elefantes: la matriarca como base de datos

McComb et al. (2001): las matriarcas mayores reconocen mejor las llamadas de
depredadores y de individuos; los grupos con matriarcas viejas tienen ventaja
reproductiva. La memoria social dura décadas y es un activo del grupo.

**Implicación:** la memoria de relaciones (quién es confiable, quién falló, quién
sabe qué) es tan importante como la memoria de tareas. Un sistema que solo
guarda hechos técnicos pierde la capa social que hace usable el resto.

## 6. Patrones que se repiten en todas las especies

1. **La fidelidad de transmisión decide si hay acumulación.** Sin ella, cada
   generación reinventa.
2. **La especialización ecológica crea identidad.** Qué comes determina cómo
   hablas.
3. **Los ancianos son infraestructura.** El conocimiento difícil se concentra en
   pocos individuos longevos.
4. **La enseñanza es rara y costosa.** Se reserva para lo que no se aprende
   observando.
5. **La información viaja con el contacto.** La estructura social es el protocolo
   de red.
6. **El sesgo social filtra.** Prestigio, conformidad y éxito deciden qué se copia.

## 7. Qué NO copiar

- **Antropomorfismo.** Una orca no "sabe" que enseña; el sistema no necesita
  conciencia para tener custodia de conocimiento.
- **"Cultura" como adjetivo.** Si no se puede medir la fidelidad de transmisión
  (¿el aprendiz ejecuta igual?), no es cultura: es coincidencia.
- **Rigidez de roles biológicos.** La matrilina no se traduce en jerarquía
  permanente de agentes; se traduce en funciones de custodia y enrutamiento.
- **Copiar la escasez.** La menopausia es una solución evolutiva a un límite
  físico; un sistema digital no necesita jubilar agentes, necesita curar
  conocimiento. Se copia la función, no el mecanismo.

## 8. Preguntas abiertas

- ¿Cómo se mide fidelidad de transmisión entre agentes sin un juez humano?
- ¿Un dialecto debe ser un glosario explícito o emerger del uso?
- ¿Cuántos custodios necesita un pod para no convertirse en cuello de botella?
- ¿La especialización por dominio debe ser fija (ecotipo) o adaptativa (umbral de
  demanda)?
