# Backend Java Agent para GitHub Copilot

Versión **0.5.0**: un agente principal y **15 skills** para cambios Java completos
o tareas individuales. Usa Quarkus/Spring y la arquitectura real del repositorio.

Consulta el [inventario y criticidad](INVENTARIO.md), el
[anexo de limpieza del workspace](AUDITORIA-WORKSPACE.md) y los
[ejemplos de las 15 skills](#uso-ejemplo-y-resultado-esperado-de-cada-skill).

## Cómo usarlo

Seleccionar **backend-java** en Copilot y escribir la solicitud en texto normal.
**No hace falta un prompt ni un slash para iniciar un cambio completo.**

```text
Este UX devuelve error genérico cuando Business informa que no
se encontró lo buscado. Debe responder HTTP 204 sin cuerpo solo en ese escenario.
Adjunto logs y contrato. Corrige el problema y completa las fases con pruebas,
clean install, cobertura y memoria. Muéstrame la skill cargada y evidencia de
cada fase. Config Maps manual; no hagas push ni despliegue.
```

El modo completo es el predeterminado al pedir corregir/implementar un cambio.
“Solo unitarias”, “solo diagnóstico” o una petición individual delimitada activa
únicamente ese alcance. Una corrección pequeña sigue necesitando calidad y memoria
cuando se pidió el cambio completo.

Para usar una skill individual, escribir `/` y seleccionar su nombre. VS Code
puede mostrar el nombre del plugin junto al nombre de la skill, por ejemplo
`/backend-java backend-plan`. Ese prefijo es normal; no es otra skill.
También puede escribirse “Solo backend-plan: prepara el plan de este cambio”.

## Qué deberías ver en un flujo completo

Antes de cada fase, el agente anuncia su número y skills, carga sus instrucciones
y ejecuta las acciones. Ejemplo: `[2/8] Plan — skills: backend-plan`.
Después indica resultado y evidencia, no solo que “usó” una skill.

| Fase | Skills | Evidencia esperada |
| --- | --- | --- |
| 1. Contexto/evidencias | contexto, evidencias | Flujo, perfil, causas/hipótesis y baseline viable |
| 2. Plan | plan | Matriz de clases/métodos, contrato, config y pruebas |
| 3. Contrato | contrato si aplica | Fuente/regeneración o motivo de no cambio |
| 4. Implementación | implementación, errores-http si aplica | Causa corregida y regresión definida |
| 5. Pruebas | unitarias, Karate; Kafka si aplica | Ejecuciones y resultados de suites significativas |
| 6. Configuración | config-manual si aplica | Delta por ambiente o no requerido con razón |
| 7. Calidad | calidad | clean install, informes actuales y verify |
| 8. Memoria/entrega | memoria, commits en preparación | Diagramas, bitácora, métricas y mensaje propuesto |

La trazabilidad queda en `docs/engineering/changes/<tarea>/change.md`. El cierre
incluye tabla de fases, gates y pendientes. La preparación del repo aparece antes
del flujo si hace falta soporte; no sustituye ninguna fase funcional.

`LOCAL_VERIFIED` acredita el cierre completo local. Si faltan build/tests,
preparación o evidencia, el modo completo queda `BLOCKED`, conservando los avances.
`SCOPED_TASK_DONE` corresponde exclusivamente a una tarea individual.
CI/revisión humana/traslado de configuración y producción se reportan aparte.

Desde 0.5.0 el agente registra el alcance y las fases mediante `backend.py
workflow-start`, `workflow-phase` y `workflow-close`. El último comando rechaza
un cierre completo con fases ausentes, artefactos modificados o gates pendientes,
y vuelve a verificar las ejecuciones actuales. El registro está en
`.assistant-local/backend/workflows/<tarea>/workflow.json`.
Un modo individual requiere una cita del pedido que limita el alcance;
el agente no debe inventarla a partir de su anuncio de auditoría.

Estos controles operan **cuando se ejecutan**: el plugin de instrucciones no
intercepta todas las respuestas de Copilot ni puede impedir que omita un comando.
Un cierre sin resultado del verificador no acredita finalización. Los hashes
prueban consistencia de archivos, no que el modelo entendió una skill, que una cita
proviene realmente del humano o que las pruebas cubren el comportamiento correcto.
El desarrollador revisa la aceptación y las evidencias antes de aprobar el cambio.

Una skill contiene instrucciones: Copilot puede cargarla con una herramienta
nativa o leyendo el SKILL.md. Eso no crea necesariamente un subagente ni una
burbuja idéntica en todas las versiones. La carga real, las acciones y sus
artefactos sí deben poder comprobarse.
[Cómo carga skills VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills).

## Instalar o actualizar

1. Tener acceso al repositorio privado en Git/VS Code. Para otros desarrolladores,
   conceder acceso primero. No insertar tokens en URLs o settings.
2. Integrar en **User Settings (JSON)** sin reemplazar otras claves:

   ```json
   {
     "chat.plugins.enabled": true,
     "extensions.autoUpdate": true
   }
   ```

3. Ejecutar **Chat: Install Plugin From Source** e indicar:

   ```text
   https://github.com/DiegoAlosilla/backend-copilot-agent.git
   ```

4. Abrir la raíz Git del microservicio y seleccionar **backend-java**.

Para pasar desde una versión anterior a 0.5.0, ejecutar **Extensions: Check for Extension Updates**,
comprobar la versión y abrir un chat nuevo. El comando `backend-cambio.prompt` se
retiró: usar el agente directamente. Si persiste un comando antiguo, comprobar
que la actualización llegó y que no hay copias del workspace ocultando el plugin.
No borrar personalizaciones para resolverlo.

VS Code comprueba actualizaciones cada 24 horas con `extensions.autoUpdate`
habilitado; respetar políticas gestionadas. También afecta otras extensiones.
[Documentación oficial](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

El plugin actualiza agente/skills/reglas. La próxima sesión prepara soporte en
`engineering/backend`, preservando perfil, política y memoria del servicio.
Archivos personalizados se detectan antes de copiar. Revisar el diff de soporte
antes de versionarlo. Un conflicto es pendiente concreto, no un permiso para
ignorar pruebas o declarar el cambio completo.

## Qué hace cada carpeta

| Carpeta/archivo | Para qué sirve | Quién lo usa |
| --- | --- | --- |
| `agents/backend-java.agent.md` | Decide alcance, carga skills y dirige fases | Copilot al seleccionar el agente |
| `skills/<nombre>/SKILL.md` | Procedimiento especializado y referencias de la fase | Copilot según la fase o petición individual |
| `rules/backend.instructions.md` | Reglas compartidas del agente/skills | Plugin o lectura explícita; respeta reglas del servicio |
| `engineering/backend` | Verificadores, perfil, política, templates y referencias | Skills que necesitan pruebas, memoria o configuración |
| `distribution` e `Install-Backend.ps1` | Preparación/actualización y alternativa por archivos | Instalador; no es otra ruta de negocio |
| `tests` y `.github/workflows` | Ensayos y CI del propio paquete | Mantenedores; no son pruebas de tu microservicio |

No se cargan todos esos archivos a la vez. El plugin registra agente/skills/reglas;
los otros recursos se leen únicamente cuando el procedimiento los requiere.
`CASO-204.md` es una referencia de HTTP 204, no un segundo agente ni regla universal.

Las instrucciones `.github/copilot-instructions.md` existentes en el microservicio
siguen siendo propias de ese repo. La alternativa por archivos instala ahí un
bloque gestionado con las reglas compartidas; instalar un plugin no convierte
por sí mismo el repo del plugin en el workspace del servicio.

## Capacidades individuales

| Skill | Capacidad |
| --- | --- |
| backend-preparar-repo | Instalar/actualizar soporte desde el plugin |
| backend-contexto | Arquitectura, endpoints, clientes y puntos donde cambiar |
| backend-evidencias | Correlacionar logs, consola, MD y referencias |
| backend-plan | Aceptación y matriz de impacto |
| backend-contrato | Contrato primero y regeneración |
| backend-implementacion | Cambio acotado con patrones del repo |
| backend-errores-http | Traducción Business → UX y regresiones |
| backend-pruebas-unitarias | JUnit/Mockito y cobertura real |
| backend-karate | Pruebas de componente y regresión HTTP |
| backend-kafka | Eventos, topics y schemas cuando corresponda |
| backend-config-manual | Delta por desarrollo/certificación/producción |
| backend-calidad | Build completo y verificación de informes |
| backend-sanity | Salud y escenarios smoke, sin reemplazar suites |
| backend-commits | Métricas, mensaje propuesto; commit solo cuando se pide |
| backend-memoria | Mapa Mermaid, bitácora y actualización por delta |

## Java, Maven, Python y calidad

La primera preparación descubre POM, JDK, perfiles/runners y reportes reales.
Las rutas Java/Maven personales quedan en `.assistant-local/backend/toolchain.json`,
excluido de Git. Sin overrides, hereda el entorno de terminal; no presume que el
JDK del editor coincide con Maven. Tras configurar build, ejecutar el diagnóstico:

```powershell
py -3 engineering/backend/scripts/backend.py doctor --repo .
```

[ENTORNO.md](engineering/backend/ENTORNO.md) explica PATH, wrapper, settings y
precedencia. Los overrides afectan solo a los checks; no cambian variables globales.
Todos los scripts/tests usan biblioteca estándar: Python 3.10+, Git y PowerShell
son requisitos; no hacen falta pip, ipykernel ni librerías externas.

Calidad inicial: clean install sin omisiones, unitarias, Karate aplicable,
Checkstyle y 95% exacto de INSTRUCTION JaCoCo. Informes ausentes/viejos, cambios
posteriores del código/entorno o suites vacías no acreditan un PASS. Los scripts
verifican consistencia; revisión y CI comprueban aceptación y alcance de pruebas.
Config Maps sigue manual: prepara delta, no inicia jobs o despliegues externos.

## Alternativa por archivos y mantenimiento

Si plugins no están disponibles, clonar este repo y ejecutar desde su raíz:

```powershell
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio' -PlanOnly
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio'
```

No mezclar esa modalidad con el mismo agente/skills del plugin. La instalación
por archivos se actualiza ejecutando nuevamente el instalador; no tiene un
servicio de actualización automática. Las copias anteriores de prompts se
revisan manualmente si existían; el instalador no borra personalizaciones.

Validación del paquete, sin librerías pip:

```powershell
py -3 -S distribution/check_package.py
py -3 -S -m unittest discover -s tests -v
```

Los ensayos del paquete no demuestran que un modelo siga todas las instrucciones.
El piloto real debe comprobar preparación, carga de skills, fases y evidencia
antes de ampliar adopción. Ver [VALIDACION.md](VALIDACION.md),
[operación](engineering/backend/OPERACION.md),
[distribución](distribution/GIT-Y-VSCODE.md) y [cambios](CHANGELOG.md).

## Inventario, auditoría y criterio para quitar archivos

El [inventario de archivos y criticidad](INVENTARIO.md) explica cada fuente,
carpeta, dependencia, usuario afectado y consecuencia de eliminarla. Incluye
los cinco Python fuente, los tres PowerShell, los controles de mantenimiento
y oportunidades de consolidación. El [anexo del workspace](AUDITORIA-WORKSPACE.md)
enumera el paquete BCP anterior, propuestas, muestras TypeScript, ZIP, bundles,
notas y cachés. Es una foto del 3 de octubre de 2026; no elimina archivos.

La auditoría examinó un árbol local **0.6.0 con cambios previos sin commit**;
al empezar, `main` remoto estaba en **0.5.0**. Publicar estos documentos por
separado no publica la implementación pendiente de 0.6.0. Identifica la versión
real con `plugin.json` y `installation.json` antes de usar rutas de soporte:

| Versión del soporte | Ruta en el microservicio | Documentación/evidencia del agente |
| --- | --- | --- |
| 0.5.0 | `engineering/backend/` | Modelo anterior descrito en esa versión |
| 0.6.0 auditada localmente | `.assistant-local/backend/support/` | Mapa y expediente únicos en `.assistant-local/backend/`, excluidos de Git |

El agente es una personalización de Copilot. Las skills son instrucciones que
Copilot carga, los Python verifican evidencia y los PowerShell preparan archivos
o ejecutan comandos en Windows. El paquete no incorpora un servidor backend
adicional: trabaja sobre el microservicio Java que abras.

## Qué es el backend técnico y cómo se utiliza

`engineering/backend` contiene el **soporte ejecutable del agente**, además de
perfil, política, documentación, referencias y plantillas. En 0.6.0 se instala
en la carpeta local indicada arriba. El flujo de uso es:

1. Abrir la raíz Git del microservicio y seleccionar `backend-java`.
2. Preparar soporte si falta o cambió la versión del plugin. El perfil inicial
   está vacío: se completa a partir del POM, runners y reportes del servicio.
3. Confirmar la selección Java/Maven/settings/repositorio local según ENTORNO.
   Python 3.10+, Git y PowerShell en Windows son las herramientas del soporte;
   el JDK y Maven dependen del servicio. El paquete actual no requiere pip.
4. Pedir un cambio completo o una skill individual. El runner conserva comandos,
   exit codes, huellas y reportes; el orquestador registra fases y comprueba cierre.
5. Revisar evidencia y pendientes. La verificación local no acredita CI/Sonar,
   aceptación humana, traslado de configuración o despliegue.

El runtime `scripts/backend.py` ofrece estos subcomandos. Sustituye la ruta de
soporte por la correspondiente a tu versión:

| Subcomando | Para qué sirve | Resultado observable |
| --- | --- | --- |
| `snapshot` | Inventario/huella de archivos técnicos, incluidos nuevos y cambios locales | JSON con fingerprint y archivos; con compare, delta frente a una foto anterior |
| `doctor` | Ejecutar versiones Java/Maven y contrastar el JDK de Maven con el perfil | TOOLCHAIN_PASS/BLOCKED y diagnóstico local; no ejecuta clean install |
| `run` | Ejecutar un comando revisado del perfil, como build, unit, karate o generate | Log, exit code, huellas y registro de reportes bajo un run ID |
| `verify` | Verificar gates contra ejecuciones y reportes actuales | Resultado de compuertas; reportes viejos, ausentes o cambiados no acreditan PASS |
| `metrics` | Medir commits, archivos y líneas desde la base Git real | Métricas de delta y pendiente; no hace commit |
| `workflow-start` | Registrar tarea, pedido y alcance | workflow.json; individual exige cita literal del pedido que lo limita |
| `workflow-phase` | Registrar resultado, skills y artefactos de una fase | Huellas de skills/evidencias; no carga por sí solo una skill en Copilot |
| `workflow-close` | Comprobar fases/evidencia y, en completo, gates/memoria/aceptación | LOCAL_VERIFIED, SCOPED_TASK_DONE o BLOCKED según alcance y evidencia |

Ejemplo de comandos para **soporte 0.6.0**, desde la raíz del microservicio y
después de configurar/confirmar el perfil. `DEMO-001` es un identificador de
ejemplo; Karate separado solo cuando el runner real del servicio lo requiere:

```powershell
py -3 -S .assistant-local/backend/support/scripts/backend.py doctor --repo .
py -3 -S .assistant-local/backend/support/scripts/backend.py run --repo . --check build --run-id DEMO-001
py -3 -S .assistant-local/backend/support/scripts/backend.py run --repo . --check karate --run-id DEMO-001
py -3 -S .assistant-local/backend/support/scripts/backend.py verify --repo . --run-id DEMO-001
```

No hay un subcomando directo `generate`: generación usa `run --check generate`
si ese comando está configurado en el perfil. `verify` comprueba calidad;
`workflow-close` comprueba el cierre del expediente completo. Las rutas de
reportes/perfiles se descubren en el servicio; estos ejemplos no certifican un
servicio específico ni garantizan un resultado aprobado.

### Por qué hay tres PowerShell y para qué sirve Install-Backend

| Script | Responsabilidad | Qué cambia o ejecuta |
| --- | --- | --- |
| `Install-Backend.ps1` | Entrada pública corta | Delega parámetros al instalador gestionado; no instala Java, Maven, Python ni un servidor |
| `distribution/Install-Managed.ps1` | Implementación de preparación/actualización | Copia archivos, conserva perfil/política, detecta conflictos, escribe metadata y exclusión local Git |
| `engineering/backend/scripts/Invoke-Command.ps1` | Puente del runtime en Windows | Lee un spec JSON y ejecuta el programa con argumentos separados, directorio y entorno de proceso; devuelve exit code |

Las modalidades de instalación son diferentes:

```powershell
# Desde la raíz del paquete 0.6.0: revisar preparación sin escribir.
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio' -SupportOnly -PlanOnly

# Preparar únicamente soporte para un agente ya instalado como plugin.
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio' -SupportOnly

# Alternativa por archivos: revisar y luego copiar soporte, agente, skills y reglas.
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio' -PlanOnly
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio'
```

Con SupportOnly no se duplican agente/skills en `.github`. Sin SupportOnly se
copian allí las instrucciones y se gestiona un bloque en copilot-instructions.
`-PlanOnly` no escribe. En una ejecución efectiva el instalador valida raíz Git,
destinos, conflictos y exclusión; no ejecuta Maven, push ni despliegue. Tampoco
borra archivos antiguos ni elimina personalizaciones. El puente Invoke-Command
se usa después para ejecutar checks; no es otro instalador.

## Uso, ejemplo y resultado esperado de cada skill

Selecciona `backend-java` en Copilot. Para un cambio completo escribe el objetivo
en lenguaje normal; el agente encadena las fases necesarias. Para una capacidad
individual escribe **Solo** seguido del nombre y alcance, o selecciona la skill
disponible en el menú `/` del cliente. Los prefijos mostrados por el plugin pueden
variar. La [documentación de skills de VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
describe carga bajo demanda e invocación en chat.

Los nombres de endpoints, clases, tickets y eventos en los ejemplos son
**ilustrativos**: sustitúyelos por los del servicio. El resultado esperado indica
qué evidencia debe entregar el agente; depende de archivos, herramientas y
accesos disponibles. Si falta un requisito, debe reportar el pendiente, no inventar PASS.

| Skill / instrucciones | Cuándo utilizarla | Ejemplo de solicitud individual | Resultado esperado |
| --- | --- | --- | --- |
| [backend-preparar-repo](skills/backend-preparar-repo/SKILL.md) | Primer uso del plugin o soporte de versión distinta | `Solo backend-preparar-repo: prepara el soporte de este microservicio usando el plugin instalado y conserva mis personalizaciones.` | Soporte instalado/actualizado, installation.json y exclusión comprobada, o conflictos con rutas/diff; no ejecuta Maven |
| [backend-contexto](skills/backend-contexto/SKILL.md) | Entender un flujo, diagnosticar ubicación de un cambio o reanudar | `Solo backend-contexto: explica el flujo de GET /pedidos/{id}, sus clientes y dónde se traducen los errores.` | Mapa entrada→lógica→dependencia→salida con rutas/símbolos, perfil descubierto y lagunas; sin implementar |
| [backend-evidencias](skills/backend-evidencias/SKILL.md) | Investigar con logs, consola, MD o referencias adjuntas | `Solo backend-evidencias: correlaciona estos logs del mismo request y separa hechos de hipótesis sobre el error genérico.` | Fuentes sanitizadas, secuencia temporal, vínculo al código y datos faltantes; no presupone acceso directo a Grafana |
| [backend-plan](skills/backend-plan/SKILL.md) | Definir aceptación e impacto antes de cambiar | `Solo backend-plan: planifica la corrección para devolver 204 sin cuerpo únicamente ante la ausencia reconocida del Business.` | Matriz de archivos/clases/métodos, contrato, config y tests con riesgos y aceptación; no modifica lógica |
| [backend-contrato](skills/backend-contrato/SKILL.md) | Cambiar/verificar interfaces HTTP o generación | `Solo backend-contrato: verifica si el OpenAPI fuente contempla 204 sin contenido; si falta, actualízalo y regenera con el mecanismo del repo.` | Fuente localizada, cambio contractual o motivo de no cambio, comando/diff de generación y compatibilidad; dependencia externa si aplica |
| [backend-implementacion](skills/backend-implementacion/SKILL.md) | Implementar una tarea ya entendida y delimitada | `Solo backend-implementacion: aplica el plan acordado en el mapper de PedidoService y conserva los demás errores.` | Diff acotado siguiendo arquitectura real, pruebas relevantes de iteración y pendientes; no declara flujo completo cerrado |
| [backend-errores-http](skills/backend-errores-http/SKILL.md) | Investigar/corregir traducción Business→UX | `Solo backend-errores-http: corrige la traducción de la señal de ausencia definida en el contrato a 204 vacío; conserva auth, timeout y 5xx.` | Causa/punto de traducción, regresión del caso y errores vecinos; comprueba status y cuerpo en límite HTTP; no aplica 404→204 universal |
| [backend-pruebas-unitarias](skills/backend-pruebas-unitarias/SKILL.md) | Crear/corregir JUnit/Mockito o revisar cobertura | `Solo backend-pruebas-unitarias: cubre los caminos feliz, ausencia y timeout de PedidoService con las convenciones del repo.` | Tests sustantivos, ejecución y reportes; distingue cobertura de clase frente a suite global y no afirma 95% sin medición completa |
| [backend-karate](skills/backend-karate/SKILL.md) | Regresión HTTP de componente | `Solo backend-karate: añade y ejecuta escenarios con datos, 204 sin cuerpo y error Business controlado usando los stubs existentes.` | Features/fixtures, runner/perfil real, escenarios ejecutados/fallidos/omitidos y reportes; ejecución bloqueada si falta infraestructura |
| [backend-kafka](skills/backend-kafka/SKILL.md) | El servicio realmente publica/consume eventos | `Solo backend-kafka: revisa y prueba el consumidor de PedidoCreado, incluidos duplicados y ack/nack según sus requisitos actuales.` | Schema/topic/config y semántica comprobados, pruebas con herramientas existentes y límites de broker/consumidor; handoff si requiere config |
| [backend-config-manual](skills/backend-config-manual/SKILL.md) | Hay delta de claves compartidas por ambiente | `Solo backend-config-manual: prepara el traslado de la nueva clave business.timeout a DEV/CERT/PROD y separa los overrides locales.` | Tabla de claves/operación/consumidor/valores/destino/prueba, referencias a secretos y pendientes; MANUAL_PENDING hasta confirmación, sin ejecutar Jenkins |
| [backend-calidad](skills/backend-calidad/SKILL.md) | Validar build y gates finales o revisar calidad | `Solo backend-calidad: ejecuta el clean install completo y comprueba unitarias, Karate aplicable, Checkstyle y JaCoCo con la política vigente.` | Comandos/exit codes y reportes actuales, verify con gates PASS/FAIL/NOT_RUN; cobertura INSTRUCTION mínima 95% exacta; cierre de fases aparte |
| [backend-sanity](skills/backend-sanity/SKILL.md) | Comprobación sanitaria delimitada | `Solo backend-sanity: usa la instancia local ya iniciada y comprueba health y un GET representativo según el contrato.` | URL/ambiente y esperado frente a observado: status, bytes de cuerpo y duración; no equivale a suite, cobertura o build completo |
| [backend-commits](skills/backend-commits/SKILL.md) | Evaluar métricas/preparar mensaje o hacer acciones Git autorizadas | `Solo backend-commits: evalúa el diff contra la base real y prepara el mensaje para DEMO-123; no ejecutes commit ni push.` | Métricas, propuesta de mensaje en inglés ≤72 caracteres, lista explícita de archivos y calidad/pedientes; preparar no hace commit |
| [backend-memoria](skills/backend-memoria/SKILL.md) | Actualizar mapa/bitácora después del cambio o verificar vigencia | `Solo backend-memoria: actualiza el mapa y el expediente de DEMO-123 con el delta del mapper y las pruebas realmente ejecutadas.` | Mapa/diagrama, metadata snapshot y bitácora por delta, fuentes/decisiones/gates; documentación sin tests no acredita calidad de código |

En modo individual el resultado corresponde exclusivamente a lo solicitado:
DIAGNOSED para contexto/diagnóstico, SCOPED_TASK_DONE para capacidad terminada,
o BLOCKED con dependencia real. Las compuertas ajenas quedan NOT_RUN. En modo
completo el agente conserva las ocho fases y requiere workflow-close antes de
afirmar LOCAL_VERIFIED; una skill interna terminada no reduce ese alcance.

Ejemplo completo que combina capacidades:

```text
Corrige este microservicio UX: la señal de ausencia reconocida por el contrato
debe devolver HTTP 204 sin cuerpo y hoy acaba en error genérico. Usa los logs
adjuntos, identifica la condición exacta y conserva los demás errores.
Completa contexto/evidencias, plan, contrato si cambia, implementación,
unitarias y Karate, config manual si aplica, calidad y memoria/entrega.
Muestra la evidencia de cada fase y el resultado de workflow-close.
Prepara el mensaje de commit, sin push ni despliegue.
```

Resultado esperado: diff de código/pruebas acotado, prueba del límite HTTP,
expediente trazable, gates actuales y mapa actualizado. Se entrega LOCAL_VERIFIED
solo con verificaciones completas; si falta un gate o aceptación, se muestran
avances y BLOCKED con los pendientes. Config Maps/CI/revisión/producción se
reportan con su estado propio y no se presentan como comprobados por el build local.
