---
name: backend-memoria
description: Actualiza memoria técnica, diagramas y bitácora por ticket después de un cambio Java, o valida documentación al reanudar. No reconstruye el repositorio completo si el delta es acotado.
---

# Memoria compartida

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Actualiza `docs/engineering/service-map.md` y expediente `changes/<ticket>` con
plantillas en `engineering/backend/templates`. Registra fuentes/rutas/símbolos y
lagunas. Usa ADR separado solo para decisiones duraderas con alternativas.
Diagrama estable sin colores históricos; diagrama del ticket puede marcar impacto.

Guarda metadata de `backend.py snapshot` en `service-map.meta.json` como base de
inspección, con fecha y referencia de PR revisado cuando exista. Snapshot es
inventario/huella, no aprobación. No escribe el SHA del futuro commit documental
en sí mismo. Compara archivos/hash antes de reutilizar; mapa aprobado no aprueba
otro cambio. Relee ruta afectada y actualiza solo secciones invalidadas.

Expediente conserva plan→resultado, prueba de aceptación, decisiones, resumen de
gates y config handoff. Logs crudos y evidencia ejecutable permanecen locales/CI;
docs llevan extractos sanitizados/enlaces. Si se pidió solo documentación, termina
SCOPED_TASK_DONE y no afirma que el código pasó tests.
