# 02 · Modelo de Riesgo Financiero

## 1. Problema de negocio

Estimar y **actualizar de forma continua** el nivel de riesgo financiero de cada cliente a lo largo del
tiempo, para apoyar decisiones de otorgamiento, cupos, precios y cobranza, y alimentar al agente IA.

## 2. Definición del problema de ML

- **Tipo:** clasificación supervisada (probabilidad de default) con salida de score continuo.
- **Unidad de análisis:** cliente (o cliente-producto).
- **Target:** default a 90+ días (evento de mora severa) en una ventana de 6-12 meses.
- **Horizonte:** re-scoreo mensual (batch) + on-demand al evaluar solicitudes.

## 3. Fuentes y variables candidatas

| Dominio | Variables de ejemplo | Justificación |
|---|---|---|
| Sociodemográfico | edad, región, tiempo como cliente | Estabilidad del cliente |
| Producto | tipo de producto, cupo, antigüedad | Exposición y relación |
| Comportamiento de pago | días de mora históricos, pagos mínimos, utilización de cupo | Señal predictiva más fuerte |
| Transaccional | ingresos recurrentes, patrones de gasto, sobregiros | Capacidad de pago |
| Buró | score de buró, consultas recientes | Comportamiento externo |
| Macroeconómico | tasas, desempleo | Efecto de contexto |

## 4. Enfoque de modelamiento

- **Algoritmo principal:** Gradient Boosting (XGBoost/LightGBM) por su desempeño tabular y manejo de no-linealidades.
- **Baseline interpretable:** Regresión logística regularizada, para comparar y para casos que exijan máxima explicabilidad regulatoria.
- **Feature engineering:** agregaciones temporales (rolling 3/6/12 meses), ratios (utilización/cupo), encoding de categóricas con target encoding supervisado y `out-of-fold` para evitar leakage.
- **Tratamiento de desbalance:** scale_pos_weight o sampleo estratificado + calibración (Platt / isotónica).

## 5. Selección de variables

- **Método:** importancia por SHAP + `recursive feature elimination` con validación cruzada temporal.
- **Criterio:** retener variables con contribución estable y alineadas al negocio; descartar las no explicables o con drift alto.
- **Governance:** documentar cada variable en el `feature store` con propietario y definición.

## 6. Evaluación

| Métrica | Objetivo | Por qué |
|---|---|---|
| AUC-ROC | ≥ 0.80 | Capacidad de discriminación |
| KS | ≥ 0.35 | Separación de buenos vs malos |
| Gini | ≥ 0.55 | Equivalente a AUC para riesgo |
| Precision@k (top decil) | alta | Calidad del bucket de mayor riesgo |
| Calibración (Brier) | baja | Probabilidades confiables |
| PSI (estabilidad) | < 0.1 | Estabilidad entre train/serve |

Validación con **CV temporal** (walk-forward) para respetar la secuencia temporal y evitar fuga de futuro.

## 7. Explicabilidad y cumplimiento

- **SHAP** global (variables más influyentes) y local (por cliente) para explicar decisiones al agente IA y a analistas.
- **Model cards** documentando desempeño, limitaciones y sesgos.
- Monitoreo de **fairness** por segmentos sensibles (región, edad) para cumplir regulación.

## 8. Frecuencia de actualización

- Retraining **mensual** programado + retraining **trigger** por drift detectado.
- Re-scoreo de cartera en batch mensual/semanal; scoring on-demand al evaluar solicitudes.
