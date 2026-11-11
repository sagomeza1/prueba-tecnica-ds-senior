# 09 · Plan de entregables, tiempo estimado y mejoras

## 1. Entregables

| # | Entregable | Descripción |
|---|---|---|
| 1 | Repositorio de código | Esqueletos de componentes/clases, configs, infra |
| 2 | Documentación | Arquitectura, modelos, ciclo de vida, monitoreo, supuestos |
| 3 | Pipeline reproducible | DAG de entrenamiento y CI/CD para ML |
| 4 | API de consumo | Contrato OpenAPI versionado |
| 5 | Monitoreo | Drift, calidad de datos y alertas |
| 6 | Mockups | Salidas técnicas y dashboard |

## 2. Tiempo estimado (MVP)

| Fase | Duración |
|---|---|
| Ingesta de datos y feature store | 2 semanas |
| Modelo de riesgo (entrenar + evaluar + servir batch) | 2-3 semanas |
| Modelo de fraude (anomalías + serving real-time) | 3-4 semanas |
| API de consumo y gateway | 1-2 semanas |
| Monitoreo y CI/CD | 2 semanas |
| **Total MVP** | **~10-12 semanas** |

## 3. Mejoras al ciclo de vida para acelerar

- **Feature store desde el día 1** (evita rework de train/serve skew).
- **Plantillas de pipeline** reutilizables para onboarding rápido de modelos nuevos.
- **Shadow deployment automático** en staging para validar antes de producción.
- **Auto-retraining por drift** (reduce intervención manual).
- **Data contracts** tempranos para evitar reprocesos de ingesta.
- **Registro de decisiones (ADR)** para no rediscutir elecciones ya tomadas.

## 4. Sustentación — presión para salir antes a producción

Si la dirección presiona para adelantar la salida a producción, estas serían mis decisiones:

1. **Priorizar el modelo de riesgo primero** (mayor valor y menor complejidad de latencia) y desplegar fraude en *shadow mode* (puntúa sin bloquear) mientras madura.
2. **MVP con guardarraíles:** modelo simple (logística/reglas) + monitoreo básico de drift desde el inicio.
3. **Reducir alcance, no calidad de gobierno:** mantener registro, versionado y monitoreo mínimos, aunque sea manual al inicio.
4. **Comunicar riesgos explícitamente:** qué se acepta (menos precisión inicial, drift no cubierto) y plan para cerrarlos en semanas siguientes.
5. **Nunca salir sin:** feature store mínimo, rollback, y al menos una métrica de drift alertando.

## 5. Riesgos de acelerar y cómo mitigarlos

| Riesgo | Mitigación |
|---|---|
| Train/serve skew por no tener feature store | Feature store mínimo en línea |
| Modelo sin validar en producción | Shadow mode + canary |
| Sin monitoreo de degradación | PSI básico desde el día 1 |
| Falsos positivos altos en fraude | Umbral conservador + revisión humana |
