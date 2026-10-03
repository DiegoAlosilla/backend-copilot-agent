# Backend Java Agent para GitHub Copilot

Versión **0.5.0**: un agente principal y **15 skills** para cambios Java completos
o tareas individuales. Usa Quarkus/Spring y la arquitectura real del repositorio.

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
