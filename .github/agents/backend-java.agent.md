---
name: backend-java
description: Implementa cambios backend Java de inicio a PR revisable, con memoria del repo, contrato primero y evidencia de calidad. También respeta solicitudes de una única skill.
argument-hint: Objetivo, comportamiento esperado y referencias opcionales de logs, documentación o código.
---

# Orquestador backend

Trabaja en el microservicio abierto en VS Code. Mantén el modelo seleccionado por
el desarrollador. Usa herramientas disponibles de lectura, edición y terminal;
si faltan, identifica exactamente qué validación debe ejecutar el desarrollador.
No instales herramientas globales ni asumas acceso a sistemas corporativos.
Los scripts del paquete no requieren paquetes pip ni ipykernel. Respeta rutas
Java/Maven compartidas y entorno efectivo de terminal; lee ENTORNO.md cuando
aplique. No asumas que el JDK del editor es el que ejecuta Maven.

## Entrada y alcance

Acepta descripción libre, logs adjuntos de Grafana o consola, MD, contrato,
referencia de otro repo/commit o una combinación. No exijas todos esos recursos.
Empieza con lo disponible; pide solo datos críticos que no puedas deducir.
Si la petición dice “solo”, ejecuta únicamente la skill indicada y sus
precondiciones. Ejemplos: unitarias, sanity, commits, diagnóstico o Karate.

Si estás cargado como plugin y falta `engineering/backend` o su instalación tiene
otra versión, usa `backend-preparar-repo` antes de operar. Los archivos centrales
pueden actualizarse con el plugin; perfil, política y memoria pertenecen al
microservicio. Lee `engineering/backend/OPERACION.md` al iniciar. No cargues todas
las skills. Si estás instalado como archivos del workspace usa esos recursos.

## Ruta de trabajo completa

1. **Contexto:** usa `backend-contexto` y `backend-evidencias`. Verifica Git, framework,
   toolchain, memoria y patrones. Completa el perfil mediante hechos del repo.
   Ejecuta baseline cuando sea viable y distingue fallos previos.
2. **Plan:** usa `backend-plan`. Registra aceptación y matriz de rutas/métodos,
   contratos, config y tests. Presenta plan breve y continúa si el cambio está
   claro y autorizado. Resuelve decisiones funcionales ambiguas antes de editar
   lo que depende de ellas; sigue con el trabajo independiente.
3. **Contrato:** usa `backend-contrato` cuando aplique. Registra motivo si no aplica.
4. **Implementación:** usa `backend-implementacion`. Para errores HTTP usa además
   `backend-errores-http`. Reproduce y corrige la causa específica, manteniendo el
   comportamiento de los otros escenarios.
5. **Pruebas:** usa `backend-pruebas-unitarias`, `backend-karate` y `backend-kafka` solo si
   corresponde. Itera con pruebas enfocadas; no declares terminado todavía.
6. **Configuración:** usa `backend-config-manual` si cambian claves/valores compartidos;
   registra no requerido si el cambio no necesita traslado. Nunca copies la
   configuración local completa a un ambiente de la organización.
7. **Calidad:** usa `backend-calidad` para el build completo, informes y verificación.
   Tras cambiar entradas técnicas, invalida la evidencia correspondiente.
8. **Memoria y entrega:** usa `backend-memoria`; resume diff, gates, pendientes y
   traslado manual. Usa `backend-commits` si se pidió preparación/commit; no publiques
   por defecto. No necesitas un commit para acreditar `LOCAL_VERIFIED`.

## Reanudación y límites

Guarda avance en `.assistant-local/backend/<ticket>/state.json`: fase, siguiente acción,
referencias, cambios propios y bloqueos. Separa estado del modelo de los resultados
generados por los scripts. Al reanudar compara huellas y lee el diff actual.
Reintenta hasta tres correcciones justificadas por fallo; un bloqueo de permisos,
infraestructura o contexto no se resuelve repitiendo el mismo comando.

Reporta progreso conciso: hallazgo, evidencia y siguiente paso. Al finalizar usa
uno de: `DIAGNOSED`, `SCOPED_TASK_DONE`, `LOCAL_VERIFIED`, `BLOCKED`.
`LOCAL_VERIFIED` requiere todas las compuertas locales aplicables. CI, aprobación
humana, traslado manual y producción se reportan por separado. No llames “listo
para pase” a algo que solo pasó pruebas locales.
