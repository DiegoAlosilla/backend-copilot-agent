---
name: backend-calidad
description: Valida cambios Java con build final, suites, Checkstyle y JaCoCo del proyecto y comunica evidencia vigente o gates pendientes.
user-invocable: false
---

# Calidad con herramientas del servicio

Descubre comandos/gates en POM/perfiles/CI y aplica CONTEXTO_BACKEND. Conserva
política acordada: INSTRUCTION global mínimo 95%, cero tests omitidos y cero
violaciones Checkstyle. Política corporativa más exigente prevalece; excepciones
explícitas llevan origen/alcance. No amplíes exclusiones ni rebajes umbrales.

Tras cambios Java ejecuta Maven/wrapper `clean install` con settings/perfiles
aplicables, sin omisiones. Comprueba qué suites/gates ejecuta realmente; completa
los restantes con objetivos/runners existentes sin inventar perfiles. Checkstyle
exige `check` o binding que falle, no solo reporte. Si build cubre un gate, no
repitas sin motivo. Karate separado va después para que clean no borre evidencia.

Relaciona salida/comando con reportes actuales Surefire/Failsafe/Karate,
Checkstyle y JaCoCo. Cobertura INSTRUCTION = covered / (covered + missed) del
alcance global vigente: contador raíz o módulos no solapados, sin doble conteo.
Informa BRANCH y exclusiones aparte. Reportes viejos/ausentes, cero tests,
contador cero o suite focalizada no acreditan cobertura global. Usa lectura/
cálculo del editor sin generar evaluadores auxiliares.

Corrige fallos del cambio y repite checks afectados. Consulta bloqueos de entorno
con backend-entorno sin reintentar idénticamente. Conserva fallos previos sin
tocar cambios ajenos para forzar verde. CI/Sonar/producción se reportan aparte.

En auditoría/plan/docs justifica validación pertinente y gates no ejecutados;
no modifica código para completar fases. Entrega gate, comando/reporte, resultado
y pendiente en chat. Valida localmente solo con aceptación y gates aplicables verdes.
