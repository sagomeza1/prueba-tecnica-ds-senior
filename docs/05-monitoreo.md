# 05 · Monitoreo y control en producción

## 1. Qué se monitorea

| Dimensión | Qué mide | Herramienta |
|---|---|---|
| Data drift | Distribución de features vs. entrenamiento (PSI, KS) | Evidently AI |
| Concept drift | Degradación de performance (AUC, precision/recall) | Evidently + métricas de negocio |
| Calidad de datos | nulos, rangos, esquema, cardinalidad | Great Expectations |
| Operativo | latencia, throughput, errores, uptime | Prometheus/Grafana |
| Negocio | falsos positivos, fraudes detectados, defaults | Dashboards/BI |

## 2. Detección de drift

- **PSI (Population Stability Index)** por feature: < 0.1 estable, 0.1-0.25 alerta, > 0.25 crítico.
- **KS de drift** comparando distribución actual vs. referencia.
- Reportes periódicos (diario en fraude, semanal en riesgo) con alertas automáticas.

## 3. Degradación de performance

- **Fraude:** precision/recall sobre etiquetas confirmadas (con retardo por el feedback loop).
- **Riesgo:** AUC/KS sobre defaults observados en la ventana de validación.
- Umbrales de alerta configurados; degradación sostenida dispara retraining o revisión.

## 4. Calidad de datos de entrada

- Expectativas de Great Expectations: esquema, nulos, rangos, unicidad, validación de categóricas.
- Bloqueo de scoring (o fallback) si los datos de entrada violan expectativas críticas.

## 5. Alertas y respuesta

| Señal | Acción automática | Acción humana |
|---|---|---|
| Drift de feature crítico | Marcar feature degradada, excluir si procede | Revisar causa raíz |
| Métrica bajo umbral | Disparar retraining / rollback | Aprobar promoción |
| Error de latencia | Escalar réplicas (HPA) | Investigar infra |

## 6. Anticipación de escenarios

- **Detección temprana de cambio de comportamiento** (p. ej., nueva tipología de fraude) vía monitoreo de anomalías en los propios features.
- **Pruebas de estrés** y simulación de degradación para validar la respuesta del sistema.
- **Runbooks** documentados para cada alerta.
