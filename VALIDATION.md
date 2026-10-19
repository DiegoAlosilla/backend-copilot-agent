# Validacion local de 0.8.0

Fecha: 18 de octubre de 2026 (America/Lima).

| Comprobacion | Resultado observado |
| --- | --- |
| `pwsh -NoProfile -File tests/Test-Harness.ps1` | 31 comprobaciones aprobadas con fixtures sinteticos |
| `pwsh -NoProfile -File tests/Test-MavenIntegration.ps1` | Maven 3.9.9 / JDK 17: 2 tests, 100% INSTRUCTION, cero violaciones Checkstyle, 2 AC aprobados y VerifyOnly vigente |
| Sintaxis de scripts con parser Windows PowerShell 5.1 | Aprobada; no ejecuta scripts |
| Ejecucion Windows PowerShell 5.1 | Pendiente: el host exige scripts firmados y rechazo la ejecucion |
| Frontmatter de las 15 skills | Nombre, descripcion y `user-invocable: false` comprobados como YAML |
| Validador generico skill-creator | Aprobado sobre copias temporales retirando solo `user-invocable`, campo Copilot no admitido por ese validador; originales conservados |
| Links Markdown locales y YAML del workflow | Comprobados |
| `git diff --check` | Sin errores |

La integracion Maven usa un proyecto Java minimo sintetico y un repositorio de
dependencias temporal con settings vacios. No demuestra comportamiento HTTP real
ni calidad del agente. La suite de regresion comprueba aceptacion, fallos/errores,
omisiones, suites vacias, reportes ausentes/viejos, contadores inconsistentes,
cobertura insuficiente/solapada, ponderacion por instrucciones, vigencia de fuentes,
politica y reportes, ejecucion nativa Maven y scoring con casos pendientes.

Los ocho escenarios de `evaluations/cases.json` quedan listos para el piloto
humano; no se registran resultados ficticios como ejecuciones de Copilot.
Pendientes: piloto corporativo, ejecucion remota del workflow, compatibilidad de
ejecucion 5.1 y adopcion/check obligatorio en CI de cada servicio.
