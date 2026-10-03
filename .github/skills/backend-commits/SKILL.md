---
name: backend-commits
description: Evalúa métricas corporativas y prepara o crea commits y PRs Java según alcance pedido, comprobando calidad vigente. Úsala para solo commits, evaluación de score o preparación de entrega.
---

# Commits y PR BACKEND

Si estás usando el plugin y faltan recursos del microservicio, usa primero
[backend-preparar-repo](../backend-preparar-repo/SKILL.md); conserva el modo individual.

Lee `engineering/backend/references/COMMITS.md`. “Evaluar/preparar” no ejecuta commit.
“Haz commit” autoriza commit local del cambio propio; push/PR necesitan pedido
correspondiente y pueden estar autorizados desde antes. No repetir aprobación.

1. Inspecciona rama, base real y diff staged/unstaged. `backend.py metrics --base`
   muestra commits, archivos y líneas; interpreta generado y docs por separado
   sin ocultarlos. No inventa base develop ni reviewer identities.
2. Para commit de código consulta evidencia actual (`backend.py verify`). Si falta,
   puede ejecutar calidad requerida sin implementar funcionalidad nueva.
   Un pedido de solo score puede terminar sin build, explicitando NOT_RUN.
3. Prepara lista explícita de archivos propios y mensaje en inglés de máximo
   72 caracteres: type(scope): JIRA-TICKET message. No añade cambios ajenos.
4. Propone commit atómico y separación por responsabilidad cuando amerite.
   No fracciona funcionalidad ni omite tests/docs para manipular métricas.
   No hace amend, squash o rebase de commits publicados sin alcance autorizado.
5. Si está autorizado ejecuta commit; confirma contenido. Para push/PR usa
   alcance autorizado y modelo corporativo; mínimo tres revisores reales según
   política del archivo original. Si faltan nombres deja checklist pendiente.

Salida: métricas actual/proyección, quality gate, mensaje/lista de archivos,
acciones ejecutadas y pendientes. No bloquea el cierre local por falta de push.
