# Piloto: ausencia reconocida Business → UX 204 vacío

El requisito del usuario es HTTP 204 sin response body cuando Business indica
que no se encontró lo buscado en un escenario específico. El repo y logs aún no
se han recibido; no asumir HTTP 404 ni un código de negocio determinado.

## Datos mínimos, deducir cuando existan

- Endpoint UX y contrato de response; versión de runtime/generador.
- HTTP, payload/código o excepción real del Business en ese escenario.
- Resultado observado del UX y logs correlacionados de una misma solicitud.
- Caso de negocio que distingue “no encontrado” de una falla técnica.

## Investigación

Traza Resource/Controller → caso de uso/service → REST client/adaptador → exception
mapper o decoding → mapper global de UX. En Quarkus un REST client puede lanzar
una excepción antes de que el service lea el body. En flujo reactivo revisa
transformaciones/recovery de Uni y la preservación de la causa.

Reproduce el caso con la respuesta real sanitizada. Una hipótesis posible es que
el mapper genérico consuma una excepción que debía tener traducción específica;
otra es que un body/código esperado no se decodifique correctamente. Demuestra
la causa antes de elegir corrección. No uses catch de Exception → 204 ni vacía
todos los 404 de todos los clientes.

## Matriz mínima de comportamiento

| Entrada Business | Resultado UX | Validación |
| --- | --- | --- |
| Ausencia exacta reconocida por requisito | 204, cero bytes de cuerpo | Unitario de traducción + componente HTTP |
| Datos encontrados válidos | Response exitoso existente | Regresión de contrato/payload |
| Otro 4xx/código no equivalente | Mapeo controlado del repo | No se convierte a 204 |
| Timeout/5xx/red/payload inválido | Error según contrato existente | Conserva comportamiento; no inventa status |

Los escenarios se ajustan a integraciones reales. Probar 204 en límite HTTP:
ausencia de entidad serializada, no `{}`, `[]`, cadena JSON o `null`. No agregar
Content-Length de forma manual ni depender de JSON deserializado para verificar
ausencia. RFC 9110 establece que 204 no contiene contenido.
[Semántica HTTP 204](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.5).

Si el contrato ya declara ese 204, no modificarlo sin motivo. Si falta, actualizar
fuente de contrato primero y regenerar; no modificar interfaz generada.

## Primer mensaje listo para usar

```text
Modo completo. Corrige el manejo de respuesta en este microservicio UX.
Cuando Business indica que no encontró lo buscado en el escenario descrito,
UX debe responder HTTP 204 sin cuerpo; actualmente devuelve error genérico.
Usa los logs/MD/archivos de referencia que adjunto. Determina la condición exacta
y el punto donde se pierde el error controlado; no conviertas otros fallos a 204.
Reproduce el fallo, prepara plan con clases/métodos, implementa la corrección y
pruébala con unitarias y Karate. Verifica clean install y 95% de INSTRUCTION.
Config Maps será manual. Entrega diff/evidencias; no hagas push ni despliegue.
```
