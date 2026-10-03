---
name: backend-java
description: Orquesta un cambio backend Java completo con skills cargadas, fases visibles y evidencia de pruebas, build y memoria. Solo limita el flujo cuando el desarrollador pide una tarea individual.
argument-hint: Describe el cambio; el modo completo es el predeterminado. Para una tarea individual escribe solo y el alcance.
---

# Backend Java: orquestación verificable

Trabaja en la raíz Git del microservicio abierto, conserva el modelo seleccionado
por el desarrollador y respeta sus reglas, permisos y cambios ajenos.
Inspecciona git status y diff antes de editar para distinguir cambios propios
de cambios previos; no descubras esa distinción solamente al cerrar.
Una descripción de fallo con resultado esperado es una solicitud de corrección:
inicia el flujo completo. Diagnosticar es la primera actividad, no un cambio de modo.
Para limitar el alcance, cita las palabras del desarrollador que lo delimitan;
tu propio resumen, una memoria previa o el anuncio de auditoría no son esa evidencia.
Un arreglo funcional no termina el flujo completo: faltan pruebas, calidad y
memoria hasta que exista evidencia. No instales herramientas globales ni asumas
acceso a Grafana, repos externos, Jenkins o producción.

## Decidir el alcance al empezar

- **Completo por defecto:** toda solicitud de corregir, implementar o actualizar
  un servicio, incluida una descripción de síntoma y comportamiento esperado
  orientada a un cambio. Mantén este modo aunque una skill interna entregue un resultado
  parcial. No lo reduzcas al encontrar una corrección pequeña.
- **Individual:** cuando el desarrollador pide solo una capacidad (diagnóstico,
  contexto, unitarias, Karate, sanity, commits, memoria, etc.) o delimita el
  alcance explícitamente. No activa fases ajenas al pedido.

No infieras modo individual de tu propio anuncio de “auditoría” ni del tamaño
del arreglo. La reducción de alcance debe venir del pedido del desarrollador.

Anuncia `Modo completo` o `Modo individual: <alcance>` y un identificador de tarea.
Acepta contexto libre, logs, consola, MD, contrato y referencias opcionales.
Usa lo disponible; resuelve solo las ambigüedades funcionales que bloquean una
acción concreta y continúa con trabajo independiente.

## Cargar instrucciones de verdad

Una skill no es un subagente ni se ejecuta por escribir su nombre. Antes de aplicar
cada una, carga su SKILL.md mediante la herramienta de skills si está disponible;
si no, léelo con la herramienta de lectura de archivos. Usa los enlaces de la
tabla, relativos a este archivo. Carga solo las skills de la fase actual.
No declares una skill aplicada si solo leíste su nombre/descripción.
Si no puedes acceder al contenido, registra la ruta y el bloqueo; no improvises
una copia de sus instrucciones. No es necesario habilitar ejecución en subagentes.

Si provienes del plugin, lee [reglas compartidas](../rules/backend.instructions.md)
y carga [preparación](../skills/backend-preparar-repo/SKILL.md) cuando falte el
soporte o cambie su versión. La raíz del plugin se obtiene de la ruta real del
archivo cargado; no es la raíz del microservicio. En instalación por archivos,
lee `.github/copilot-instructions.md` del microservicio y el soporte ya instalado.
No presupongas que instrucciones del repo del plugin son instrucciones del servicio.

Lee `engineering/backend/OPERACION.md` después de preparar. Java/Maven compartidos
se guardan en overrides locales; consulta ENTORNO.md y diagnostica versiones antes
del build. Los scripts requieren Python 3.10+ sin librerías pip ni ipykernel.

## Fases del modo completo

Antes de cada fase anuncia `[n/8] <fase> — skills: <nombres>` y cárgalas de verdad.
Al acabar indica resultado y evidencia. Si no aplica, explica el motivo concreto.
Registra la trazabilidad en `docs/engineering/changes/<tarea>/change.md`, usando
el template CAMBIO: modo, fase, skills, carga, resultado, rutas/comandos y pendientes.
La preparación es una precondición, no una fase que sustituya al cambio.

Tras preparar soporte, guarda solamente el pedido actual del desarrollador en
`.assistant-local/backend/<tarea>/request.txt` (sin adjuntos/logs ni secretos).
Ejecuta `backend.py workflow-start --repo <raíz> --task <tarea> --request-file <ruta>`.
El modo predeterminado es complete; individual requiere `--mode individual
--scope-quote <cita literal que limita el pedido>`. Conserva esta decisión al reanudar;
no abras otra tarea para eludir pendientes. La copia del pedido debe ser fiel,
sin convertir “corrige” en “solo diagnostica”. Si no puedes registrar el pedido,
mantén el alcance humano y reporta el control pendiente, sin afirmar cierre verificado.

Después de leer cada SKILL.md con herramientas y terminar una fase, ejecuta
`backend.py workflow-phase --repo <raíz> --task <tarea> --phase <n> --status DONE
--skill <ruta real al SKILL.md> --evidence <artefacto relativo al servicio>`;
repite --skill/--evidence según corresponda. Este comando registra hashes;
no carga las instrucciones en tu contexto ni demuestra que las comprendiste.
Contrato/config permiten NOT_APPLICABLE con --reason; bloqueos se registran con
BLOCKED y --reason. Los artefactos deben describir acciones/resultados reales,
no repetir las instrucciones ni afirmar resultados sin sus reportes.
Prefiere artefactos por fase que se conserven sin cambios (plan.md, evidencia de
pruebas, etc.). La bitácora en construcción puede cambiar: vuelve a registrar
una fase si cambia su evidencia legítimamente; no edites hashes para forzar el cierre.

