# Open Human Memory

Investigación abierta sobre memoria para agentes: qué puede aprender un sistema
de su experiencia, qué puede justificar y cómo evitar que sus errores se
conviertan en certezas permanentes.

**Estado:** programa de investigación con un **diagnóstico ejecutable**. No hay
producto todavía; hay un harness mínimo para decidir qué capa importa antes de
construir otra arquitectura.

## Inicio rápido

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m ohmem.experiment --train 200 --eval 50
```

En Windows PowerShell:

```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests -v
python -m ohmem.experiment --train 200 --eval 50
```

El harness compara cinco condiciones (sin memoria, retrieval, oráculo,
procedimiento y abstracción) en tres distribuciones (instancias nuevas, familias
nuevas con la misma estructura y familias estructuralmente nuevas). Es un
instrumento sintético, no un benchmark de LLM.

Licencia: MIT (`LICENSE`).

## La pregunta

> ¿Puede un agente acumular conocimiento procedimental durante meses,
> transferirlo entre modelos y mejorar sin reentrenar el LLM, sin convertir
> errores del pasado en conocimiento canónico?

La respuesta corta: **sí hay evidencia parcial de que se puede acumular y
transferir; no hay evidencia de que se pueda hacer durante meses con deriva real
ni de que la validación causal esté resuelta.** El programa estudia ambas cosas y,
sobre todo, la corrección.

## Primer resultado (sintético)

Prototipo 001 compara sin memoria, retrieval, oráculo, procedimiento y
abstracción en tres distribuciones. Media de 3 semillas:

| Condición | D1 | D2 | D3 |
|---|---|---|---|
| A sin memoria | 0.240 | 0.507 | 0.000 |
| B retrieval | 0.980 | 0.993 | 0.027 |
| C oráculo | 1.000 | 1.000 | 0.000 |
| D procedimiento | 0.920 | 1.000 | 0.007 |
| E abstracción | 0.487 | 0.000 | 0.000 |

Es un instrumento sintético, no un benchmark de LLM. Detalles, resultados crudos
y reproducción en
[`prototipo-001-diagnostico/`](resources/investigation/prototipo-001-diagnostico/).

## Por dónde empezar

| Documento | Para qué |
|---|---|
| [24-programa-de-investigacion-v2.md](resources/investigation/24-programa-de-investigacion-v2.md) | Horizontes, hipótesis y experimento diferencial A–E |
| [28-programa-de-competencia.md](resources/investigation/28-programa-de-competencia.md) | Programa v3: continuidad, competencia y expansión |
| [29-experimento-diagnostico.md](resources/investigation/29-experimento-diagnostico.md) | El experimento que decide qué capa importa |
| [prototipo-001-diagnostico/](resources/investigation/prototipo-001-diagnostico/) | Resultados, reproducibilidad y lectura crítica |
| [15-respuesta-directa.md](resources/investigation/15-respuesta-directa.md) | La respuesta corta a la pregunta central |
| [21-revision-critica-fuentes.md](resources/investigation/21-revision-critica-fuentes.md) | Qué evidencia sostiene qué, en dos ejes |
| [23-marco-de-validez.md](resources/investigation/23-marco-de-validez.md) | Fenómeno, traducción y ventaja comparativa |
| [25-protocolo-fuentes-primarias.md](resources/investigation/25-protocolo-fuentes-primarias.md) | Cómo se buscan y evalúan las fuentes |
| [27-plan-de-implementacion.md](resources/investigation/27-plan-de-implementacion.md) | Qué se implementa y qué no (JANUS-C) |
| [precedentes/](resources/investigation/precedentes/) | Qué se ha intentado, incluidos los competidores 2026 |
| [papers/](resources/investigation/papers/) | CUMULUS (EN/ES), revisión v0.2 y JANUS v0.2 |

## Las tres líneas

1. **CUMULUS** — hipótesis de portabilidad: contratos procedurales agnósticos al
   modelo, auditoría ciega y enrutamiento por portabilidad. En revisión; su
   novedad amplia fue retirada.
2. **JANUS** — hipótesis de validación: memoria con identificabilidad declarada,
   sin prometer causalidad cuando no se puede estimar. En revisión.
3. **ESCM** — línea fundamental: memoria experimental y autocorrectiva, con
   incertidumbre, ignorancia, agenda de experimentos y anti-persistencia
   selectiva. Pendiente de experimento.

## Lo que este proyecto no afirma

- Que la biología justifique una arquitectura.
- Que CUMULUS o JANUS sean superiores sin evidencia comparativa.
- Que la memoria contrafactual sea un terreno inexplorado.
- Que persistir abstracciones siempre mejore al agente.
- Que la capa social mejore el aprendizaje por sí sola.

## Estructura

```
docs/plan.md                     rondas y criterios
resources/investigation/         investigación, precedentes, papers
```

## Repositorio

https://github.com/jdsalasca/open-human-memory

Documentos de trabajo, no arbitrados. La afiliación MIT es la declarada por el
autor humano y debe verificarse antes de un envío; la participación de IA debe
declararse conforme a las normas del venue.
