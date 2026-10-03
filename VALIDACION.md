# Validación de la entrega 0.3.0

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

Se comprobó el frontmatter de las **15 skills**, agente y prompt, además de JSON,
nombres, referencias internas y sintaxis Python. Todos los scripts/checks usan
biblioteca estándar. `py -3 -S distribution/check_package.py` pasó.

`distribution/check_package.py` valida el manifest Copilot y 17 definiciones
(15 skills, agente y prompt). El workflow de CI se incluyó para ejecutar estos
checks cuando se publique en GitHub; aún no se ejecutó en servidor remoto.

Las fixtures simulan reportes; no son pruebas de Quarkus/Karate de un servicio
empresarial. No se probó descubrimiento en VS Code corporativo ni el modelo real,
Maven/Artifactory, CI/Sonar o Grafana. Instalación desde fuente y ciclo automático
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
