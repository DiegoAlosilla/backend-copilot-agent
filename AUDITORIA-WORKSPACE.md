# Anexo: archivos del workspace y candidatos de limpieza

Foto del 3 de octubre de 2026 de la carpeta de trabajo superior al repositorio.
Este documento complementa [INVENTARIO.md](INVENTARIO.md). Las rutas siguientes
son relativas a esa carpeta superior; **no son archivos distribuidos por el
plugin backend-java**. No se eliminó ninguno.

## Conteo observado antes de documentar

| Ubicación | Fuentes/documentos/artefactos | Cachés Python | Relación con paquete actual |
| --- | --- | --- | --- |
| `backend-copilot-agent/` | 47 | 5 | Repositorio principal; inventario individual en INVENTARIO |
| `agente-bcp-copilot/` | 46 | 2 | Paquete anterior 0.2.0 con nombres BCP y repositorio Git local propio |
| `propuesta-agente-bcp/` | 2 | 0 | Diseño inicial del piloto |
| `revision-plugin/` | 5 | 0 | Muestras TypeScript de implementación/pruebas de descubrimiento de plugins |
| Raíz superior | 13 | 0 | 6 ZIP, 4 bundles Git y 3 notas de versión |
| **Total** | **113** | **7** | **120 archivos físicos, excluyendo metadata .git** |

La entrega documental añade dos Markdown en el repositorio principal: 122
archivos físicos si no se generan más cachés. La metadata `.git/` de ambos
checkouts se registra como carpeta técnica; no se enumera ni publica su contenido.
No se encontraron requisitos de ejecución del paquete actual que apunten a las
otras tres carpetas o a los ZIP/bundles/notas de la raíz superior.

## Paquete anterior: agente-bcp-copilot

Cada fila es un archivo observado. La criticidad indica el impacto **si alguien
todavía utiliza 0.2.0**. Para backend-java actual, todos tienen impacto directo
nulo porque no están referenciados por sus fuentes. Antes de retirar la carpeta
completa, confirmar adopción y respaldar su historia Git y cambios propios.

