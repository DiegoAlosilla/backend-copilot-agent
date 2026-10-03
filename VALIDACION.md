# Validación de la entrega 0.4.0

Fecha: 3 de octubre de 2026. Ejecutado en Windows con Python 3.14 y PowerShell 7.

**42 pruebas automáticas pasaron**, sin cargar paquetes instalados, mediante:

```powershell
py -3 -S -m unittest discover -s tests -v
```

Cobertura de los ensayos (no es porcentaje JaCoCo):

- Instalador: plan sin escritura, preservación de instrucciones existentes,
  segunda instalación sin duplicación, exclusión local de logs y conflicto
  detectado sin instalación parcial. SupportOnly no copia agentes/workflows;
  actualización conserva perfil/política, protege archivos personalizados y
  mantiene texto ajeno al bloque de instrucciones (incluido cambio CRLF/LF).
- Reportes: mínimo exacto 95%, 94.9% rechazado, contador root sin doble suma,
  JaCoCo solapado/inválido, cero tests, JUnit agregado, fallos, omitidos y
  contadores inconsistentes, Karate vacío/fallido/desconocido, Checkstyle vacío
  o con violaciones.
- Ejecución real de fixtures en repos Git temporales: compuertas verdes, Karate
  no ejecutado, reportes viejos, cambio posterior de código/toolchain, reporte
  alterado, comando fallido, excepción incompleta, timeout con terminación del
  proceso y rutas/IDs inválidos.
- Huella: archivos nuevos sí cuentan, bitácora/logs excluidos, toolchain local
  incluido por hash. Métricas distinguen commits, delta PR y pendiente.
- Toolchain: overrides Java/Maven aplicados solo al hijo, PATH conservado,
  entorno heredado, rutas inválidas bloqueadas, cambio de entorno invalida
  evidencia y diagnóstico compara Java de Maven con el requerido.
- Frontmatter plano: scalars del paquete y rechazo explícito de formas no
  soportadas/duplicadas. El validador no necesita un parser YAML externo.

Se comprobó el frontmatter de las **15 skills**, agente y reglas, además de JSON,
nombres, referencias internas y sintaxis Python. Todos los scripts/checks usan
biblioteca estándar. `py -3 -S distribution/check_package.py` pasó.

`distribution/check_package.py` valida el manifest Copilot y 17 definiciones
(15 skills, agente y reglas). Los checks no prueban que un modelo aplique las
skills ni que termine el flujo completo; esa conducta se valida en el piloto.
La CI de 0.3.0 pasó en Windows/Python 3.10 y 3.14. El resultado de la nueva
versión se registra en Actions y en las notas de su release.

El piloto de 0.3.0 informó skills visibles en slash, una búsqueda de OPERACION.md
sin coincidencias y un arreglo sin trazabilidad completa. Eso confirma descubrimiento
en ese cliente; no acredita preparación ni carga/ejecución de cada skill.
El registro de la sesión también contiene baseline clean install fallido y tests
focalizados correctos. No contiene evidencia de cierre completo tras el cambio.
Los logs dejan pendiente confirmar la señal funcional del request; un arreglo
defensivo no demuestra por sí mismo resolución del incidente observado.
0.4.0 corrige las instrucciones de alcance, carga, fases y cierre y simplifica
la entrada. Requiere repetir el piloto para evaluar cumplimiento real.

Las fixtures simulan reportes; no son pruebas de Quarkus/Karate de un servicio
empresarial. No se probaron los gates reales del servicio, Maven/Artifactory,
CI/Sonar o Grafana. Instalación desde fuente y ciclo automático
de actualización VS Code no se probaron en el cliente corporativo. No hay repo
UX objetivo en este workspace.
El caso 204 y comandos/runners deben probarse al instalar en ese repositorio.

Los scripts son controles de consistencia, no controles contra un operador que
modifique evidencia ni validadores semánticos de contrato/tests. La revisión y
CI deben comprobar aceptación, alcance de suites y exclusiones. Python 3.10+ y
Windows PowerShell están contemplados por el código; versiones distintas a las
probadas necesitan su propia verificación.

Formatos contrastados con documentación oficial de VS Code/Copilot enlazada en
README. No se copiaron skills externas ni se instalaron herramientas de la organización.

## 0.5.0: control del flujo tras el segundo piloto

El segundo log suministrado describe una auditoría individual, revisión de cambios
existentes, 9 pruebas focalizadas aprobadas y clean install fallido. No contiene
el pedido original ni evidencia suficiente de carga de skills o de ocho fases.
No se confirma qué commit/imagen estaba desplegado ni que la prueba fallida fuese
obsoleta. No se incorporaron logs, rutas ni contenido del servicio a este paquete.

Se añadieron workflow-start/phase/close al runtime existente, sin dependencias.
53 pruebas locales con Python y -S aprobaron: las 42 existentes y 11 del flujo.
Las nuevas verifican alcance conservado, cita requerida para individual, fases
pendientes, evidencia modificada, skill/artefacto faltante, plan previo, límites
de no aplica, gates reales del runner con build fallido y código modificado.
El escenario positivo usa reportes sintéticos; no valida aceptación del caso UX.

Los controles verifican consistencia cuando se ejecutan. No autentican el origen
humano del pedido, no prueban lectura cognitiva de skills ni contenido semántico
de documentos. Copilot puede omitir instrucciones: el siguiente piloto debe mostrar
workflow-start, registro de fases y workflow-close. Sin ellos no se acredita cierre.
No se ejecutó Copilot de la otra máquina ni se corrigió el microservicio desde aquí.
