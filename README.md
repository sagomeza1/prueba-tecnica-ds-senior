# Plataforma Analítica de Riesgo Financiero y Detección de Fraude

> Prueba técnica — Data Scientist Senior · Hitss Colombia / Claro Colombia
> **Autor:** Alejandro · **Fecha:** 2026-11-11

## Resumen ejecutivo

Se diseña una plataforma analítica productiva que entrena, sirve y gobierna **dos modelos** sobre el
mismo ecosistema de datos bancarios:

1. **Modelo de Riesgo Financiero (Riesgo de Crédito)** — estima y actualiza de forma continua el nivel
   de riesgo de un cliente a lo largo del tiempo (probabilidad de default / bucket de riesgo).
2. **Modelo de Detección de Fraude / Comportamientos Atípicos** — identifica transacciones anómalas que
   puedan indicar fraude, abuso o riesgo, en tiempo real.

Ambos alimentan a un **agente inteligente IA de negocio** a través de una capa de API gobernada, y la
plataforma cubre el ciclo de vida completo del modelo (entrenamiento → registro → validación → despliegue
→ monitoreo → retiro), con buenas prácticas de industria.

## Decisiones clave (resumen)

| Decisión | Elección | Justificación |
|---|---|---|
| Orquestación | Airflow + Spark (batch) y Kafka/Spark Streaming (real-time) | Bancario: conviven procesos batch (riesgo) y streaming (fraude) |
| Feature store | Feast (online + offline) | Consistencia train/serve, reuso de features |
| Registro de modelos | MLflow Model Registry | Versionado, stages, transición gobernada |
| Serving | FastAPI (online) + Spark (batch), sobre Kubernetes | Latencia <100ms en fraude; batch escalable en riesgo |
| Monitoreo | Evidently AI + Great Expectations + Prometheus/Grafana | Drift, calidad de datos y métricas operativas |
| Infraestructura | Híbrida: cloud (K8s) + on-prem (BD core) | Reuso de infraestructura existente de la organización |
| Explainability | SHAP + model cards | Riesgo bancario exige explicabilidad ante regulación |

## Estructura del repositorio

    prueba-ds-senior/
    ├── README.md                     ← este documento
    ├── docs/
    │   ├── 01-arquitectura.md        ← arquitectura de referencia (end-to-end)
    │   ├── 02-modelo-riesgo.md       ← diseño modelo de riesgo financiero
    │   ├── 03-modelo-fraude.md       ← diseño modelo de fraude/anomalías
    │   ├── 04-ciclo-vida.md          ← MLOps: versionado, stages, promoción
    │   ├── 05-monitoreo.md           ← drift, degradación, calidad de datos
    │   ├── 06-entrega-consumo.md     ← API, batch, streaming, agente IA
    │   ├── 07-supuestos-riesgos.md   ← supuestos, alternativas descartadas, riesgos
    │   └── 08-metricas-mockups.md    ← métricas, valor y mockups de salidas
    ├── src/
    │   ├── common/                   ← utilidades, config, logging, métricas
    │   ├── features/                 ← feature store y feature engineering
    │   ├── risk_model/               ← modelo de riesgo financiero
    │   ├── fraud_model/              ← modelo de fraude/anomalías
    │   ├── serving/                  ← API online y scoring batch
    │   └── monitoring/               ← drift, calidad, alertas
    ├── configs/                      ← YAML de entorno (dev/staging/prod)
    ├── infra/k8s/                    ← manifiestos de despliegue
    └── notebooks/                    ← exploración y experimentación

## Cómo leer este entregable

1. Empieza por *docs/01-arquitectura.md* para ver el diseño completo.
2. *docs/02* y *docs/03* detallan cada modelo (variables, enfoque, evaluación).
3. *docs/04*, *docs/05* y *docs/06* cubren el ciclo de vida, monitoreo y entrega.
4. *docs/07* y *docs/08* documentan supuestos, riesgos, métricas y mockups.
5. *src/* contiene los esqueletos de componentes y clases (no el código final).
