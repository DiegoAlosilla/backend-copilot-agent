# <servicio> — mapa técnico

Estado documental: borrador | revisado
Metadata: service-map.meta.json (snapshot del código inspeccionado)
PR/revisor/fecha de revisión cuando exista:

## Responsabilidad

Channel/Business, endpoints/eventos y contrato fuente.

## Arquitectura y dependencias

Patrón observado y evidencia (rutas/símbolos/imports).
Diagrama Mermaid externo y componentes internos cuando añadan claridad.

| Cliente/recurso | Protocolo/uso | Config keys | Timeout/errores | Evidencia |
| --- | --- | --- | --- | --- |

## Flujos relevantes

Entrada → caso de uso/service → dependencia → mapeo → salida.
Secuencia del caso complejo, enlace a clases/métodos y tests.

## Build y pruebas

Comandos/perfiles y runners realmente comprobados; versión framework/toolchain.

## Configuración y pase

Recorrido Config Maps → Jenkins → Properties → Azure/GitOps confirmado; diferencias
por ambiente mediante referencias sin datos sensibles.

## Lagunas y decisiones

Supuestos, contradicciones, ADRs y expedientes por ticket. Aprobar documentación
no sustituye relectura de código en el siguiente cambio.
