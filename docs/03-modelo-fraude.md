# 03 · Modelo de Detección de Fraude / Comportamientos Atípicos

## 1. Problema de negocio

Identificar **comportamientos transaccionales atípicos** que puedan indicar fraude, abuso o riesgo, en
tiempo real, minimizando falsos positivos (fricción con clientes legítimos).

## 2. Naturaleza del problema

- Detección de anomalías con **etiquetas escasas y desbalanceadas** (el fraude es raro y las etiquetas llegan tarde).
- Requiere **baja latencia** (decisión en línea durante la transacción).
- Necesita **explicación** para que un analista humano pueda actuar.

## 3. Enfoque híbrido (supervisado + no supervisado)

| Componente | Técnica | Rol |
|---|---|---|
| Modelo no supervisado | Isolation Forest / Autoencoder | Detectar anomalías sin etiqueta (fraude nuevo/emergente) |
| Modelo supervisado | XGBoost/LightGBM sobre fraudes confirmados | Alta precisión donde hay historial |
| Reglas de negocio | Motor de reglas (límites, listas negras) | Guardarraíles y cumplimiento inmediato |
| Ensemble | Score combinado (anomalía + fraude + reglas) | Decisión final con umbral calibrado |

El **score combinado** pondera cada componente; el umbral de alerta se calibra contra el costo de un
falso positivo vs. un fraude no detectado.

## 4. Variables / features

| Dominio | Features | Justificación |
|---|---|---|
| Monto y frecuencia | monto, # transacciones por ventana | Velocidad de gasto anormal |
| Comportamiento histórico | desviación vs. perfil del cliente | Lo "atípico" es relativo al cliente |
| Geografía | distancia entre transacciones, IP/ubicación | Fraude por ubicación |
| Dispositivo/ID | cambios de dispositivo, fingerprints | Account takeover |
| Red | conexiones entre cuentas/receptores | Fraude en anillos/redes |
| Temporal | hora, día, intervalo entre transacciones | Patrones de bot |

## 5. Evaluación

| Métrica | Objetivo | Por qué |
|---|---|---|
| Precision | alta (pocos FP) | Cada FP es fricción con cliente real |
| Recall | balanceado | No dejar pasar fraude |
| PR-AUC | alto | Mejor que ROC en clases desbalanceadas |
| Tasa de falsos positivos | baja (< 5%) | Experiencia del cliente |
| Latencia P95 | < 100 ms | Decisión en línea |
| F1 (por umbral) | optimizado | Balance precision/recall |

Evaluación con **evaluación temporal** + test de detección de fraude emergente (el modelo debe capturar
fraude no visto en entrenamiento).

## 6. Feedback loop

1. Alerta generada → analista confirma/descarta.
2. Etiqueta confirmada → se registra como ground truth.
3. Reentrenamiento periódico (semanal) con nuevas etiquetas.
4. Medición de degradación entre reentrenamientos.

## 7. Latencia y despliegue

- Feature store **online** (Redis) para features de perfil y agregados de ventana.
- Serving en K8s con autoscaling; inferencia en CPU (modelos tabulares ligeros).
- Degradación controlada: si el score online falla, fallback a reglas de negocio (never block la transacción por fallo técnico).
