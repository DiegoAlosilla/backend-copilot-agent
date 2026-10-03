---
name: backend-plan
description: Prepara un plan verificable de cambio Java con matriz de contrato, clases, métodos, configuración y tests. Úsala para planificar; en modo solo plan no modifica lógica.
---

# Plan de cambio

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Usa `engineering/backend/templates/CAMBIO.md`. Define comportamiento actual, esperado,
aceptación y alcance. Por cada cambio identifica ruta y símbolo real, razón y test.
Marca archivos propuestos como nuevos; no inventes métodos en clases existentes.
Separa cambio obligatorio de mejoras opcionales y preserva arquitectura existente.

Planifica contrato/generación cuando aplique, lógica, pruebas y config manual.
Incluye diagnóstico antes de corrección y regresión de escenarios vecinos.
Estima riesgos por dependencias y cobertura baseline, no por promesas de duración.
Si baseline ya incumple calidad, informa costo y bloqueo; no baja umbrales.

Diagramas: dependencias externas e internos para ubicación; secuencia para el flujo
cuando aclara errores/orden. Color ámbar = modificado, verde = nuevo, con leyenda;
detalle de métodos va en matriz de impacto. Si se pidió solo plan, termina aquí.
