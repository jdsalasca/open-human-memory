# Pre-registro de experimentos confirmatorios

**Fecha:** 17 de noviembre de 2026

La auditoría de MEM-005 señaló que el protocolo, el código, los resultados y el
análisis entraron en el mismo commit. Eso no prueba que las hipótesis se cambiaran
después de ver los datos, pero **impide que un tercero lo verifique**. Este documento
fija el flujo para los experimentos confirmatorios.

## Flujo

1. **Protocolo.** Se escribe `protocolo.md` con pregunta, diseño, métricas, claims y
   criterios de muerte.
2. **Código y tests.** Se implementa el experimento y los tests sin ejecutar las
   llamadas al modelo.
3. **Hash y commit.** Se calcula el SHA-256 del protocolo y se guarda en
   `protocolo.sha256`. Se commitean protocolo, código, tests y hash **antes** de la
   corrida.
4. **Corrida.** Se ejecuta el experimento con el modelo y la semilla fijados.
5. **Resultados.** Se publican los JSON y el análisis en un **commit separado**.
6. **Errata.** El protocolo no se edita después de la corrida. Cualquier corrección
   va en `errata.md` con fecha y motivo.

## Comandos

```powershell
Get-FileHash resources/investigation/mem-006/protocolo.md -Algorithm SHA256 |
  ForEach-Object { $_.Hash.ToLower() } |
  Set-Content resources/investigation/mem-006/protocolo.sha256
```

El revisor puede comprobar el hash con:

```powershell
Get-FileHash resources/investigation/mem-006/protocolo.md -Algorithm SHA256
```

## Estado

| Experimento | ¿Pre-registrado con hash? | Nota |
|---|---|---|
| MEM-002/003/004 | No | Exploratorios; protocolo y resultados en el mismo commit |
| MEM-005 | No | Exploratorio; el factorial se diseñó tras MEM-004 |
| MEM-006 | **Sí** | Protocolo y hash en `mem-006/` antes de la corrida |
| META-001 | Pendiente | Debe seguir el mismo flujo |

**Regla:** un experimento sin hash previo se reporta como **exploratorio** y no se usa
para confirmar una claim. Los pilots siguen siendo útiles; no se presentan como
confirmación.
