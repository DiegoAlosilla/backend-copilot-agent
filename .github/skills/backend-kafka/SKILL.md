---
name: backend-kafka
description: Implementa o prueba cambios Kafka Java cuando el repositorio usa publicación o consumo de eventos. Úsala para topics, schemas, schemas de notificación o fallos de mensajería confirmados.
---

# Kafka

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Confirma framework/conector y versiones con código/POM. Revisa schema/payload,
clave, headers, topic por config y consumidores. No asume transporte Kafka por
el nombre de una integración ni crea schemas a partir de nombres de negocio.
Para productores distingue confirmación del broker de procesamiento consumidor.
Para consumidores revisa ack/nack, reintentos, duplicados/idempotencia, orden y
DLQ según requisitos del flujo; no promete exactly-once de negocio.

Usa pruebas y dependencias ya aprobadas (stub, in-memory o broker test). No
impone Docker/Testcontainers cuando no estén habilitados. Registra explícitamente
qué semántica valida cada prueba. Si necesita configuración externa prepara
handoff con `backend-config-manual`; no toca Jenkins/Properties.
