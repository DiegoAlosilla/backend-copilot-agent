# Cambios

## 0.4.0 — 3 de octubre de 2026

- Entrada única: seleccionar backend-java y describir el cambio. Retirado el
  prompt redundante cuyo nombre aparecía con sufijo .prompt en VS Code.
- Modo completo por defecto para cambios; SCOPED_TASK_DONE solo para individuales.
- Carga explícita de SKILL.md, anuncio de fases y registro de evidencia por fase.
- Precondición de preparación visible y cierre BLOCKED si faltan gates/soporte.
- Carpetas convencionales agents/skills/rules; instalador por archivos adapta
  destinos y conserva configuración propia. Reglas compartidas como componente
  del plugin y lectura explícita del agente.
- README explica nombres del menú, cada carpeta y límites de los ensayos.

## 0.3.0 — 3 de octubre de 2026

- Nombres y contenido genéricos; historial inicial nuevo para la distribución.
- README con instalación desde Git, capacidades y modos individuales.
- Todos los scripts/checks sin dependencias pip; ensayos con -S.
- Diagnóstico Java/Maven y overrides locales de rutas, settings y repositorio.
- Cambios del entorno efectivo invalidan evidencia anterior; 42 pruebas pasaron.

## 0.2.0 — 2 de octubre de 2026

- Distribución Git como plugin Copilot con agente y skills desde la misma fuente.
- Skill de preparación de repo para instalar/actualizar soporte sin duplicar
  agentes del plugin ni tocar configuración local del servicio.
- Actualización de archivos gestionados por huellas; conserva perfiles/políticas
  y texto ajeno a su bloque de instrucciones. Conflictos se detectan antes de copiar.
- Guía de instalación/actualización nativa en VS Code, ajustes y CI del paquete.

## 0.1.0 — 2 de octubre de 2026

- Primer MVP: agente backend, 14 skills independientes, memoria y evidencias.
- Caso piloto Business→UX 204 vacío y Config Maps como traslado manual.
- Runtime Python estándar con verificación de reportes y pruebas en repos temporales.
