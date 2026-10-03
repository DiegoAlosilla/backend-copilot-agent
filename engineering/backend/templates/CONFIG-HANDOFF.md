# Config Maps — traslado manual <ticket>

Estado: NOT_REQUIRED | MANUAL_PENDING | MANUAL_CONFIRMED
Rama feature de Config Maps:
Archivos locales fuente:
SHA/diff código:
Nombre real de carpetas/archivo:
delivery y Groovy: referencia o pendiente; no generar estructura inventada.

| Clave | Operación | Consumidor | Tipo | DEV | CERT | PROD | Destino confirmado | Validación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Cambios solo locales excluidos del traslado

URLs mock, switches de test y otros overrides; justificar exclusión sin secretos.

## Ejecución manual del desarrollador

1. Crear/reutilizar rama feature y revisar los YAML del servicio en desarrollo,
   certificación y producción; mantener APIs y referencias de cada ambiente.
2. Aplicar solo las claves compartidas del delta; validar parser y diff del servicio.
3. Completar delivery con formato del repo si aplica; no copiar valores sensibles.
4. Commit/push por modelo de la organización y ejecutar Jenkins con rama/ambiente correctos.
5. Confirmar traslado a Properties y registrar SHA/job/ambiente.
6. Al desplegar confirmar carga efectiva y comportamiento del microservicio.

Orden de promoción/compatibilidad/rollback:
Pendientes que impiden el pase:
Evidencia del dev (job, Properties, release/verificación):
