---
name: backend-implementacion
description: Implementa un cambio acotado en backend Java Spring o Quarkus siguiendo arquitectura y patrones del repo. Úsala tras entender la ruta de cambio y aceptación.
---

# Implementación Java

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Implementa tareas del plan con diffs pequeños y pruebas durante la iteración.
Preserva imports/dependencias entre capas o puertos/adaptadores. No migra la
arquitectura como efecto lateral. Usa librerías y manejo de errores existentes.
Reutiliza patrones del servicio cuando sean correctos; no copies código de
referencia incompatible con versiones, contrato o reglas locales.

Evita capturas genéricas que oculten fallos, bloquear pipelines reactivos,
timeouts nuevos arbitrarios y log de datos sensibles. Maneja recursos, estados
vacíos y excepciones con la semántica acordada. Nuevas clases usan cabecera BACKEND
definida en `engineering/backend/ESTANDAR-JAVA.md`.

Tras cada tarea corre tests relevantes y revisa diff/Checkstyle. Si la corrección
demanda configuración utiliza `backend-config-manual`; si hay evento utiliza `backend-kafka`.
No declarar cambio terminado antes de `backend-calidad` en el flujo completo.
