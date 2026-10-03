# Operación del MVP 0.4.0

Copilot usa este repo para completar el perfil y ejecutar checks. JSON se usa en
perfil/política para que los verificadores no dependan de librerías externas.
Si se instala mediante plugin, `backend-preparar-repo` copia/actualiza este soporte al
microservicio con SupportOnly. Huellas en `.assistant-local/backend/installation.json`
protegen personalizaciones. Política/perfil pertenecen al servicio y se preservan.
Python 3.10+ y Git son requisitos de los scripts; PowerShell en Windows. Sin
Python el agente puede trabajar y pedir ejecución manual; la verificación
automática se reporta bloqueada, no se instala Python automáticamente.

## Configuración inicial

`repository-profile.json` llega vacío a propósito. Copilot debe descubrir POM,
perfil/runners y reportes antes de configurarlo, evitando fijar la máquina del
autor. Cree `.assistant-local/backend/toolchain.json` con estos nombres solo si son
necesarios: maven, mavenHome, mavenSettings, mavenRepository y javaHome. Valores son rutas
locales, no secretos. También puede usar mvnw del repo como executable.

Leer [ENTORNO.md](ENTORNO.md) para precedencia y diferencia entre Java del editor
y de Maven. Tras configurar build ejecutar `backend.py doctor --repo .` antes
de acreditar el primer build, al cambiar rutas o si hay errores de toolchain.
Todos los scripts/tests usan stdlib; no hay dependencias pip.

Ejemplo de **forma**, adaptar rutas/perfiles al repo; no copiar como hecho:

```json
{
  "commands": {
    "build": {
      "executable": "${maven}",
      "args": ["-s", "${mavenSettings}", "-Dmaven.repo.local=${mavenRepository}", "clean", "install"],
      "workingDirectory": ".",
      "timeoutSeconds": 1800,
      "gates": ["build", "unit", "checkstyle", "coverage"]
    },
    "karate": {
      "executable": "${maven}",
      "args": ["-s", "${mavenSettings}", "-Dmaven.repo.local=${mavenRepository}", "verify", "-Pcomponent"],
      "gates": ["karate"]
    }
  },
  "reports": {
    "unit": {"kind": "junit-xml", "patterns": ["target/surefire-reports/TEST-*.xml"]},
    "karate": {"kind": "karate-json", "patterns": ["target/karate-reports/karate-summary-json.txt"]},
    "checkstyle": {"kind": "checkstyle-xml", "patterns": ["target/checkstyle-result.xml"]},
    "coverage": {"kind": "jacoco-xml", "patterns": ["target/site/jacoco/jacoco.xml"]}
  }
}
```

Debe integrar estos campos al perfil, no reemplazar otros. `component`, las rutas
y gates son ejemplos. Si build ejecuta Karate inclúyalo en gates; si no, separarlo.
Cuando se ejecuta Karate aparte, impedir que sobrescriba reportes unitarios del
build: usar output dedicado/perfil del repo o asignar los gates al último comando
que realmente ejecute la suite correspondiente. Acreditar con contadores actuales.
Pueden añadirse comandos `unit`, `checkstyle` y `generate`; gates vacíos sirven
para generación. Comandos son ejecutable y args, nunca una cadena shell.

No registrar tokens en args/environment; usa mecanismos corporativos locales
fuera de evidencia. Logs y execution specs permanecen no versionados. El runner
no sanitiza logs crudos: inspeccionarlos localmente y copiar solo extractos limpios.

## Comandos

Desde raíz Git; Windows puede usar `py -3` en lugar de `python`:

```powershell
py -3 engineering/backend/scripts/backend.py snapshot --repo . --output .assistant-local/backend/initial.json
py -3 engineering/backend/scripts/backend.py doctor --repo .
py -3 engineering/backend/scripts/backend.py run --repo . --check build --run-id CAMBIO-001
py -3 engineering/backend/scripts/backend.py run --repo . --check karate --run-id CAMBIO-001
py -3 engineering/backend/scripts/backend.py verify --repo . --run-id CAMBIO-001
py -3 engineering/backend/scripts/backend.py metrics --repo . --base origin/develop
```

`origin/develop` es ejemplo: usar base real. El runner graba exit code, huellas y
reportes; no imprime log crudo. Espera máxima por proceso según perfil, termina
el árbol de procesos del comando al vencer timeout. El asistente debe seguir
dando avances mientras usa una terminal que permita ejecución no bloqueante.