| Ruta dentro de `agente-bcp-copilot/` | Función | Criticidad en 0.2.0 | Consecuencia al eliminar / capacidad afectada |
| --- | --- | --- | --- |
| `plugin.json` | Manifest bcp-backend 0.2.0, declara agente/skills/prompts | Crítica | Rompe descubrimiento del paquete anterior |
| `README.md` | Instalación y uso del MVP BCP | Media | Se pierde guía de usuarios antiguos |
| `CHANGELOG.md` | Evolución histórica BCP | Media | Se pierde trazabilidad del MVP |
| `VALIDACION.md` | Ensayos/piloto de la versión anterior | Media | Se pierde evidencia histórica, no valida el paquete actual |
| `MANIFEST.sha256` | Huellas de distribución antigua | Media | Se pierde comprobación manual de integridad histórica |
| `Install-Bcp.ps1` | Wrapper del instalador BCP | Crítica para instalar | Preparación antigua deja de encontrar la entrada |
| `requirements-dev.txt` | PyYAML 6.0.3 para validador de desarrollo antiguo | Alta para CI antiguo | `check_package.py` antiguo importa yaml; no es requisito del backend-java actual |
| `.gitignore` | Exclusiones de cachés/evidencias/paquetes/venv | Alta para mantenimiento | Facilita incorporación de artefactos locales en el repo antiguo |
| `.gitattributes` | Normalización de texto | Media | Aumentan diferencias de finales de línea/hashes |
| `.github/copilot-instructions.md` | Reglas generales BCP | Alta | Agente y skills antiguas pierden reglas comunes |
| `.github/agents/bcp-backend.agent.md` | Orquestador BCP antiguo | Crítica | Se pierde el agente antiguo de cambio completo |
| `.github/prompts/bcp-cambio.prompt.md` | Entrada `/bcp-cambio` asociada a bcp-backend | Alta para entrada antigua | Se pierde ese comando; el paquete actual inicia con el agente directamente |
| `.github/workflows/validate-agent.yml` | CI antigua y pip de requirements-dev | Alta para mantenimiento | Se pierde comprobación de ese paquete |
| `.github/skills/bcp-preparar-repo/SKILL.md` | Preparación de soporte engineering/bcp | Crítica para preparación | Afecta preparación de todas las skills BCP antiguas |
| `.github/skills/bcp-contexto/SKILL.md` | Contexto y perfil del servicio | Alta | Se pierde diagnóstico inicial antiguo |
| `.github/skills/bcp-evidencias/SKILL.md` | Correlación de fuentes/logs | Alta | Se pierde investigación guiada antigua |
| `.github/skills/bcp-plan/SKILL.md` | Plan y matriz de impacto | Alta | Se pierde planificación antigua |
| `.github/skills/bcp-contrato/SKILL.md` | Fuente contractual/generación | Alta | Se pierde procedimiento de contratos antiguo |
| `.github/skills/bcp-implementacion/SKILL.md` | Implementación Java | Alta | Se pierde procedimiento de cambio antiguo |
| `.github/skills/bcp-errores-http/SKILL.md` | Traducción Business→UX | Alta | Se pierde capacidad HTTP antigua |
| `.github/skills/bcp-pruebas-unitarias/SKILL.md` | JUnit/Mockito y cobertura | Alta | Se pierde capacidad de unitarias antigua |
| `.github/skills/bcp-karate/SKILL.md` | Componente HTTP | Alta | Se pierde capacidad Karate antigua |
| `.github/skills/bcp-kafka/SKILL.md` | Eventos Kafka | Alta en Kafka | Se pierde capacidad de mensajería antigua |
| `.github/skills/bcp-config-manual/SKILL.md` | Traslado manual por ambiente | Alta | Se pierde preparación Config Maps antigua |
| `.github/skills/bcp-calidad/SKILL.md` | Verificación de calidad | Crítica para cierre antiguo | Se pierde procedimiento de gates antiguo |
| `.github/skills/bcp-memoria/SKILL.md` | Memoria/diagramas del servicio | Alta | Se pierde continuidad documental antigua |
| `.github/skills/bcp-commits/SKILL.md` | Métricas y entrega | Alta | Se pierde procedimiento de commits antiguo |
| `.github/skills/bcp-sanity/SKILL.md` | Smoke independiente | Alta para smoke | Se pierde capacidad sanitaria antigua |
| `distribution/Install-Managed.ps1` | Instalación gestionada antigua | Crítica | Wrapper/preparación antigua dejan de instalar; no usar para instalar backend-java |
| `distribution/check_package.py` | Validación antigua con PyYAML | Alta para mantenimiento | CI antigua falla o pierde control; no sustituye al validador plano actual |
| `distribution/GIT-Y-VSCODE.md` | Distribución del MVP anterior | Media | Se pierde orientación histórica de instalación |
| `distribution/vscode-user-settings.jsonc` | Ejemplo de ajustes de VS Code | Media | Se pierde ejemplo, reproducible desde documentación |
| `engineering/bcp/OPERACION.md` | Guía del runtime anterior | Alta | Se pierden instrucciones operativas del paquete antiguo |
| `engineering/bcp/ESTANDAR-JAVA.md` | Convenciones Java antiguas | Alta | Implementación/unitarias BCP pierden referencia |
| `engineering/bcp/repository-profile.json` | Comandos/reportes del servicio | Crítica | Runtime antiguo no lee un perfil válido |
| `engineering/bcp/quality-policy.json` | Gates/umbrales antiguos | Crítica | Runtime antiguo pierde política de verificación |
| `engineering/bcp/scripts/bcp.py` | Runtime anterior: snapshot/run/verify/metrics | Crítica | Se pierde verificación automática antigua; no tiene los ocho subcomandos actuales |
| `engineering/bcp/scripts/Invoke-Command.ps1` | Ejecución Windows del runtime antiguo | Crítica en Windows | Runner antiguo no ejecuta por esa vía |
| `engineering/bcp/references/CASO-204.md` | Guía del piloto HTTP | Alta para HTTP | bcp-errores-http pierde referencia |
| `engineering/bcp/references/COMMITS.md` | Convención/métricas | Alta para entrega | bcp-commits pierde referencia |
| `engineering/bcp/references/CONFIG-MAPS.md` | Recorrido de configuración | Alta para configuración | bcp-config-manual pierde referencia |
| `engineering/bcp/templates/CAMBIO.md` | Plantilla del cambio antigua | Media | Plan/memoria antiguos pierden estructura |
| `engineering/bcp/templates/SERVICE-MAP.md` | Plantilla de mapa | Media | Memoria antigua pierde estructura |
| `engineering/bcp/templates/REFERENCIAS.md` | Plantilla de fuentes | Media | Evidencias antiguas pierden estructura |
| `engineering/bcp/templates/CONFIG-HANDOFF.md` | Plantilla de traslado | Media | Configuración antigua pierde estructura |
| `tests/test_runtime.py` | Pruebas del runtime/instalador antiguos | Alta para mantenimiento | Se pierden regresiones del paquete anterior |

