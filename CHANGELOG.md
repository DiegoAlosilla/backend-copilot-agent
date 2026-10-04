# Cambios

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