Verify usa última ejecución registrada de cada gate dentro del run ID y compara
contenido actual. Reportes deben haberse regenerado (hash/mtime distinto de antes)
y seguir intactos. Rebuild después de un cambio técnico, no editar manifest para
forzar verde. `.assistant-local` y `docs/engineering` no afectan huella técnica;
otros archivos Git y no ignorados sí. El toolchain local se incluye por hash, sin
copiar su contenido. Declare en `fingerprintInputs` las rutas locales adicionales
que influyen en pruebas, incluso ignoradas (por ejemplo application-local).
Archivos externos, secretos del gestor y servicios externos no se cubren por
huella: registrar esa limitación y verificar overrides cuando influyan en el caso.
El SHA es base de inspección, no prueba
de autorización. No escribir tokens/datos personales en metadata.

## Reportes admitidos y límites

- `junit-xml`: testsuite/testsuites con testcase; cuenta fallos, errors y skipped.
- `karate-json`: summary con scenariosPassed/scenariosFailed; falla con
  featuresFailed. Tags que no seleccionan un escenario no figuran como skipped:
  el dev/agente debe revisar que cubre la matriz esperada.
- `checkstyle-xml`: raíz checkstyle, al menos un file y cero violaciones por default.
  Confirmar que incluye código de tests; el XML solo no prueba configuración.
- `jacoco-xml`: contador INSTRUCTION en raíz, mínimo sin redondeo; BRANCH informativo.
  Módulos pueden sumarse si no se solapan clases. Preferir un agregado del servicio.
  No usar wildcard que capture agregado y módulos. Revisar exclusiones y alcance.

Gate build exige clean/install, exit 0 y entrada técnica sin modificaciones en el
comando; rechaza flags conocidos de omisión/selección parcial. El POM puede tener
skips encubiertos o suites faltantes: revisar bindings/effective POM y criterios
funcionales. Los scripts no son sandbox ni controles anti-manipulación; evidencias
locales pueden alterarse. CI/revisión humana confirman contenido final y política.

`notApplicable` solo se admite para gate que de verdad no aplica y contiene
reason, approvedBy y trackingReference corporativos. Build/cobertura no se omiten
por este mecanismo. Un pedido de skill individual no necesita verify completo:
presenta resultado del check y `SCOPED_TASK_DONE`, con gates ajenos NOT_RUN.

## Estado y documentación

El agente inicia un expediente ejecutable después de preparar el soporte. Ejemplo
(reemplazar tarea/rutas; comandos Python con biblioteca estándar):

```powershell
py -3 -S engineering/backend/scripts/backend.py workflow-start --repo . --task CAMBIO-1 --request-file .assistant-local/backend/CAMBIO-1/request.txt
py -3 -S engineering/backend/scripts/backend.py workflow-phase --repo . --task CAMBIO-1 --phase 2 --status DONE --skill '<ruta real>/backend-plan/SKILL.md' --evidence docs/engineering/changes/CAMBIO-1/plan.md
py -3 -S engineering/backend/scripts/backend.py workflow-close --repo . --task CAMBIO-1 --run-id CAMBIO-1 --acceptance-evidence '<reporte o documento del escenario>'
```

El pedido se guarda localmente, fiel al texto humano, sin logs/secretos. Modo
complete predeterminado; individual solo con --mode individual --scope-quote
literal del pedido que delimita alcance. El script comprueba la cita contra el
archivo, no puede autenticar su origen humano. No reenviar ese archivo al repo.
Las fases DONE necesitan artefactos no vacíos y archivos de skills; contrato/config
permiten NOT_APPLICABLE con --reason. BLOCKED necesita la dependencia concreta.
En modo completo el cierre comprueba ocho fases, hashes de evidencias/skills,
mapa/bitácora y evidencia de aceptación; vuelve a ejecutar verify del run indicado.
En modo individual basta la capacidad solicitada con evidencias vigentes;
no exige gates ajenos. Reanudar el mismo expediente, sin sustituir su alcance.

El registro no demuestra lectura cognitiva ni corrección semántica de artefactos.
No impide que Copilot omita herramientas: sin resultado de workflow-close no
declarar LOCAL_VERIFIED. La UI puede mostrar lectura de archivos en lugar de
invocación nativa; registrar rutas, no simular llamadas a skills.

State del chat: `.assistant-local/backend/<ticket>/state.json`, con modo, fase, próximo
paso, archivos propios y bloqueos. Evidencia: `runs/<run-id>`, generada por runner.
Compartido: `docs/engineering/service-map.md`, metadata de snapshot y expediente
`changes/<ticket>`. Templates están en `engineering/backend/templates`.

Calidad local PASS no acredita CI, Sonar, aceptación semántica, traslado manual,
aprobación humana o despliegue. Informar cada resultado con su alcance y pendiente.
