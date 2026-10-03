# Distribuir el agente desde Git

Versión de distribución 0.3.0. La rama destinada a instalación debe contener
únicamente versiones revisadas. Mantener cambios de desarrollo en ramas feature;
proteger la rama estable con PR y checks según la plataforma Git.

## En la máquina del desarrollador

En VS Code, ejecutar **Chat: Install Plugin From Source** e indicar
`https://github.com/DiegoAlosilla/backend-copilot-agent.git`. Es privado: Git/VS Code
deben autenticarse con una cuenta que tenga acceso. Para otros desarrolladores,
conceder acceso previamente. Integrar `vscode-user-settings.jsonc` en los ajustes
de usuario, sin reemplazar otras claves. El archivo configura plugin support y
actualización automática; no desactiva controles corporativos.
`extensions.autoUpdate` también afecta actualizaciones de extensiones: respetar
el valor gestionado por la organización si existe. No se cambia ese ajuste desde el agente.

VS Code documenta comprobaciones automáticas de plugins cada 24 horas con
`extensions.autoUpdate` habilitado. Se pueden forzar con **Extensions: Check for
Extension Updates**. Cambiar la versión de `plugin.json` en cada publicación.
La disponibilidad depende de VS Code/extensión y política de la organización. No es un
servicio que se ejecute cuando VS Code está cerrado.
[Instalación y actualización de plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

Seleccionar `backend-java` y abrir un chat nuevo tras actualizar. Las skills también
se pueden ejecutar individualmente. El plugin contiene el agente y las skills;
el microservicio conserva su perfil, política y documentación. La primera sesión
usa `/backend-preparar-repo` para instalar soporte en el repo con `-SupportOnly`.
Esta preparación no duplica agentes/skills ni copia workflows del paquete.

Actualización tiene dos partes:

1. VS Code actualiza el plugin compartido desde Git: instrucciones y skills.
2. En la siguiente sesión del agente, la preparación del repo aplica nuevas plantillas
   y scripts compartidos. Preserva perfil/política y detiene archivos localmente
   modificados. No ejecuta Maven o modifica lógica al actualizar soporte.

`installation.json` local registra versión y huellas de archivos gestionados.
Los cambios de soporte pueden aparecer en `git diff`: revisarlos/versionarlos
con el modelo del equipo. La actualización del plugin no agrega commits al
microservicio ni inicia el cambio funcional automáticamente. Cambios de política
central requieren revisión explícita porque se preserva la política del servicio.

Si plugins no están disponibles en la versión corporativa, conservar la
instalación por archivos del README; no afirmar autoactualización en ese caso.
No instalar simultáneamente las mismas skills como plugin y como archivos del
workspace: el workspace puede ocultar las del plugin por precedencia. La migración
de copias 0.1.0 se revisa manualmente; no se borran personalizaciones.

## Repositorio de distribución

La fuente principal es `DiegoAlosilla/backend-copilot-agent`, rama `main`.
La entrega 0.3.0 usa nombres genéricos e historial inicial propio. No contiene
hosts privados, logs, secretos o código de microservicios. El repositorio se
distribuye privado; no incrustar PAT en URL o settings.

Para moverlo sin un remoto disponible se entrega un Git bundle:

```powershell
git clone 'D:\ruta\backend-copilot-agent-v0.3.0.bundle' backend-copilot-agent
```

El bundle conserva historial/etiqueta. Para instalar/actualizar desde VS Code
usar la URL de Git. Un ZIP o bundle por
sí mismo no ofrece actualizaciones de red.

## Publicar una nueva versión

1. Cambiar skills/scripts en feature branch, añadir regresión si aplica.
2. Ejecutar tests y `distribution/check_package.py`.
3. Incrementar versión de plugin y notas de CHANGELOG. La versión registrada de
   política es informativa; su migración en cada servicio requiere revisión.
4. Actualizar manifest de integridad; crear PR hacia la rama estable.
5. Tras aprobar/integrar, etiquetar la versión. Instalar desde rama estable y
   verificar una máquina piloto antes de ampliar adopción.

La actualización automática sigue la fuente instalada y las políticas del
cliente. Una etiqueta fijada da reproducibilidad, pero no un canal de futuras
versiones. Para distribución de varios plugins/branches se puede añadir un
marketplace corporativo posteriormente; este MVP se instala desde su URL Git.

## Organización del paquete

`plugin.json` utiliza el formato Copilot con paths explícitos a agentes, skills y
commands. Así `.github` sigue siendo fuente única para plugin e instalación por
archivos, sin mantener copias divergentes. Su compatibilidad se comprueba con el
cliente corporativo. [Referencia del formato Copilot](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

CI del repo del agente valida el paquete; no despliega microservicios ni lee
secretos empresarials. Ajustar runners e índices de dependencias de desarrollo si
el repositorio se aloja en plataforma corporativa.