| Fase | Skills que debes cargar | Resultado necesario |
| --- | --- | --- |
| 1. Contexto y evidencias | [contexto](../skills/backend-contexto/SKILL.md), [evidencias](../skills/backend-evidencias/SKILL.md) | Flujo real, perfil, causas/hipótesis y baseline viable |
| 2. Plan | [plan](../skills/backend-plan/SKILL.md) | Aceptación y matriz de clases/métodos, contrato, config y pruebas antes de editar lógica |
| 3. Contrato | [contrato](../skills/backend-contrato/SKILL.md) si aplica | Fuente y regeneración; o motivo de no cambio de interfaz |
| 4. Implementación | [implementación](../skills/backend-implementacion/SKILL.md); [errores HTTP](../skills/backend-errores-http/SKILL.md) para este tipo de fallo | Causa específica corregida y regresión definida |
| 5. Pruebas | [unitarias](../skills/backend-pruebas-unitarias/SKILL.md), [Karate](../skills/backend-karate/SKILL.md); [Kafka](../skills/backend-kafka/SKILL.md) si aplica | Pruebas significativas del cambio y regresiones; no basta con generar tests |
| 6. Configuración | [config manual](../skills/backend-config-manual/SKILL.md) si aplica | Delta por ambiente o evidencia de que no cambia configuración compartida |
| 7. Calidad completa | [calidad](../skills/backend-calidad/SKILL.md) | clean install sin omisiones, informes actuales y verify con gates aplicables aprobados |
| 8. Memoria y entrega | [memoria](../skills/backend-memoria/SKILL.md), [commits](../skills/backend-commits/SKILL.md) en modo preparación | Mapa/bitácora actualizados, métricas y mensaje propuesto; commits efectivos solo si se autorizan |

No conviertas “si aplica” en permiso para omitir unitarias, calidad o memoria.
Karate/otros gates admiten solamente excepciones justificadas por el perfil y
la política; no inventes una aprobación. Un error HTTP 204 requiere probar cuerpo
vacío y que auth, timeouts y errores ajenos conservan el mapeo correcto.

Presenta el plan y continúa con el cambio autorizado. No pidas aprobación rutinaria
para cada fase. Si falta una decisión o infraestructura, marca esa dependencia,
continúa con fases independientes y conserva lo pendiente.

## Comprobar antes de cerrar

En modo completo, lee nuevamente el registro de fases y la verificación actual.
Ejecuta `backend.py workflow-close --repo <raíz> --task <tarea> --run-id <run>
--acceptance-evidence <ruta relativa a evidencia del escenario>` y utiliza su
resultado. Revalida gates desde sus ejecuciones; no acepta un PASS escrito a mano.
En modo individual omite run-id/acceptance-evidence si son ajenos al pedido.
Si no ejecutaste este cierre, indica control pendiente y no LOCAL_VERIFIED.
Solo entrega `LOCAL_VERIFIED` si aceptación y gates aplicables tienen evidencia
vigente y la memoria está actualizada. Si código/config/entorno cambió después de
los checks, repite los afectados. No inventes porcentaje de cobertura ni un PASS.
Si faltan tests, Maven, acceso a skills, reportes o preparación, entrega `BLOCKED`
con el arreglo realizado y el trabajo pendiente; no lo presentes como completo.
Un clean install previo al cambio solo es baseline; no acredita el build final.
Tests focalizados con -Dtest permiten iterar, pero no sustituyen la suite completa,
Karate o cobertura. Un fallo previo demostrado sigue bloqueando gates completos:
no lo ocultes ni edites cambios ajenos para forzar verde. Continúa con trabajo
independiente y describe la dependencia exacta.
Si los logs no contienen la señal funcional que activa el mapeo esperado, distingue
corrección defensiva de causa demostrada. Prueba el request representativo en el
límite HTTP antes de declarar que el incidente quedó resuelto. Un 404 genérico
no prueba un código de negocio ni autoriza devolver 204.
Un diff local no identifica la versión desplegada: contrasta imagen/commit de DEV
antes de afirmar que falta el arreglo. Un test fallido no es automáticamente
“desactualizado”: decide con contrato/criterio esperado si el defecto está en código
o prueba. No recomiendes desplegar una corrección con gates requeridos pendientes.
**SCOPED_TASK_DONE está reservado al modo individual.** DIAGNOSED corresponde a
una solicitud de diagnóstico. Un estado de una skill interna no cambia el modo
ni sustituye la verificación final del orquestador.

El cierre debe incluir tabla de las ocho fases con skills aplicadas, estado y
ruta/comando de evidencia, más gates, diff y pendientes reales. Una frase como
“usé todas las skills” no es evidencia. No es obligatorio que la UI muestre una
llamada nativa a skills: la lectura real, las acciones y sus artefactos son
observables. Distingue esa lectura de una invocación nativa o de un subagente.
La memoria interna del cliente no sustituye mapa y bitácora en docs/engineering.

Guarda punto de reanudación en `.assistant-local/backend/<tarea>/state.json`:
modo, fase, siguiente acción, cambios propios y bloqueos. Al reanudar compara
huellas, lee diff y recupera fases pendientes. No repitas toda la comprensión
si la memoria sigue vigente; relee el flujo afectado.
Reintenta hasta tres correcciones justificadas por fallo; no repitas bloqueos
idénticos de permisos/infraestructura. CI, revisión humana, traslado manual y
producción se reportan por separado. No hagas push, PR ni despliegue por defecto.
