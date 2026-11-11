---
title: "Plataforma Analítica de Riesgo Financiero y Detección de Fraude"
subtitle: "Prueba Técnica · Data Scientist Senior · Hitss Colombia / Claro Colombia"
author: "Alejandro"
date: "2026-11-11"
geometry: margin=2cm
---

# 1. Entendimiento del problema

Una organización bancaria quiere evolucionar su plataforma analítica hacia modelos predictivos y un
agente inteligente IA. Se pide entrenar y evaluar **dos modelos** sobre fuentes de datos heterogéneas
(cloud + on-prem):

- **Modelo de riesgo financiero:** evalúa y actualiza continuamente el nivel de riesgo de un cliente.
- **Modelo de fraude/anomalías:** identifica comportamientos transaccionales atípicos.

El alcance no es solo el modelo: cubre **todo el ciclo de vida** (datos, entrenamiento, despliegue,
monitoreo, consumo) con buenas prácticas de industria.

# 2. Arquitectura de referencia

## Capas end-to-end

- **Fuentes:** BD core (on-prem) + data lake (cloud) + eventos transaccionales.
- **Ingesta:** Spark/Airflow (batch) + Kafka/Spark Streaming (real-time).
- **Entrenamiento:** pipeline reproducible con feature engineering y validación.
- **Registro:** MLflow Model Registry (versionado y stages).
- **Serving:** FastAPI (online) + Spark (batch), sobre Kubernetes.
- **Consumo:** API gateway gobernada para el agente IA y aplicaciones.
- **Monitoreo:** Evidently AI + Great Expectations + Prometheus/Grafana.

## Decisiones clave

| Decisión | Elección | Justificación |
|---|---|---|
| Orquestación | Airflow + Spark + Kafka | Conviven batch (riesgo) y streaming (fraude) |
| Feature store | Feast (online/offline) | Consistencia train/serve |
| Registro | MLflow | Versionado y promoción gobernada |
| Serving | FastAPI + Spark sobre K8s | Latencia <100ms y batch escalable |
| Monitoreo | Evidently + GE + Prometheus | Drift, calidad y operación |
| Explainability | SHAP + model cards | Exigencia regulatoria bancaria |

# 3. Modelo de riesgo financiero

- **Tipo:** clasificación supervisada (probabilidad de default) con score continuo.
- **Target:** default a 90+ días en ventana 6-12 meses.
- **Algoritmo:** Gradient Boosting (LightGBM/XGBoost) + baseline de regresión logística interpretable.
- **Variables:** sociodemográficas, producto, comportamiento de pago, transaccional, buró, macro.
- **Feature engineering:** agregaciones temporales (3/6/12m), ratios, target encoding out-of-fold.
- **Evaluación:** AUC ≥ 0.80, KS ≥ 0.35, Gini ≥ 0.55, precision@k, calibración, PSI < 0.1.
- **Validación:** CV temporal (walk-forward) para evitar fuga de futuro.
- **Explicabilidad:** SHAP global y local para el agente IA y analistas.
- **Frecuencia:** retraining mensual + trigger por drift; scoring batch y on-demand.

# 4. Modelo de fraude / anomalías

- **Naturaleza:** etiquetas escasas y desbalanceadas, baja latencia requerida.
- **Enfoque híbrido:** Isolation Forest/Autoencoder (no supervisado) + XGBoost (supervisado) + reglas, con score combinado calibrado por costo.
- **Variables:** monto/frecuencia, desviación vs perfil, geografía, dispositivo, red, temporal.
- **Evaluación:** precision alta (pocos FP), recall balanceado, PR-AUC, FPR < 5%, latencia P95 < 100ms.
- **Feedback loop:** analista confirma/descarta → ground truth → reentrenamiento semanal.
- **Resiliencia:** fallback a reglas si el score online falla (nunca bloquear por fallo técnico).

# 5. Ciclo de vida (MLOps)

- **Estados:** Registered → Staging → Production → Archived (MLflow).
- **Versionado:** semver + run ID + hash de datos; artefactos inmutables.
- **Promoción con gates:** tests → shadow deployment → validación → aprobación humana.
- **Estrategias:** shadow, canary, blue/green, champion/challenger.
- **CI/CD:** push → lint/test → training → validación → registro → despliegue.
- **Gobierno:** aprobaciones por rol, model cards, ADR, trazabilidad completa.
- **Manejo del cambio:** retraining por drift, canales de feedback, revisión trimestral.

