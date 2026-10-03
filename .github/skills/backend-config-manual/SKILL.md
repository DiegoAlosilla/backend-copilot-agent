---
name: backend-config-manual
description: Prepara un traslado manual de configuración desde un cambio Java hacia Config Maps DEV/CERT/PROD, con claves y valores por ambiente. En el MVP no edita repositorios externos ni ejecuta Jenkins.
---

# Configuración — handoff manual

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Lee `engineering/backend/references/CONFIG-MAPS.md` y usa
`engineering/backend/templates/CONFIG-HANDOFF.md` en el expediente del cambio.

Detecta configuración real de Quarkus y perfil local; YAML requiere soporte del
proyecto. Clasifica cada cambio: compartido por ambiente, exclusivo local, secreto
o desconocido. Solo prepara traslado de los compartidos; secretos son referencias
al gestor corporativo, no literales. URLs locales, mocks y switches de seguridad
de test no pasan a ambientes de la organización.

Por clave compartida registra consumidor, tipo, valor DEV/CERT/PROD o pendiente,
operación (alta/modificación/baja), archivo destino confirmado o aún por confirmar
y prueba necesaria. Presencia compatible no significa valores idénticos.
Documenta rama feature, directorios desarrollo/certificación/producción y delivery
con nombres reales cuando se proporcionen. No inventa formato de delivery ni
Groovy; solicita esa estructura cuando sea necesaria para una fase futura.

Si no hay cambios compartidos registra “no requerido”. Si faltan valores por
ambiente deja pendientes, sin bloquear unitarias/local. Entrega guía para que el
dev copie/edite únicamente el delta, ejecute job del ambiente y confirme versión
en Properties. Estado `MANUAL_PENDING` hasta evidencia del desarrollador.
