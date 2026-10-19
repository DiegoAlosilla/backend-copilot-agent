# Cambios

## 0.8.0 — 18 de octubre de 2026

- Conserva el flujo SDD con matriz AC de requisito/origen, prueba y evidencia.
- Checkpoint de sesión y reanudación con invalidación de resultados afectados.
- Verificador opcional PowerShell: ejecuta Maven, valida JUnit/Checkstyle/JaCoCo
  actuales y vincula aceptación, hashes de fuentes, política y reportes.
- Rechaza tests omitidos/fallidos, suites vacías, reportes viejos, cobertura
  insuficiente/solapada y criterios sin un test aprobado inequívoco.
- Modo VerifyOnly para comprobar evidencia existente sin ejecutar Maven.
- Ocho casos de piloto con revisión humana y medidor de éxito, fallos críticos,
  tiempo e intervenciones; casos pendientes nunca producen aprobación.
- Pruebas de regresión de las herramientas y workflow del paquete. La integración
  en CI de servicios y la eficacia en Copilot requieren adopción/piloto reales.
- Mantiene recursos y evidencia fuera del microservicio, sin nuevo runtime del
  agente ni instalaciones globales, y conserva aprobación previa a stage/commit.

## 0.7.0 — 4 de octubre de 2026

- Un único agente y flujo completo; skills internas sin comandos individuales.
- Sustituye preparación de soporte por detección de entorno y contexto reutilizable.
- Retira runtime, instaladores, scripts Python/PowerShell, tests y CI del paquete,
  engineering, reglas duplicadas, evaluadores, plantillas y expedientes automáticos.
- Mantiene procedimientos de contrato, HTTP, Java, pruebas, Kafka, configuración
  manual y calidad dentro de las skills.
- Siempre presenta diagnóstico, sospechas y plan antes de modificar.
- Contexto en memoria del editor o archivo personal fuera del microservicio.
- Agrupación concreta de commits con aprobación previa a stage/commit.
- Atiende sesión GitHub expirada con login del desarrollador y reanudación.
- Solo dos instalaciones: plugin VS Code o archivos personales en ~/.copilot.
- Documentación del servicio únicamente bajo solicitud expresa.

Esta versión reemplaza la arquitectura de 0.6.0 y anteriores. No requiere sus
archivos de soporte. Historial previo disponible en Git.
