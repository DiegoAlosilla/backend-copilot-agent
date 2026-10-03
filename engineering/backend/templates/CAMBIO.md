# <ticket>: <objetivo>

Estado: IN_PROGRESS | DIAGNOSED | SCOPED_TASK_DONE | LOCAL_VERIFIED | BLOCKED
Modo: completo | diagnóstico | unitarias | Karate | sanity | commits | memoria
Base inspeccionada:
Fuentes y aceptación:
Alcance autorizado:

## Observado y esperado

Síntoma, condición exacta y resultado verificable. Separar hechos e hipótesis.

## Matriz de impacto

| Ruta | Clase/método/clave/schema | Cambio | Criterio | Prueba |
| --- | --- | --- | --- | --- |

## Plan y decisiones

Tareas, dependencias, fuera de alcance y preguntas que bloquean una tarea concreta.

## Trazabilidad del flujo

En modo completo registrar las ocho fases, aunque alguna no aplique. Cada skill
debe haber sido cargada de verdad: herramienta de skills o lectura del SKILL.md.
Separar instrucciones cargadas de acciones terminadas y resultados comprobados.

| Fase | Skill(s) | Carga y ruta real | Estado | Acción/evidencia o motivo de no aplica |
| --- | --- | --- | --- | --- |
| 1. Contexto/evidencias | | | NOT_RUN | |
| 2. Plan | | | NOT_RUN | |
| 3. Contrato | | | NOT_RUN | |
| 4. Implementación | | | NOT_RUN | |
| 5. Pruebas | | | NOT_RUN | |
| 6. Configuración | | | NOT_RUN | |
| 7. Calidad | | | NOT_RUN | |
| 8. Memoria/entrega | | | NOT_RUN | |

En modo individual registrar solo el alcance solicitado. SCOPED_TASK_DONE no
cierra un cambio completo. Gates/aceptación pendientes dejan el modo completo
en BLOCKED, con avances y dependencias identificados.

## Resultado y evidencia

| Gate | PASS/FAIL/NOT_RUN/NOT_APPLICABLE | Evidencia | Alcance |
| --- | --- | --- | --- |

Comando/run ID/huella, escenarios reproducidos, causa y regresiones verificadas.
CI/Sonar/revisión humana separados de las compuertas locales.

## Configuración y entrega

No requerido con razón o enlace a CONFIG-HANDOFF. Pendientes y rollback.
Commit/push/PR ejecutados o preparados según alcance. No mezclar estado local
con aprobación del cambio ni verificación de producción.
