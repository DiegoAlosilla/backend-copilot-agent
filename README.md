# Backend Java Agent

Versión **0.8.0**. Un agente orquestador y **15 skills** para
soporte, auditorías e implementaciones Java con Quarkus/Spring. El desarrollador
selecciona `backend-java` en Copilot y describe lo que necesita.

## Estructura

```text
backend-copilot-agent/
  plugin.json
  agents/backend-java.agent.md
  skills/<capacidad>/SKILL.md
  skills/backend-calidad/scripts/       # verificador opcional Maven/reportes
  skills/backend-calidad/references/    # política por servicio y uso en CI
  evaluations/                         # protocolo de piloto del agente
  scripts/Measure-AgentEvaluation.ps1
  tests/Test-Harness.ps1
  README.md
  CHANGELOG.md
```

Las reglas comunes están en el agente; cada skill contiene sus criterios propios.
El editor conserva el runtime del agente. Las validaciones usan el JDK,
Maven/wrapper, Git y herramientas existentes del microservicio. El paquete añade
un verificador opcional para PowerShell 5.1/7 y un medidor de evaluaciones humanas,
sin módulos externos, Python, Node ni Docker. Si no puede ejecutar scripts, el
agente comprueba los mismos gates manualmente y declara el método y sus límites.

## Dos opciones de instalación

Elige **una** para evitar agentes y skills duplicados. Instala fuera del
microservicio; no copia soporte ni modifica sus instrucciones o ignores.

### 1. Plugin dentro de VS Code

Para probar esta copia local ahora, integra estas claves en **User Settings (JSON)**,
conservando los ajustes existentes:

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "D:/AgenteBCP/backend-copilot-agent": true
  }
}
```

Si ya tienes `chat.pluginLocations`, agrega solo esta entrada. Abre un chat nuevo,
selecciona `backend-java` y comprueba que carga la versión local. Deshabilita una
copia anterior del mismo plugin mientras haces el piloto.

Para distribuir la versión **después de publicarla en el repositorio**, ejecuta
**Chat: Install Plugin From Source** e indica
`https://github.com/DiegoAlosilla/backend-copilot-agent.git`. Instalar desde esa URL
usa lo publicado, no estos cambios locales. Las políticas del banco pueden
gestionar disponibilidad y acceso al repositorio privado.

