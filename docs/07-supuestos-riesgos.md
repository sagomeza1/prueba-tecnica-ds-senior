# 07 · Supuestos, alternativas y riesgos

## 1. Supuestos del ejercicio

- Existe acceso a datos transaccionales, de producto, sociodemográficos y de buró, con histórico suficiente (≥ 18-24 meses).
- La infraestructura cloud está disponible (K8s + data lake) y la BD core on-prem se integra vía conectores.
- Se dispone de etiquetas de fraude (aunque con retardo) y de defaults históricos para riesgo.
- Cumplimiento normativo: datos personales (habeas data), explicabilidad y auditoría.
- Latencia de fraude objetivo < 100 ms y volumen alto (escala con streaming).
- Equipo: DS + ML Engineer + Data Engineer + Compliance.

## 2. Alternativas consideradas y descartadas

| Alternativa | Decisión | Por qué |
|---|---|---|
| Deep learning (LSTM/transformers) para tabular | Descartada (primera iteración) | GBM logra desempeño similar con menos costo y mayor explicabilidad |
| Todo on-premise | Descartada | Limita escalabilidad y madurez de servicios |
| Todo cloud | Descartada | BD core on-prem y dependencias existentes → híbrido |
| Sin feature store (features en código) | Descartada | Riesgo de train/serve skew y duplicación |
| Modelo único para ambos problemas | Descartada | Riesgo y fraude tienen targets, latencia y métricas distintas |
| AutoML puro | Descartada | Menos control, trazabilidad y explicabilidad |
| Serving serverless (solo Lambda) | Parcial | Riesgo de cold-start en latencia de fraude → K8s preferido |

## 3. Riesgos aceptados explícitamente

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Etiquetas de fraude tardías/ruidosas | Degradación supervisado | Enfoque híbrido con no supervisado + feedback loop |
| Falsos positivos | Fricción con clientes | Umbral calibrado por costo, explicación al analista |
| Data drift | Degradación silenciosa | Monitoreo PSI/KS + retraining automático |
| Train/serve skew | Scores inconsistentes | Feature store único online/offline |
| Complejidad operativa (MLOps) | Costo de mantenimiento | Automatización progresiva, MVP primero |
| Dependencia de la BD on-prem | Punto único de falla | Replicación a data lake, ventanas de batch |
