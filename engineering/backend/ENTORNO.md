# Java, Maven, VS Code y Python

## Seleccionar las herramientas

Leer POM padre/módulos, compiler/toolchains y CI para identificar el JDK requerido.
No actualizar el POM para acomodarlo al JDK disponible. Comparar editor y terminal.

1. Rutas compartidas explícitamente: comprobarlas y guardarlas en
   `.assistant-local/backend/toolchain.json`, excluido de Git.
2. Revisar ajustes disponibles de VS Code: `java.configuration.runtimes`,
   `java.jdt.ls.java.home`, configuración de Maven y `terminal.integrated.env.windows`.
   Son candidatos; no prueban por sí mismos qué JDK ejecuta Maven.
3. Si el repo usa Maven Wrapper, registrar su ruta real (`.\mvnw.cmd` en Windows).
   Usarlo conforme al repo; si necesita descarga/conectividad no disponible,
   reportar el bloqueo. No reemplazarlo silenciosamente.
4. Sin selección explícita/wrapper del repo, resolver `mvn` en el PATH efectivo.

El `executable` del perfil es la selección revisada: `${maven}`, wrapper o `mvn`.
El runtime respeta esa elección. `javaHome` fija JAVA_HOME y antepone su bin al
PATH del hijo. `mavenHome` fija MAVEN_HOME/M2_HOME y antepone su bin. Conserva el
resto del PATH, incluido un PATH del comando. Sin overrides hereda el entorno del
proceso de Python. No usa aliases de shell: configurar el ejecutable real.
No modifica variables globales ni configuración de VS Code.

El editor puede usar otro JDK; la terminal tiene su propio entorno configurable.
[Java en VS Code](https://code.visualstudio.com/docs/java/java-project),
[entorno de terminal](https://code.visualstudio.com/docs/terminal/advanced).
Maven puede usar JAVA_HOME o Java en PATH;
[documentación de Maven](https://maven.apache.org/install.html).

## Overrides locales

Ejemplo de estructura: **reemplazar las rutas por las que existan**, omitir campos
innecesarios y guardar en `.assistant-local/backend/toolchain.json`:

```json
{
  "javaHome": "C:/tools/jdk-17",
  "maven": "C:/tools/apache-maven/bin/mvn.cmd",
  "mavenHome": "C:/tools/apache-maven",
  "mavenSettings": "C:/Users/<usuario>/.m2/settings.xml",
  "mavenRepository": "C:/Users/<usuario>/.m2/repository"
}
```

El perfil compartido puede contener placeholders, no paths personales. Forma de
`commands.build`, adaptar gates al POM antes de usarla:

```json
{
  "executable": "${maven}",
  "args": ["-s", "${mavenSettings}", "-Dmaven.repo.local=${mavenRepository}", "clean", "install"],
  "workingDirectory": ".",
  "gates": ["build", "unit", "checkstyle", "coverage"]
}
```

Para `mvn` de PATH o wrapper cambiar executable y eliminar placeholders que no
apliquen. Sin `-s`, Maven sigue su configuración habitual. Credenciales, mirrors
y proxies quedan en mecanismos locales; no copiar settings.xml o secretos a
evidencia ni reescribir ese archivo. `service.javaMajor` registra el JDK requerido.

Maven Toolchains puede elegir un compilador distinto al Java que ejecuta Maven.
Revisar POM/toolchains.xml y registrar esa diferencia. El diagnóstico compara
el Java de Maven; no certifica todos los compiladores configurados.

## Diagnóstico antes del build

Tras configurar el build real desde el repo:

```powershell
py -3 engineering/backend/scripts/backend.py doctor --repo .
```

Muestra Python, rutas resueltas, `java -version`, Maven `--version` y comparación
con `service.javaMajor`. Guarda `.assistant-local/backend/doctor.json`. Un path
inexistente o JDK distinto bloquea el diagnóstico. No ejecuta clean/install ni
instala paquetes. El wrapper puede necesitar su descarga habitual del repo.

La evidencia incluye huella del comando y JAVA_HOME, MAVEN_HOME, M2_HOME, PATH y
opciones Java/Maven. Un cambio requiere nueva ejecución para acreditar calidad.
Los valores permanecen locales. La huella no sigue archivos fuera del repo o
binarios instalados: si cambia settings.xml/toolchains.xml o las herramientas,
volver a ejecutar checks. `doctor` no valida mirrors, credenciales o dependencias.

Si se cambió el entorno en otra consola, abrir terminal nueva en VS Code y volver
a diagnosticar. El runner usa PowerShell sin perfil; conserva el entorno heredado
y aplica overrides del comando. No editar variables globales para un solo repo.

## Python y librerías

Se requiere Python 3.10+: `py -3` en Windows o el python/python3 real de la máquina.
No asumir que el selector de notebooks determina todos los comandos de terminal.
Todos los scripts/tests usan biblioteca estándar: no hay requirements externos,
pip en CI ni installs automáticos. `ipykernel` sirve a notebooks y no hace falta.
El paquete también se verifica con `-S`, sin carga de site ni paquetes instalados.

Si una futura tarea necesita librerías, usar el comando/índice aprobado que
proporcione el desarrollador. No incrustar hosts privados o autenticación en el
repo compartido ni reemplazar el índice por PyPI público. Un comando terminado
en `ipykernel` instala ese paquete; no equivale a instalar cualquier dependencia.
Este paquete no necesita ejecutar ese comando.