Se conserva el formato Copilot de `plugin.json`, compatible con `agents/` y
`skills/`. No agregar el schema de Agent Plugins 1.0 sin migrar también sus rutas.
[Plugins y rutas locales en VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

### 2. Archivos personales en ~/.copilot

En Windows, `~/.copilot` corresponde a `%USERPROFILE%\.copilot`. En WSL/SSH usa
la carpeta del usuario del host donde se ejecuta Copilot.

Con el explorador de archivos:

1. Copia `agents/backend-java.agent.md` a `~/.copilot/agents/`.
2. Copia las 15 carpetas `skills/backend-*` a `~/.copilot/skills/`, conservando
   cada `SKILL.md` y sus subcarpetas `scripts/` y `references/` cuando existan.
   Integra las carpetas sin reemplazar otras personalizaciones.
3. Abre un chat nuevo y selecciona `backend-java`.

No copies `plugin.json`, README o CHANGELOG a `.copilot`. Para actualizar reemplaza
solo los archivos de este agente; revisa diferencias si los personalizaste.
No necesitas instalarlo también como plugin. Los paths relativos agente→skills
funcionan con la misma estructura en ambas opciones.
[Agentes personales](https://code.visualstudio.com/docs/agent-customization/custom-agents),
[skills personales](https://code.visualstudio.com/docs/agent-customization/agent-skills).

## Cómo trabaja

Un único flujo: **entorno/contexto → diagnóstico e hipótesis → plan → contrato e
implementación → pruebas → configuración → calidad → entrega**. Se evalúan todas
las fases y se justifican las que no corresponden al pedido. Auditar entrega
diagnóstico y plan; corregir incluye modificación y validación. El agente no
expande el alcance de una auditoría para aplicar cambios sin autorización.

Antes de editar muestra sospechas, archivos afectados, pruebas, comandos/gates
y riesgos. Pregunta por ambigüedades o rutas corporativas necesarias mediante
las preguntas de Copilot cuando la herramienta esté disponible, o en texto.
No exige comandos slash: las skills están ocultas del menú `/` mediante
`user-invocable: false` y siguen disponibles para el orquestador.

Java/Maven/settings y preferencias se conservan como `CONTEXTO_BACKEND` con
memoria nativa del editor. Si no existe persistencia nativa, usa un único archivo
personal `~/.copilot/backend-java-context.md`. Es contexto lógico persistido,
no una variable global del sistema. Las selecciones vigentes se reutilizan y se
revalida lo que cambie entre proyectos/hosts. No se almacenan credenciales.
[Memoria de VS Code](https://code.visualstudio.com/docs/agents/run/memory).

Plan y matriz de aceptación permanecen en chat/memoria. Si se usa el verificador,
su política y evidencia JSON se guardan fuera del servicio. El agente no crea `.engineering`,
`.assistant-local`, perfiles, bitácoras o scripts dentro del microservicio, ni
altera ignores para ocultarlos. Solo una petición expresa de documentar/crear
contexto técnico genera documentación en el destino acordado. Maven conserva sus
reportes habituales en `target/`; código, contratos y pruebas sí pueden cambiar.

La entrega incluye una tabla de commits propuestos: propósito, archivos/hunks,
mensajes y validaciones. **Espera aprobación de esa agrupación antes de stage/commit.**
Push, PR y despliegue requieren alcance adicional. Puede entregar el diff probado
para revisión mientras la aprobación sigue pendiente.

Si vence GitHub, distingue autenticación de permisos/red y da al desarrollador
el comando de login por navegador del host correcto. Reanuda tras recuperar acceso
y conserva avances locales. No requiere `gh` para tareas locales ni instala esa
herramienta por su cuenta.

## Skills que orquesta

| Skill | Responsabilidad |
| --- | --- |
| backend-entorno | Toolchain, rutas reutilizables y autenticación |
| backend-contexto | Arquitectura y recorrido real del servicio |
| backend-evidencias | Hechos, logs correlacionados e hipótesis |
| backend-plan | Aceptación, impacto, ejecución y validaciones |
| backend-contrato | Fuente contractual, compatibilidad y generación |
| backend-implementacion | Cambio Java con patrones del repo |
| backend-errores-http | Traducción Business→UX y regresiones |
| backend-pruebas-unitarias | JUnit/Mockito y escenarios significativos |
| backend-karate | Componente/HTTP y resultados reales |
| backend-kafka | Schemas, eventos y semántica de entrega |
| backend-config-manual | Delta DEV/CERT/PROD para traslado manual |
| backend-calidad | Build, suites, Checkstyle y JaCoCo |
| backend-sanity | Smoke/health funcional cuando corresponde |
| backend-memoria | Contexto externo y documentación explícita |
| backend-commits | Agrupación, aprobación y commits autorizados |

## Piloto en tu microservicio

```text
Audita este problema: UX devuelve un error genérico cuando Business informa
una ausencia que debería resultar en HTTP 204 sin cuerpo. Revisa contrato,
código y logs adjuntos; presenta hechos, sospechas y un plan con pruebas.
```

Después de revisar el plan:

```text
Implementa la corrección, ejecuta las validaciones aplicables y propón commits
agrupados. Config Maps queda manual. Espera mi aprobación de la agrupación.
```

Comprueba estos comportamientos en Copilot:

| Escenario | Resultado esperado |
| --- | --- |
| Auditoría | Diagnóstico/hipótesis/plan en chat; sin editar código ni crear carpetas |
| Corrección Java | Plan previo, cambio, regresión, build final y evidencia de gates |
| Rutas especiales | Pregunta lo faltante, reutiliza selección en fases y chats siguientes |
| GitHub expirado | Login por navegador del cliente correcto; conserva punto de reanudación |
| Entrega | Grupos concretos; ningún stage/commit antes de aprobarlos |
| Documentación expresa | Archivos solo en ubicación existente/acordada, sin expedientes extra |

Política mantenida: INSTRUCTION global ≥95%, cero tests omitidos y cero violaciones
Checkstyle, respetando política más exigente o excepciones expresas del servicio.
Karate/Kafka/sanity se aplican según requisitos e infraestructura reales.

Estas son instrucciones que dirige Copilot; no incluyen un runtime que imponga
todo el flujo. El verificador impone los gates declarados al ejecutarse y devuelve
exit 1 si no puede acreditarlos. Los resultados se respaldan con comandos y
reportes reales del proyecto; su alcance y significado funcional requieren revisión.
La carga y el comportamiento en el Copilot corporativo deben comprobarse en el
piloto; un README o una revisión estática no demuestran esa ejecución.

## Harness sobre el flujo SDD

- Cada criterio AC vincula especificación/contrato → comportamiento → test →
  resultado y evidencia. Cobertura alta no sustituye aceptación funcional.
- El checkpoint conserva alcance, fase, siguiente acción, diff y bloqueos en la
  memoria existente. Al reanudar se invalidan los resultados afectados por cambios.
- El [verificador](skills/backend-calidad/references/harness.md) ejecuta Maven y
  verifica JUnit, Checkstyle y JaCoCo actuales, incluyendo aceptación y hashes de
  fuentes/reportes. `-VerifyOnly` detecta evidencia invalidada sin ejecutar el build.
- Los [ocho casos de evaluación](evaluations/README.md) permiten comparar versiones
  con el mismo modelo y fixture. El medidor calcula resultados registrados por un
  revisor; no simula una ejecución de Copilot ni atribuye eficacia sin un piloto.

La política de ejemplo se adapta al POM/CI real y a todos los módulos/suites del
servicio. Los reportes custom o gates externos pendientes no se convierten en
aprobados. No se instala soporte en el microservicio ni se altera su CI sin una
adopción específica; la guía explica cómo convertir el comando en check obligatorio.

Para comprobar las herramientas del paquete con fixtures sintéticos:

```powershell
pwsh -NoProfile -File ./tests/Test-Harness.ps1
```

Prueba opcional con Java 17+, Git y Maven reales (descarga artefactos públicos
en un repositorio Maven temporal, con settings vacíos y sin usar credenciales):

```powershell
pwsh -NoProfile -File ./tests/Test-MavenIntegration.ps1
```

Usa un proyecto Java sintético, no un microservicio BCP. No acredita HTTP real
ni el comportamiento del agente. Requiere una política del host que permita scripts.

El workflow `.github/workflows/harness.yml` comprueba esas herramientas en el
repositorio del paquete. Su ejecución remota y la protección de ramas solo se
acreditan tras publicar y verificar GitHub; no prueban un microservicio bancario.
Los resultados locales y sus límites están en [VALIDATION.md](VALIDATION.md).

## Migración desde versiones anteriores

Actualiza agente y skills por una de las dos opciones, y abre un chat nuevo.
Desde 0.7.0 copia también los recursos de `backend-calidad`; conservar solo su
`SKILL.md` deja el verificador inaccesible. Los evaluadores del paquete son
opcionales para el mantenedor y no se copian al servicio. No instales dependencias
ni cambies políticas de ejecución corporativas para habilitarlos.
En instalación por archivos retira únicamente la antigua skill
`backend-preparar-repo` del paquete; conserva personalizaciones ajenas.
Deshabilita duplicados del agente anterior para evitar que sus reglas se mezclen.

Si un piloto anterior creó soporte o memoria en un microservicio, revisa primero
su contenido y conserva las evidencias útiles fuera del proyecto antes de retirar
solo los artefactos de ese piloto. Esta versión no los borra automáticamente ni
necesita instalar soporte. No se ha intervenido ningún microservicio al actualizar
este paquete local.
