# Revisión externa

**Fecha:** 16 de noviembre de 2026
**Objetivo:** someter el repositorio a una revisión científica externa antes de la
revisión por pares humana.

## Configuración

| Campo | Valor |
|---|---|
| Modelo | `gpt-6.1-terra` |
| `reasoning_effort` | `medium` |
| CLI | `codex-cli 0.169.0` |
| Cuenta | ChatGPT |
| Sandbox | `read-only` |
| Modo | `--ephemeral --skip-git-repo-check` |
| Salida | [`codex-gpt-6.1-terra-medium.md`](codex-gpt-6.1-terra-medium.md) |

**Nota de modelo.** El identificador correcto es `gpt-6.1-terra` (con punto).
`gpt-6-terra` no existe para cuentas ChatGPT. OpenCode se usa siempre con
`deepseek-v4.1-flash-1017`; Codex CLI, con `gpt-6.1-terra`.

La salida de `gpt-6-luna` se descartó por decisión del autor
(`archive/luna-max-descartada.md`, vacío) y no se usa.

## Informes

| Informe | Qué cubre |
|---|---|
| [`codex-gpt-6.1-terra-medium.md`](codex-gpt-6.1-terra-medium.md) | Revisión completa del repositorio (dictamen: rechazar en su estado actual) |
| [`validacion-lire-007.md`](validacion-lire-007.md) | Revisión adversarial de 007 y LIRE-001: explicaciones alternativas, hipótesis nuevas y tres experimentos priorizados |

## Qué se pidió

Una revisión tipo venue (NeurIPS/ACL) sobre el repositorio completo: consistencia
entre afirmaciones y evidencia, lógica de la teoría, reproducibilidad,
sobreafirmaciones, estructura y qué falta para pasar revisión por pares. El informe
debía incluir dictamen, fortalezas, debilidades con archivo y línea, errores
factuales, faltas de reproducibilidad, lista priorizada P0/P1/P2 y afirmaciones a
retirar.

## Reproducir

```powershell
Get-Content prompt.txt -Raw | codex exec --ephemeral --skip-git-repo-check `
  -s read-only -C "C:\Users\jdsal\Documents\Programming-personal\open-human-memory" `
  -m gpt-6.1-terra -c model_reasoning_effort="medium" `
  -o "resources\investigation\revision-externa\codex-gpt-6.1-terra-medium.md" -
```

## Resultado

**Dictamen: rechazar en su estado actual.** El revisor considera que el trabajo es
un programa de investigación con correcciones visibles, pero que no demuestra la
hipótesis principal y que la contribución defendible es metodológica. La respuesta
punto por punto está en
[`../../../docs/respuesta-a-revision-externa.md`](../../../docs/respuesta-a-revision-externa.md).

## Uso

El informe es **entrada para la revisión humana**, no un aval. Sus hallazgos se
integran o se rebaten en `docs/manuscrito.md` y `docs/registro-de-afirmaciones.md`,
con la trazabilidad de cada cambio.