# 6. Monitoreo y control

| Dimensión | Métrica | Herramienta |
|---|---|---|
| Data drift | PSI / KS por feature | Evidently AI |
| Concept drift | AUC / precision degradados | Evidently + negocio |
| Calidad de datos | nulos, rangos, esquema | Great Expectations |
| Operativo | latencia, throughput, errores | Prometheus/Grafana |

- **Umbrales PSI:** < 0.1 OK, 0.1-0.25 alerta, > 0.25 crítico.
- **Respuesta:** drift → retraining/rollback; latencia → escalado HPA.
- **Anticipación:** monitoreo de anomalías en features, pruebas de estrés, runbooks.

# 7. Entrega operativa y consumo

- **Riesgo:** batch (cartera) + API on-demand.
- **Fraude:** API real-time.
- **API:** REST versionada (/v1), OAuth2/mTLS, rate-limit, contrato OpenAPI.
- **Agente IA:** consume scores + explicaciones SHAP, traduce a lenguaje natural, recomienda acciones; sin decidir solo en temas sensibles.
- **Acceso:** gateway con scopes, cuotas y auditoría por consumidor.

# 8. Supuestos, alternativas y riesgos

## Supuestos

- Datos transaccionales, producto, sociodemográficos y buró con ≥ 18-24 meses de histórico.
- Infra cloud (K8s + data lake) y BD core on-prem integrables.
- Etiquetas de fraude (con retardo) y defaults históricos disponibles.
- Cumplimiento normativo (habeas data, explicabilidad, auditoría).

## Alternativas descartadas

| Alternativa | Por qué |
|---|---|
| Deep learning para tabular | GBM similar desempeño, menos costo, más explicable |
| Todo on-prem / todo cloud | Se adopta híbrido por dependencias |
| Sin feature store | Riesgo de train/serve skew |
| Modelo único para ambos problemas | Targets, latencia y métricas distintas |
| AutoML puro | Menos control y trazabilidad |

## Riesgos aceptados

- Etiquetas de fraude tardías → enfoque híbrido + feedback loop.
- Falsos positivos → umbral calibrado + explicación.
- Data drift → monitoreo PSI/KS + retraining.
- Complejidad MLOps → automatización progresiva (MVP primero).

# 9. Métricas y valor

- **Técnicas:** AUC/KS/Gini (riesgo), precision/recall/PR-AUC/FPR (fraude).
- **Negocio:** pérdidas por fraude evitadas, reducción de mora, menos falsos positivos.
- **Valor:** mejores decisiones de otorgamiento, menos pérdida, mejor experiencia, capacidad de escalar a nuevos casos de uso.

# 10. Plan y mejoras

- **Entregables:** repo de código, documentación, pipeline, API, monitoreo, mockups.
- **Tiempo MVP:** ~10-12 semanas (ingesta 2s, riesgo 2-3s, fraude 3-4s, API 1-2s, monitoreo 2s).
- **Aceleradores:** feature store desde el día 1, plantillas de pipeline, shadow deployment, auto-retraining por drift.

## Presión para salir antes a producción

1. Priorizar riesgo primero; fraude en shadow mode.
2. MVP con guardarraíles (modelo simple + monitoreo básico).
3. Reducir alcance, no el gobierno mínimo.
4. Comunicar riesgos explícitamente.
5. Nunca salir sin feature store mínimo, rollback y alerta de drift.

# 11. Mockups de salidas

**API riesgo:**

    { "cliente_id": "CLI-1000231", "score": 0.18, "bucket": "bajo",
      "explicacion": { "top_factores": [ ... ] } }

**Alerta fraude:**

    { "transaccion_id": "TX-9988123", "score_anomalia": 0.93,
      "decision": "REVISAR", "razones": ["monto 8x mediana", ...] }

**Dashboard monitoreo:** PSI por feature, performance de fraude, latencia y throughput.

# 12. Mejoras futuras

- AutoML guiado, explicaciones LLM en lenguaje natural.
- Detección de fraude en grafos (anillos).
- Scoring de riesgo en streaming.
- Online learning con monitoreo reforzado.
- Data contracts para robustecer la ingesta.

---

## Conclusión

La solución es **pragmática y escalable**: GBM tabular con feature store y MLflow, un enfoque híbrido
para fraude con feedback loop, monitoreo continuo de drift y una API gobernada que alimenta al agente IA.
El valor no está solo en predecir, sino en **explicar y hacer accionable** el resultado para el negocio.
