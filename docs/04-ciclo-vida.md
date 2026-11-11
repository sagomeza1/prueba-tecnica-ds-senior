# 04 · Ciclo de vida y gobierno de modelos (MLOps)

## 1. Estados del modelo

Se usa el Model Registry de MLflow con estados explícitos y transiciones gobernadas:

    Registered → Staging → Production → Archived

- **Registered:** modelo entrenado y registrado, con métricas y artefactos versionados.
- **Staging:** candidato a producción; pasa pruebas de validación y shadow deployment.
- **Production:** sirviendo tráfico real; monitoreado de forma continua.
- **Archived:** retirado, con trazabilidad conservada para auditoría.

## 2. Versionado

- **Semver** (major.minor.patch) + ID de run de MLflow + hash de datos de entrenamiento.
- Cada versión inmutable; asociada a: código (commit git), features, dataset, hiperparámetros, métricas y artefactos.
- El `feature store` versiona también las definiciones de features, garantizando consistencia train/serve.

## 3. Transición y promoción (gates)

| Etapa | Gate | Automatización |
|---|---|---|
| Registered → Staging | Tests unitarios + métricas sobre umbral | CI (automatizado) |
| Staging → Production | Shadow deployment + validación de drift + aprobación | CI/CD + aprobación humana |
| Production → Archived | Métricas bajo umbral sostenido o reemplazo | Automatizado con revisión |

## 4. Estrategias de despliegue

- **Shadow deployment:** el candidato puntúa en paralelo sin afectar tráfico; se comparan métricas.
- **Canary:** % creciente de tráfico al nuevo modelo con monitoreo de error.
- **Blue/green:** switch atómico con rollback inmediato.
- **Champion/challenger:** el modelo vigente (champion) compite con candidatos; se promueve al ganador.

## 5. Pipeline de entrenamiento (CI/CD para ML)

    push → lint/tests → feature build → training → validación → registro → despliegue staging → prod

- **Orquestación:** Airflow DAG (retraining programado) + eventos de retrigger por drift.
- **Reproducibilidad:** todo versionado (código, datos, features, modelo, config).
- **Rollback:** a versión anterior en segundos vía blue/green.

## 6. Gobierno y auditoría

- Aprobaciones por roles (DS, ML Engineer, Risk/Compliance).
- Model cards y registro de decisiones (ADR).
- Trazabilidad completa: qué modelo, con qué datos, decidió qué, y por qué.
- Cumplimiento de retención y retiro seguro (archivado).

## 7. Manejo del cambio (evolución de datos y negocio)

- Retraining automático ante drift de datos o de concepto.
- Canales de feedback (etiquetas de fraude, defaults confirmados).
- Revisión trimestral del portafolio de modelos para retirar o actualizar.
