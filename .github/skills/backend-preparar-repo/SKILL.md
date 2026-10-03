---
name: backend-preparar-repo
description: Prepara o actualiza los scripts y plantillas compartidas de un microservicio cuando el agente está instalado como plugin de VS Code. Conserva perfil, política y cambios locales; no publica ni despliega.
---

# Preparar el repo con el plugin

Úsala al iniciar una sesión del agente cuando falte `engineering/backend` o su versión sea
distinta a la del plugin cargado. Compara plugin.json con packageVersion en
`.assistant-local/backend/installation.json`, no con la política preservada del repo.
No requiere repetirla por cada skill de una
misma sesión. Ubica la raíz **del plugin** a partir de la ruta real de este
SKILL.md: tres niveles hacia arriba. No busca credenciales ni el cache completo.
El microservicio objetivo es la raíz Git del workspace del desarrollador; no
confundas esa raíz con la del plugin.

Lee [el instalador del paquete](../../../Install-Backend.ps1) y el
[procedimiento compartido](../../../engineering/backend/OPERACION.md) si hace falta.
En Windows ejecuta el instalador de esa raíz con `-RepositoryPath` igual al
microservicio y `-SupportOnly`. Usa argumentos de PowerShell sin formar una
cadena evaluada. En otras plataformas registra instalación manual pendiente;
no improvisa un script que sobrescriba archivos.

`SupportOnly` copia/actualiza únicamente `engineering/backend` y la exclusión local.
No copia agentes/skills del plugin al microservicio ni modifica `.vscode`.
Preserva perfil/política existentes. Solo actualiza un archivo gestionado si
coincide con la huella registrada de la instalación anterior. Si hay conflicto,
entrega diff/rutas y continúa con tareas que no dependan del recurso bloqueado.
No usa force, borra personalizaciones o altera código productivo.

Tras preparar, el agente completa perfil mediante POM/runners reales y usa los
scripts instalados. Esto es preparación de soporte, no evidencia de que las
pruebas del microservicio pasaron.