## Propuestas y muestras TypeScript

| Ruta desde raíz superior | Función observada | Criticidad para backend-java actual | Consecuencia al eliminar / recomendación |
| --- | --- | --- | --- |
| `propuesta-agente-bcp/PROPUESTA.md` | Diseño inicial, decisiones y alcance del piloto | Baja operativa; media histórica | No rompe skills; archivar como diseño histórico si su trazabilidad se conserva |
| `propuesta-agente-bcp/PLANTILLAS.md` | Plantillas conceptuales del piloto, incluidas estructuras aún no operativas | Baja operativa; media histórica | No rompe skills; no confundir con templates vigentes |
| `revision-plugin/agentPluginService.ts` | Interfaces y tipos del servicio de plugins de VS Code | Baja operativa | No es parte del plugin; se pierde referencia de investigación |
| `revision-plugin/agentPluginServiceImpl.ts` | Implementación de descubrimiento/servicio de plugins | Baja operativa | No se ejecuta desde este paquete; se pierde referencia del cliente |
| `revision-plugin/pluginParsers.ts` | Parsers de manifest, skills, reglas y otros componentes | Baja operativa | No valida este repo por sí mismo; se pierde muestra de análisis |
| `revision-plugin/agentPluginFormatDetection.test.ts` | Tests de detección de formatos del cliente | Baja operativa | No los ejecuta la CI Python del paquete; se pierde muestra de investigación |
| `revision-plugin/configuredAgentPluginDiscovery.test.ts` | Tests de plugins configurados del cliente | Baja operativa | Igual: pruebas del cliente, no del agente |

Las muestras TypeScript tienen imports hacia el árbol interno de VS Code y no
se encontró aquí su proyecto de compilación completo. No son un backend
adicional ni dependencias Java/Python. Mantenerlas como referencia exige registrar
procedencia/commit; de otro modo su vigencia no es demostrable. Las propuestas
contienen decisiones antiguas, como memoria versionada, que no sustituyen el
comportamiento local de 0.6.0.

## Artefactos de distribución y notas en la raíz superior

Se leyeron directorios de ZIP y referencias de bundles, sin extraer ni ejecutar
su contenido. Las cantidades de ZIP son entradas de archivo, no tests aprobados.

