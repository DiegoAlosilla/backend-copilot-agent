---
name: backend-sanity
description: 'Ejecuta solo una prueba sanitaria o smoke test de un microservicio: salud y escenarios mínimos definidos, con status y cuerpo esperados. No equivale a cobertura o pruebas completas.'
---

# Sanity / prueba sanitaria

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Aclara alcance usando el pedido: URL/ambiente o arranque local, health y endpoint
funcional representativo. Deduce config desde el repo si se trabaja local.
No levanta Redis, fachadas o Business que el servicio no use. Reutiliza procesos
existentes; registra qué arrancaste y si deben quedar abiertos según pedido.

Define resultado esperado por escenario antes de ejecutarlo. Health, endpoint
y downstream son verificaciones distintas; un 4xx/5xx puede probar conectividad,
pero solo pasa aceptación si era esperado. En el caso piloto comprueba HTTP 204
y body vacío, caso con datos y un error real controlado mediante fixtures.
No hace requests mutantes a producción por un pedido genérico de sanity.

Registra URL sin datos sensibles, ambiente, status, bytes de body, duración y
resultado esperado/observado. Si pruebas HTTP 204 con herramientas que omiten
body automáticamente, verifica además mapeo/serialización en test de componente.
Salida SCOPED_TASK_DONE/BLOCKED; unitarias, cobertura, build y commits quedan
NOT_RUN si no se solicitaron. No inicia flujo completo ni prepara PR.
