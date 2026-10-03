---
name: backend-errores-http
description: Diagnostica y corrige la traducción de respuestas Business a HTTP en un servicio UX o Channel, incluyendo el caso específico que debe devolver 204 vacío en lugar de error genérico.
---

# Traducción Business → UX

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Lee `engineering/backend/references/CASO-204.md` para el piloto 204. Es una guía de
investigación, no una regla universal “404 → 204”.

1. Obtén endpoint y condición exacta: HTTP Business, código/payload o excepción.
   Traza REST client, response exception mapper, service/use case, mapper global
   y Resource. Revisa Mutiny si es reactivo y dónde el fallo cambia de tipo.
2. Confirma regla funcional con usuario/contrato: solo el escenario identificado
   se convierte al status esperado. No convierte auth, timeout, 5xx, payload
   inválido ni cualquier NotFoundException de otro origen en éxito vacío.
3. Reproduce con fixture/stub y test antes de cambiar. Elige el punto de mapeo
   del repo con menos impacto. Mantén observabilidad y manejo de otros errores.
4. Si el contrato no contempla el response requerido usa `backend-contrato` primero.
   Código generado no se modifica manualmente.
5. Verifica status y ausencia de body en el límite HTTP; una entidad null en
   unitarias no basta. Prueba caso encontrado, ausencia reconocida y errores
   distintos al caso. Mantén encabezados corporativos aplicables.

Salida: causa demostrada, punto de cambio, pruebas de traducción y regresión;
estado de cobertura/build se reporta separado si se pidió solo diagnóstico.
