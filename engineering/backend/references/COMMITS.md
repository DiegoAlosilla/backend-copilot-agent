# Política de commits del paquete

Convención inicial del equipo; ajustar explícitamente según el repositorio.
Mensaje type(scope): JIRA-TICKET message, inglés, presente simple, ≤72 caracteres.
Objetivo 1–2 commits por PR; 3–4 riesgo de score y >4 no recomendable. Promedio
archivos/commit <15 y líneas/commit <100. Líneas PR ≤50 ideal; 51–300 aceptable;
>300 recomienda evaluar separación. Mínimo tres revisores en PR.

Son métricas corporativas de forma; no equivalen a calidad funcional. El delta
total incluye tests y documentación que deben acompañar la corrección. Separar
solo por responsabilidad/revisabilidad. El script computa net diff desde merge
base contra HEAD, pendiente contra HEAD y suma por commit; no suma delta neto
como si fuera volumen real de cada commit. Proyección es informativa porque un
nuevo commit puede revertir/cambiar líneas existentes.

Calidad de código exige evidencia actual. Cambios solo docs pueden usar validación
documental apropiada sin ejecutar Maven; informar por qué no aplica. No concede
excepción a cobertura productiva ni omite Karate para facilitar commit.

No se instala hook bloqueante universal: seguir instrucciones no garantiza su
cumplimiento. CI debe aplicar gates obligatorios antes de integrar según repo.
