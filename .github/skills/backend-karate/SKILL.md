---
name: backend-karate
description: Crea o ajusta pruebas de componente Karate y verifica runners y resultados reales. Úsala para features, escenarios HTTP o regresión de un flujo; puede ejecutarse sin el agente completo.
---

# Karate de componente

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Detecta versión, runner, perfil, tags, karate-config, mocks y formato real de
reportes. Mantén convenciones; no instala otra versión ni asume que Maven lo
ejecuta. Usa stubs deterministas del Business para reproducir el escenario.
Verifica códigos esperados, payload/schema y errores; un status 500 inesperado
falla aunque haya conectividad. Para 204 verifica ausencia de contenido con las
assertions compatibles con el runner y un control HTTP de cuerpo cuando haga
falta; no esperes `{}` o JSON null.

Ejecuta comando `karate` con runner y reportes explícitos del perfil. Registra
escenarios descubiertos, ejecutados, fallidos y omitidos. Soporte automático:
JUnit XML o summary Karate JSON con counters documentados en OPERACION.md.
Si otro formato no está soportado conserva evidencia y registra revisión manual;
no declara compuerta verificada por el script.

Si falta infraestructura sigue creando/revisando escenarios y declara ejecución
bloqueada. No atribuye éxito de componente a un mock unitario del cliente.