| Archivo | Función / contenido | Criticidad directa actual | Si se elimina / recomendación |
| --- | --- | --- | --- |
| `agente-bcp-copilot-v0.1.0.zip` | Snapshot de 35 archivos del primer paquete | Baja | No afecta agente instalado; se pierde entrega histórica; conservar copia externa antes de limpiar |
| `agente-bcp-copilot-v0.2.0.zip` | Snapshot de 46 archivos del paquete BCP anterior | Baja | Igual; no reemplaza historial Git |
| `agente-bcp-copilot-v0.2.0.bundle` | Historia/referencias Git antiguas, incluye main y tag v0.2.0 | Baja operativa; media de recuperación | Se pierde vía offline de restauración; confirmar respaldo del repo antiguo |
| `backend-copilot-agent-v0.3.0.zip` | Snapshot de 47 archivos de versión 0.3.0 | Baja | No afecta runtime activo; se pierde snapshot histórico |
| `backend-copilot-agent-v0.3.0.bundle` | Historia/referencias hasta main 9e0c886 y tag v0.3.0 | Baja operativa; media de recuperación | Se pierde recuperación offline; evaluar si bundle posterior conserva lo necesario |
| `backend-copilot-agent-v0.4.0.zip` | Snapshot de 46 archivos de versión 0.4.0 | Baja | No afecta runtime activo; se pierde snapshot histórico |
| `backend-copilot-agent-v0.4.0.bundle` | Historia/referencias hasta main 70cb319 y tags 0.3.0/0.4.0 | Baja operativa; media de recuperación | Se pierde copia offline de esa entrega |
| `backend-copilot-agent-v0.5.0.zip` | Snapshot de 47 archivos de versión 0.5.0 | Baja | No afecta runtime activo; conservar rollback si está en adopción |
| `backend-copilot-agent-v0.5.0.bundle` | Historia/referencias hasta main c1d7d25 y tags 0.3.0–0.5.0 | Baja operativa; media de recuperación | No contiene por sí solo cambios locales pendientes de 0.6.0 |
| `backend-copilot-agent-v0.6.0.zip` | Snapshot de 47 archivos del paquete local 0.6.0, previo a esta documentación | Baja operativa; alta como entrega pendiente | No publica una versión Git; conservar hasta respaldar/publicar los cambios 0.6.0 por separado |
| `release-notes-backend-v0.3.0.md` | Notas de entrega 0.3.0 | Baja operativa; media histórica | No afecta skills; archivable si release/changelog conserva información |
| `release-notes-backend-v0.4.0.md` | Notas de entrega 0.4.0 | Baja operativa; media histórica | Igual |
| `release-notes-backend-v0.5.0.md` | Notas de entrega 0.5.0 | Baja operativa; media histórica | Igual |

## Cachés observadas: cada archivo

| Ruta desde raíz superior | Función | Criticidad | Si se elimina |
| --- | --- | --- | --- |
| `backend-copilot-agent/distribution/__pycache__/check_package.cpython-314.pyc` | Bytecode del validador | Baja | Python vuelve a compilar la fuente; no se pierde su procedimiento |
| `backend-copilot-agent/engineering/backend/scripts/__pycache__/backend.cpython-314.pyc` | Bytecode del runtime | Baja | Igual; conservar backend.py fuente |
| `backend-copilot-agent/tests/__pycache__/test_package.cpython-314.pyc` | Bytecode de pruebas de parser | Baja | Igual; conservar test_package.py |
| `backend-copilot-agent/tests/__pycache__/test_runtime.cpython-314.pyc` | Bytecode de pruebas de runtime | Baja | Igual; conservar test_runtime.py |
| `backend-copilot-agent/tests/__pycache__/test_workflow.cpython-314.pyc` | Bytecode de pruebas del flujo | Baja | Igual; conservar test_workflow.py |
| `agente-bcp-copilot/engineering/bcp/scripts/__pycache__/bcp.cpython-314.pyc` | Bytecode del runtime antiguo | Baja | Se regenera si se vuelve a usar ese paquete |
| `agente-bcp-copilot/tests/__pycache__/test_runtime.cpython-314.pyc` | Bytecode de tests antiguos | Baja | Se regenera si se vuelven a ejecutar |

Las cachés son dinámicas y están ignoradas por Git. Un inventario de una futura
ejecución puede tener otros nombres/versiones o cantidades; no actualizarlas
como si fueran catálogo obligatorio del plugin.

## Orden sugerido de limpieza posterior

1. Cachés Python: impacto bajo y regenerables. Esta auditoría no las borra.
2. ZIP/bundles viejos: mover a un archivo de entregas después de verificar
   respaldo e historia; conservar 0.6.0 pendiente.
3. Muestras TypeScript/propuesta: archivar por procedencia, separados de la fuente.
4. Paquete BCP anterior: confirmar que nadie lo instala/actualiza desde esa copia;
   respaldar historial y personalizaciones antes de retirar el checkout.
5. Paquete vigente: consolidar duplicación documental; cualquier retiro de skills,
   runtime, instalador o tests requiere su propia migración y validación.

No se propone retirar Python/PowerShell por su extensión. Se propone retirar o
archivar únicamente cuando su responsabilidad desaparezca o esté sustituida.
