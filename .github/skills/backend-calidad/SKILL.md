---
name: backend-calidad
description: 'Ejecuta y verifica compuertas locales con reportes actuales: unitarias, Karate, Checkstyle, JaCoCo y Maven clean install. Úsala para cierre completo o validación del build, sin publicar cambios.'
---

# Calidad con evidencia

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Lee `engineering/backend/OPERACION.md` y política; revisa profile y toolchain.
Ejecuta comandos mediante `engineering/backend/scripts/backend.py run` con un run ID común.
Comandos son arrays revisados, sin shell interpolado. Si full build ejecuta las
suites y genera todos los reportes, declara sus gates en profile y evita repetir
comandos sin motivo. Si Karate corre separado, ejecuta build final primero y
luego Karate, evitando que clean borre su evidencia.

Build final incluye clean/install sin skips. Checkstyle requiere objetivo check
o binding corporativo que realmente bloquee y cubra tests; reportar checkstyle
no basta. Cobertura usa INSTRUCTION 95% y XML válido con contador root; BRANCH
se informa separado. No sumes reportes solapados ni cuentes doble generado.
Registra alcance/exclusiones existentes y no las amplíes por cuenta del agente.

Ejecuta `backend.py verify`. Corrige hasta tres iteraciones justificadas. Si cambian
entradas técnicas repite gates afectados con nueva huella. Reportes ausentes,
viejos, cero tests, tests omitidos, command failure o formatos desconocidos no
son PASS. CI y Sonar corporativos se reportan aparte; nunca los inventes.

El script verifica archivos/contadores/huellas, no calidad semántica de tests ni
compatibilidad de contrato. Revisa esos aspectos y presenta evidencia humana.
Solo usa LOCAL_VERIFIED cuando gates locales requeridos pasan y aceptación está
cubierta; mantén pendientes de config manual/CI y revisión final por separado.
