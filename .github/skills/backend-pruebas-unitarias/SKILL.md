---
name: backend-pruebas-unitarias
description: Crea o corrige pruebas unitarias Java y verifica cobertura JaCoCo con la política del repo. Úsala para solo unit tests, Mockito, AAA o cobertura; no activa commits ni cambios funcionales por defecto.
---

# Unitarias Java

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Lee política y `engineering/backend/ESTANDAR-JAVA.md`. Identifica convenciones y tests
de referencia disponibles antes de escribir. AAA con separación, @DisplayName,
nombres descriptivos en inglés y assertions sustantivas. MockitoExtension,
@Mock/@InjectMocks para pruebas unitarias con Mockito cuando corresponda; no
impone Mockito a CDI o @QuarkusTest. Usa matchers tipados y validación de mensaje/
código en assertThrows. No @Disabled, lenient ni tests comentados para cerrar.

Cubre caminos feliz, errores y límites relevantes del código intervenido;
no mockees toda la lógica ni asserts solo de existencia. Mantén Checkstyle en
src/test y cabecera BACKEND. No modifica productivo para subir cobertura salvo que
la solicitud incluya corregirlo; reporta si descubres un defecto.

Ejecuta comando `unit` con `backend.py run`, usando profile y run ID. Para acreditar
95% global usa medición de suite completa y XML elegible; un test seleccionado
no acredita cobertura global. Si solo pide tests de una clase, puede cerrar
`SCOPED_TASK_DONE` con resultado específico y cobertura global `NOT_RUN`.
No baja mínimo ni excluye lógica para alcanzar score. Build/commit completo se
invoca únicamente si el usuario pidió ese alcance.
