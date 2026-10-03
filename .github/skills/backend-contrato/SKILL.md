---
name: backend-contrato
description: Actualiza contratos HTTP o schemas de evento y regenera clases Java con el mecanismo del repositorio. Úsala cuando cambia una interfaz o falta un response documentado.
---

# Contract first

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Localiza contrato fuente, repo dueño, generator, configuración y rutas generadas.
Comprueba request/response, códigos, media types, required y clientes afectados.
Si el comportamiento esperado ya está documentado, registra que es corrección
de implementación. Si no está, cambia primero la fuente contractual autorizada.
Si el contrato vive fuera del workspace prepara diff/instrucciones y registra
la dependencia; no modifiques archivos derivados para simular el cambio.

Ejecuta el comando `generate` descubierto/revisado mediante el runner o mecanismo
existente del repo. Revisa diff de generados y compatibilidad. No cambia versión
del generator ni dependencias sin necesidad demostrada. Para eventos comprueba
consumidores y versión de schema por separado del contrato HTTP.

En HTTP 204 documenta response sin content; no añade un schema vacío de objeto.
Reporta contrato modificado/no requerido, generación y compatibilidad comprobada
o pendiente. La validación semántica del contrato no se sustituye por compilar.
