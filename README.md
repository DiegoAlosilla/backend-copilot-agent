# Backend Java Agent para GitHub Copilot

Versión **0.3.0**. Un agente para cambios en microservicios Java existentes y
**15 skills independientes** para usar solamente la capacidad necesaria.
Soporta Quarkus o Spring según el repo, contrato primero, unitarias, Karate,
Kafka cuando corresponda y documentación reutilizable con diagramas Mermaid.
La instalación y los ensayos automatizados se validaron en Windows.

## Instalación recomendada desde Git

1. En VS Code con Copilot, iniciar sesión con una cuenta que tenga acceso a este
   repositorio privado. Para el equipo, conceder acceso antes de instalar.
2. Integrar estas claves en **User Settings (JSON)**, conservando las existentes:

   ```json
   {
     "chat.plugins.enabled": true,
     "extensions.autoUpdate": true
   }
   ```

3. Ejecutar **Chat: Install Plugin From Source** en la paleta y pegar:

   ```text
   https://github.com/DiegoAlosilla/backend-copilot-agent.git
   ```

4. Abrir la raíz Git del microservicio. Seleccionar **backend-java** en Copilot
   y el modelo permitido por el equipo. Iniciar con `/backend-cambio`.

Si la versión o las políticas del cliente no permiten plugins, usar la
[instalación por archivos](#alternativa-por-archivos). No instalar las mismas
skills por ambas modalidades; las copias del workspace pueden ocultar el plugin.
No insertar tokens en URLs o settings.

VS Code comprueba actualizaciones de plugins cada 24 horas con la actualización
automática habilitada. Puede forzarse desde **Extensions: Check for Extension
Updates**. Este ajuste también afecta extensiones; respetar configuración
gestionada. [Referencia oficial](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

El plugin actualiza agente/skills. En la próxima sesión, `backend-preparar-repo`
actualiza scripts y plantillas en `engineering/backend`, preservando perfil,
política y memoria del servicio. Archivos personalizados se detectan antes de
copiar; no se sobrescriben. Revisar y versionar el diff de soporte con el equipo.
El ciclo real de instalación/actualización debe comprobarse en el cliente piloto.

## Cómo iniciar un cambio

Adjuntar lo disponible: logs descargados de Grafana, consola, Markdown, contrato
o código de otro servicio. El agente empieza con eso y pide solo datos críticos.

```text
/backend-cambio Este UX devuelve error genérico cuando Business indica que no
se encontró lo buscado. Debe devolver HTTP 204 sin cuerpo solo en ese caso.
Adjunto logs y contrato. Diagnostica, muestra el plan de clases/métodos,
corrige y verifica unitarias, Karate, clean install y 95% de INSTRUCTION.
Config Maps manual. No hagas push ni despliegue.
```

Si el cliente no expone el slash prompt, seleccionar `backend-java` y pegar el
texto sin `/backend-cambio`. Revisar personalización/Diagnostics si no aparece.

La primera sesión prepara el soporte y descubre POM, perfiles, runners y reportes
reales. El perfil llega sin comandos preinventados. Los siguientes cambios
reutilizan memoria validada contra las huellas y releen el flujo afectado.

## Qué capacidades tiene

El flujo completo es **contexto → evidencias → plan → contrato → implementación
→ pruebas → configuración → calidad → memoria/entrega**. Se limita al alcance
pedido y conserva la arquitectura real: capas, hexagonal o híbrida.

| Skill | Uso individual |
| --- | --- |
| `/backend-preparar-repo` | Instalar/actualizar soporte desde el plugin |
| `/backend-contexto` | Arquitectura, endpoints, clientes y lugares donde tocar |
| `/backend-evidencias` | Correlacionar logs y documentación; distinguir hechos e hipótesis |
| `/backend-plan` | Aceptación y matriz de clases/métodos, contratos, config y tests |
| `/backend-contrato` | Contrato primero y regeneración; no editar clases generadas |
| `/backend-implementacion` | Cambio acotado con patrones del repo |
| `/backend-errores-http` | Diagnóstico/mapeo Business → UX; 204 específico, sin cuerpo |
| `/backend-pruebas-unitarias` | JUnit/Mockito y cobertura real según política |
| `/backend-karate` | Pruebas de componente y regresión HTTP |
| `/backend-kafka` | Topics, schemas, publicación/consumo si aplica |
| `/backend-config-manual` | Delta de configuración por ambiente para traslado manual |
| `/backend-calidad` | Build completo y verificación de informes actuales |
| `/backend-sanity` | Smoke: salud y escenarios mínimos; no reemplaza la suite |
| `/backend-commits` | Métricas, mensajes y commits cuando se solicitan |
| `/backend-memoria` | Mapa Mermaid, bitácora y actualización por delta |

Ejemplos: “`/backend-sanity Solo verifica salud y este endpoint`” o
“`/backend-commits Solo evalúa métricas y prepara el mensaje, sin commit`”.
Las tareas individuales no activan por defecto todo el flujo.

## Java, Maven y variables del equipo

El agente descubre qué JDK pide el POM y comprueba el Maven/JDK de la terminal.
Las rutas que comparta el desarrollador se guardan en
`.assistant-local/backend/toolchain.json`, excluido de Git. Los overrides afectan
solo los procesos de los checks; no cambian variables globales ni VS Code.
Si no hay overrides, hereda el entorno del proceso que lo ejecuta.

El JDK de la extensión Java y el de Maven pueden diferir. Revisar las rutas
configuradas en VS Code y comprobar el resultado real con:

```powershell
py -3 engineering/backend/scripts/backend.py doctor --repo .
```

El diagnóstico requiere primero configurar el comando `build` real. No instala
herramientas ni descarga dependencias del servicio por su cuenta. Consulte
[ENTORNO.md](engineering/backend/ENTORNO.md) para precedencia, settings.xml,
repositorio Maven local, PATH, wrapper y ejemplos.

## Python: sin instalaciones pip

**Todos los scripts y tests del paquete usan únicamente la biblioteca estándar.**
Se requiere Python 3.10+ para los verificadores, Git y PowerShell en Windows.
No hace falta `pip install`, `ipykernel`, Jupyter ni acceso a un índice PyPI.
Los comandos de instalación de paquetes de la organización siguen siendo
válidos para otras necesidades; este agente no los ejecuta ni los modifica.

| Archivo Python | Propósito |
| --- | --- |
| `engineering/backend/scripts/backend.py` | Diagnóstico, ejecución, reportes, huellas y métricas |
| `distribution/check_package.py` | Validar el paquete al mantenerlo/publicarlo |
| `tests/test_*.py` | Ensayos aislados del paquete; no son tests del microservicio |

Sin Python, el agente puede analizar y editar; la verificación automática queda
pendiente. No declara calidad aprobada ni intenta instalar Python por su cuenta.

## Calidad y memoria

La política inicial exige `clean install`, unitarias, Karate, Checkstyle y
**95% exacto de INSTRUCTION JaCoCo**, sin redondear 94.9% ni ocultar fallos con
omisiones. Se configura con el POM/runners reales. No cambia exclusiones para
obtener verde. Informes ausentes, viejos o alterados y cambios posteriores del
código/entorno invalidan la evidencia. Son controles locales de consistencia;
la revisión funcional y CI siguen siendo necesarias.

La documentación del servicio vive en `docs/engineering`: mapa de dependencias
con Mermaid, metadata de validación y bitácora por cambio. La vista estructural
explica arquitectura/dependencias; la secuencia explica el flujo modificado.
Destaca clases afectadas y diferencia inferencia, evidencia y revisión humana.

Config Maps se mantiene manual: el agente prepara un delta por desarrollo,
certificación y producción. El desarrollador lo traslada a la rama feature y
ejecuta Jenkins según el proceso del equipo. No modifica repos externos ni
inicia jobs/despliegues automáticamente.

## Alternativa por archivos

Clonar este repo o extraer el ZIP 0.3.0, y desde su raíz ejecutar:

```powershell
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio' -PlanOnly
.\Install-Backend.ps1 -RepositoryPath 'D:\ruta\microservicio'
```

Esta modalidad conserva instrucciones previas y detecta conflictos antes de
copiar. **No se autoactualiza**: actualizar el clon y ejecutar nuevamente el
instalador. Para actualización periódica, usar la modalidad plugin desde Git.

## Mantenimiento y comprobaciones

```powershell
py -3 -S distribution/check_package.py
py -3 -S -m unittest discover -s tests -v
```

`-S` prueba que no se necesitan paquetes instalados. Los **42 tests** pasaron en
Windows; ver [VALIDACION.md](VALIDACION.md). La corrección del caso 204 y Maven/
Karate reales se validan al instalar en el microservicio objetivo.

Más detalle: [operación y comandos](engineering/backend/OPERACION.md),
[distribución y actualización](distribution/GIT-Y-VSCODE.md),
[caso piloto 204](engineering/backend/references/CASO-204.md) y
[cambios de versión](CHANGELOG.md).
