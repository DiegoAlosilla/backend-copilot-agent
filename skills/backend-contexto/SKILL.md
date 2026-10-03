---
name: backend-contexto
description: Entiende un microservicio Java existente o valida su memoria para identificar arquitectura, endpoints, clientes y lugares de cambio. Úsala para diagnóstico o antes de modificar un servicio.
---

# Contexto del servicio

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

1. Lee reglas compartidas y `engineering/backend/OPERACION.md`. Inspecciona Git y
   cambios ajenos. Identifica POM padre/módulos, framework/versiones, Java, Maven,
   contrato/generador, pruebas unitarias, Karate y configuración real.
2. Revisa `docs/engineering/service-map.md` y su metadata si existen. Con
   `backend.py snapshot` compara huellas del código actual y entradas de la memoria;
   incluye archivos nuevos, eliminados y cambios sin commit. Relee siempre las
   clases del flujo afectado. Si no hay mapa, crea un resumen inicial basado en
   código; no una exploración exhaustiva de cada clase.
3. Traza entrada → lógica → cliente/repositorio → salida. Enumera dependencias
   HTTP, eventos, Redis y BD únicamente con evidencia; cuenta clientes distintos
   por interfaces/config, no por número de llamadas. Distingue Channel/Business.
4. Detecta capas, hexagonal o híbrido por dependencias/imports. No deduzcas patrón
   solo de nombres de paquetes. Registra convenciones, tests representativos
   disponibles y comandos que realmente descubre el repo.
5. Completa `engineering/backend/repository-profile.json`; toolchain personal va en
   `.assistant-local/backend/toolchain.json`. Confirma perfiles y runners; no uses
   los paths de otro desarrollador. Ejecuta baseline si aplica.
   Lee `engineering/backend/ENTORNO.md` si se comparten Java/Maven o hay diferencias
   con VS Code. Configura el build real y ejecuta `backend.py doctor --repo .`;
   compara JDK efectivo de Maven con el POM antes de atribuir fallos al código.

Salida: mapa de flujo con rutas/símbolos, pruebas de referencia, perfil operativo,
lagunas y contradicciones. Si se pidió solo entendimiento, termina `DIAGNOSED`;
no implementes ni ejecutes la entrega completa.
